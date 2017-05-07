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
varying vec4 v_color;
varying vec3   v_texcoord;  // Interpolated fragment texture coordinates (out)
void main()
{
    v_color = u_color * color;
    v_texcoord = position;
    gl_Position = <transform>;
}
"""

fragment = """
varying vec4 v_color;
varying vec3      v_texcoord;        // Interpolated fragment texture coordinates (out)
uniform samplerCube u_texture;       // Texture
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
    texture = np.zeros((6,1024,1024,3),dtype=np.float32).view(gloo.TextureCube)
    texture.interpolation = gl.GL_LINEAR
    for j in range(0, 6):
        try:
            texture[j] = data.get(abspath(GEDUNG[i]))/255.
        except:
            print(GEDUNG[i])
    textures.append(texture)

def init_all_cubes(data):
    global window, CUBES, vertex, fragment

    for x, y, height, width, length in data:
        vertices, faces, outline = custom_cube(x/92, y/15, height, width/34)

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
        if t[0] == 1:
            t[0] = x
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

data = []
with open("datagedung.txt") as f:
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

print(data)
init_all_cubes(data)

# OpenGL initalization
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glPolygonOffset(1, 1)
gl.glEnable(gl.GL_LINE_SMOOTH)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


# Run
app.run()
