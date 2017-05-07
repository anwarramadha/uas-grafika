# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo, data
from glumpy.geometry import colorcube
from glumpy.transforms import Trackball, Position
from os.path import abspath

vertex = """
uniform vec4 u_color;
attribute vec3 position;
attribute vec4 color;
attribute vec3 a_normal;
varying vec3 v_normal;
varying vec4 v_color;
varying vec3   v_texcoord;  // Interpolated fragment texture coordinates (out)
void main()
{
	v_normal = a_normal;
    v_color = u_color * color;
    v_texcoord = position;
    gl_Position = <transform>;
}
"""

fragment = """
varying vec4 v_color;
varying vec3      v_texcoord;        // Interpolated fragment texture coordinates (out)
varying vec3      v_normal;          // Interpolated normal (out)
uniform samplerCube u_texture;       // Texture
void main()
{
    vec3 lightsource = normalize(vec3(1,0.6,0.8)).xyz;
	float brightness = dot(v_normal, lightsource);
    vec4 v_color = textureCube(u_texture, v_texcoord);
    gl_FragColor = v_color*(0.7 + 0.5*brightness);
}
"""

window = app.Window(width=1024, height=1024,
                    color=(0.30, 0.30, 0.35, 1.00))

CUBES = []
VIO = []

# Upload the texture data
textures = []

for i in range(0, 2):
    texture = np.zeros((6,1024,1024,3),dtype=np.float32).view(gloo.TextureCube)
    texture.interpolation = gl.GL_LINEAR
    textures.append(texture)


textures[0][2] = data.get(abspath("FotoGedung/P_20170505_101510.jpg"))/255.
textures[0][3] = data.get(abspath("FotoGedung/P_20170505_101510.jpg"))/255.
textures[0][0] = data.get(abspath("FotoGedung/P_20170505_101510.jpg"))/255.
textures[0][1] = data.get(abspath("FotoGedung/P_20170505_101510.jpg"))/255.
textures[0][4] = data.get(abspath("FotoGedung/P_20170505_101510.jpg"))/255.
textures[0][5] = data.get(abspath("FotoGedung/P_20170505_101510.jpg"))/255.

textures[1][2] = data.get(abspath("FotoGedung/P_20170502_115905.jpg"))/255.
textures[1][3] = data.get(abspath("FotoGedung/P_20170502_115905.jpg"))/255.
textures[1][0] = data.get(abspath("FotoGedung/P_20170502_115905.jpg"))/255.
textures[1][1] = data.get(abspath("FotoGedung/P_20170502_115905.jpg"))/255.
textures[1][4] = data.get(abspath("FotoGedung/P_20170502_115905.jpg"))/255.
textures[1][5] = data.get(abspath("FotoGedung/P_20170502_115905.jpg"))/255.

def init_all_cubes(data):
    global window, CUBES, vertex, fragment

    for x, y, height, width in data:
        vertices, faces, outline = custom_cube(x, y, height, width)

        cube = gloo.Program(vertex, fragment)
        cube.bind(vertices)
        cube['transform'] = Trackball(Position("position"))
        window.attach(cube['transform'])
        CUBES.append(cube)
        VIO.append((vertices, faces, outline))
        # cube['u_texture'] = texture

def custom_cube(x, y, height, width):
    vertices, faces, outline = colorcube()
    for t in vertices['position']:
        t[0] += x
        # height
        if t[2] == 1:
            t[2] = height
        # width
        if t[1] == 1:
            t[1] = width
    print(vertices)
    return vertices, faces, outline

def color_all_cubes():
    global CUBES, VIO
    i = 0
    for index, cube in enumerate(CUBES):
        cube['u_texture'] = textures[i]
        # cube['texture'] = data_glumpy.get(abspath("lena.jpg"))/255.
        i+=1
        cube.draw(gl.GL_TRIANGLES, VIO[index][1])

@window.event
def on_draw(dt):
    window.clear()

    # Filled cube
    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    color_all_cubes()

    # Outlined cube
    # gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
    # gl.glEnable(gl.GL_BLEND)
    # gl.glDepthMask(gl.GL_FALSE)
    # cube['u_color'] = 0, 0, 0, 1
    # cube.draw(gl.GL_LINES, outline)
    # cube2['u_color'] = 0, 0, 0, 1
    # cube2.draw(gl.GL_LINES, outline)
    # gl.glDepthMask(gl.GL_TRUE)
@window.event
def on_key_press(key, modifiers):
    global phi, theta
    if key == app.window.key.UP:
        glm.translate(CUBES[0], 0, 0, 0.1)

# Build cube data
data = [
    (-2, 0, 1, 2),
    (1, 0, 2, 1)]
init_all_cubes(data)

#preparing normal
for idx, cube in enumerate(CUBES):
	cube['a_normal'] = [VIO[idx][0][i][2] for i in range(24)]

# OpenGL initalization
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glPolygonOffset(1, 1)
gl.glEnable(gl.GL_LINE_SMOOTH)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


# Run
app.run()
