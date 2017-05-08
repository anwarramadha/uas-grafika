# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo, data
from glumpy.geometry import colorcube
from glumpy.transforms import Trackball, Position, PanZoom
from os.path import abspath

vertex = """
uniform vec4 u_color;
uniform mat4      view;            // View matrix
attribute vec3 position;
attribute vec4 color;
varying vec4 v_color;
varying vec3   v_texcoord;  // Interpolated fragment texture coordinates (out)
void main()
{
    v_color = u_color * color;
    v_texcoord = position;
    gl_Position = view * <transform>;
}
"""

fragment = """
varying vec4 v_color;
varying vec3      v_texcoord;        // Interpolated fragment texture coordinates (out)
uniform samplerCube u_texture;       // Texture
uniform mat4      view;            // View matrix
void main()
{

    vec4 v_color = textureCube(u_texture, v_texcoord);
    gl_FragColor = v_color;
}
"""

window = app.Window(width=1024, height=1024,
                    color=(0.30, 0.30, 0.35, 1.00))

CUBES = []
VIO = []
GEDUNG = ['Building/P_20170505_102534.jpg', 'Building/P_20170505_102404.jpg', 'Building/P_20170505_105104.jpg',
            'Building/P_20170505_102534.jpg', 'Building/P_20170505_104051_PN.jpg', 'Building/P_20170505_105218.jpg',
            'Building/P_20170505_105218.jpg', 'Building/P_20170505_104519_PN.jpg', 'Building/P_20170505_104519_PN.jpg',
            'Building/P_20170505_104051_PN.jpg', 'Building/P_20170505_104051_PN.jpg', 'Building/P_20170505_104051_PN.jpg',
            'Building/P_20170505_103947_PN.jpg', 'Building/P_20170505_104051_PN.jpg', 'Building/P_20170505_104739_PN_2.jpg',
            'Building/P_20170505_104739_PN_3.jpg', 'Building/P_20170505_104739_PN_3.jpg', 'Building/P_20170505_102705.jpg',
            'Building/P_20170505_103244.jpg', 'Building/P_20170505_103227_PN.jpg', 'Building/P_20170505_102705.jpg',
            'Building/P_20170505_102404.jpg', 'Building/P_20170505_102534.jpg', 'Building/P_20170505_102404.jpg',
            'Building/P_20170505_102534.jpg', 'Building/P_20170505_102534.jpg', 'Building/P_20170505_104739_PN_3.jpg',
            'Building/P_20170505_104739_PN_3.jpg', 'Building/P_20170505_102404.jpg', 'Building/P_20170505_105333.jpg',
            'Building/P_20170505_105218.jpg','Building/P_20170505_105218.jpg', 'Building/P_20170505_105218.jpg',
            'Building/P_20170505_104739_PN_3.jpg', 'Building/P_20170505_103244.jpg', 'Building/P_20170505_103207.jpg',
            'Building/P_20170505_104739_PN_3.jpg', 'Building/P_20170505_104739_PN_3.jpg']
# Upload the texture data
textures = []

for i in range(0, 38):
    texture = np.zeros((6, 1024, 1024, 3), dtype=np.float32).view(gloo.TextureCube)
    texture.interpolation = gl.GL_LINEAR
    for j in range(0, 6):
        try:
            texture[j] = data.get(abspath(GEDUNG[i]))/255.
        except:
            print(GEDUNG[i])
    textures.append(texture)

view = np.eye(4, dtype=np.float32)
def init_all_cubes(data):
    global window, CUBES, vertex, fragment

    for x, y, height, width, length in data:
        vertices, faces, outline = custom_cube(x, y, height, width)

        cube = gloo.Program(vertex, fragment)
        cube.bind(vertices)
        cube['transform'] = Trackball(Position("position"))
        cube['view'] = view
        window.attach(cube['transform'])
        CUBES.append(cube)
        VIO.append((vertices, faces, outline))
        # cube['u_texture'] = texture

def custom_cube(x, y, height, width):
    vertices, faces, outline = colorcube()
    for t in vertices['position']:
        t[0] += x
        t[1] += y
        # height
        # if t[2] == 1:
        #     t[2] = height
        # # width
        # if t[1] == 1:
        #     t[1] = width

    print(vertices)
    return vertices, faces, outline


def color_all_cubes():
    global CUBES, VIO
    j = 0
    for index, cube in enumerate(CUBES):
        cube['u_texture'] = textures[j]
        j += 1
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


zoom = PanZoom(Position("position"), aspect=1, zoom=1)

@window.event
def on_key_press(key, modifiers):
    global phi, theta
    if key == app.window.key.UP:
        for cube in CUBES:
            glm.translate(view, 0, -0.01, 0)
            cube['view'] = view
    if key == app.window.key.DOWN:
        for cube in CUBES:
            glm.translate(view, 0, 0.01, 0)
            cube['view'] = view
    if key == app.window.key.LEFT:
        for cube in CUBES:
            glm.translate(view, 0.01, 0, 0)
            cube['view'] = view
    if key == app.window.key.RIGHT:
        for cube in CUBES:
            glm.translate(view, -0.01, 0, 0)
            cube['view'] = view
    if key == 87:
        for cube in CUBES:
            glm.translate(view, 0, 0, 0.01)
            cube['view'] = view
    if key == 83:
        for cube in CUBES:
            glm.translate(view, 0, 0, -0.01)
            cube['view'] = view


# Build cube data

data = []
with open("data_gedung_2.txt") as f:
	idxLine = 5
	tup = []
	for line in f:
		if (idxLine == 5):
			idxLine = 0
			if tup:
				data.append(tuple(tup))
				del tup[:]
		else:
			idxLine = idxLine + 1
			tup.append(float(line))

	if tup:
		data.append(tuple(tup))
		del tup[:]

init_all_cubes(data)

# preparing normal
# for idx, cube in enumerate(CUBES):
    # cube['a_normal'] = [VIO[idx][0][i][2] for i in range(24)]

# OpenGL initialization
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glPolygonOffset(1, 1)
gl.glEnable(gl.GL_LINE_SMOOTH)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

# Run
app.run()
