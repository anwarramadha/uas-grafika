import numpy as np
from glumpy import app, gl, glm, gloo, data
from os.path import abspath

vertex = """
    uniform mat4   u_model;         // Model matrix
    uniform mat4   u_view;          // View matrix
    uniform mat4   u_projection;    // Projection matrix
    attribute vec3 a_position;
    attribute vec3 a_normal;
    varying vec3   v_tex_coord;
    varying vec3   v_normal;
    varying vec3   v_position;  // Interpolated position (out)
    
    void main()
    {
        gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
        v_normal = a_normal;
        v_tex_coord = a_position;
        v_position = a_position;
    }
"""

fragment = """
    uniform mat4      u_model;           // Model matrix
    uniform mat4      u_view;            // View matrix
    uniform mat4      u_normal;          // Normal matrix
    uniform vec3      u_light_position;  // Light position
    uniform vec3      u_light_intensity; // Light intensity
    uniform samplerCube texture;       // Texture
    varying vec3      v_normal;          // Interpolated normal (out)
    varying vec3      v_position;        // Interpolated position (out)
    varying vec3      v_tex_coord;        // Interpolated fragment texture coordinates (out)
    void main()
    {
        // Calculate normal in world coordinates
        vec3 normal = normalize(u_normal * vec4(v_normal,1.0)).xyz;
        // Calculate the location of this fragment (pixel) in world coordinates
        vec3 position = vec3(u_view*u_model * vec4(v_position, 1));
        // Calculate the vector from this pixels surface to the light source
        vec3 surfaceToLight = u_light_position - position;
        // Calculate the cosine of the angle of incidence (brightness)
        float brightness = dot(normal, surfaceToLight) /
                          (length(surfaceToLight) * length(normal));
        brightness = max(min(brightness,1.0),0.0);
        // Calculate final color of the pixel, based on:
        // 1. The angle of incidence: brightness
        // 2. The color/intensities of the light: light.intensities
        // 3. The texture and texture coord: texture(tex, fragTexCoord)
        // Get texture color
        vec4 t_color = textureCube(texture, v_tex_coord);
        gl_FragColor = t_color * (0.1 + 0.9*brightness * vec4(u_light_intensity, 1));
    } """

window = app.Window(width=1024, height=1024)


@window.event
def on_draw(dt):
    global phi, theta, beta

    window.clear()
    program.draw(gl.GL_QUADS)
    # Rotate cube
    # glm.rotate(model, theta, 0, 0, 1)
    # glm.rotate(model, phi, 0, 1, 0)
    # glm.rotate(model, beta, 1, 0, 0)
    program['u_model'] = model
    program['u_normal'] = np.array(np.matrix(np.dot(view, model)).I.T)


@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)


@window.event
def on_resize(width, height):
    program['u_projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)


@window.event
def on_key_press(key, modifiers):
    global phi, theta
    if key == app.window.key.UP:
        glm.translate(view, 0, 0, 0.1)
        program['u_view'] = view

    elif key == app.window.key.DOWN:
        glm.translate(view, 0, 0, -0.1)
        program['u_view'] = view

    elif key == app.window.key.RIGHT:
        glm.translate(view, -0.1, 0, 0)
        program['u_view'] = view
    elif key == app.window.key.LEFT:
        glm.translate(view, 0.1, 0, 0)
        program['u_view'] = view


p = np.array([[+1, +1, +1], [-1, +1, +1], [-1, -1, +1], [+1, -1, +1],
              [+1, -1, -1], [+1, +1, -1], [-1, +1, -1], [-1, -1, -1]])
n = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0],
              [-1, 0, 1], [0, -1, 0], [0, 0, -1]])

faces_p = [0, 1, 2, 3, 0, 3, 4, 5, 0, 5, 6, 1,
           1, 6, 7, 2, 7, 4, 3, 2, 4, 7, 6, 5]
faces_n = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2,
           3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5]

program = gloo.Program(vertex, fragment)
program['a_position'] = [p[i] for i in faces_p]
program['a_normal'] = [n[i] for i in faces_n]

texture = np.zeros((6, 1024, 1024, 3), dtype=np.float32).view(gloo.TextureCube)
texture.interpolation = gl.GL_LINEAR
texture[1] = data.get(abspath("Left_t4.png")) / 255.
texture[0] = data.get(abspath("Right_t4.png")) / 255.
texture[4] = data.get(abspath("Front_t4.png")) / 255.
texture[5] = data.get(abspath("Back_t4.png")) / 255.
texture[2] = data.get(abspath("Top_t4.png")) / 255.
texture[3] = data.get(abspath("Bottom_t4.png")) / 255.

model = np.eye(4, dtype=np.float32)
view = np.eye(4, dtype=np.float32)
print(view)
glm.translate(view, 0, 0, -5)
print(view)
glm.scale(model, 0.5, 1, 0.1)

program['texture'] = texture
program['u_model'] = model
program['u_view'] = view
program["u_light_position"] = 0, 2, -2
program["u_light_intensity"] = 2, 2, 2

phi = 1
theta = 0.1
beta = 0.5

app.run()
