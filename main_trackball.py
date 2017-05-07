# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo, data as data_glumpy
from glumpy.geometry import colorcube
from glumpy.transforms import Trackball, Position
from os.path import abspath

vertex = """
uniform vec4 u_color;
attribute vec3 position;
attribute vec4 color;
varying vec4 v_color;
void main()
{
    v_color = u_color * color;
    gl_Position = <transform>;
}
"""

fragment = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
}
"""

window = app.Window(width=1024, height=1024,
                    color=(0.30, 0.30, 0.35, 1.00))

CUBES = []
VIO = []

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
    for index, cube in enumerate(CUBES):
        cube['u_color'] = 1, 1, 1, 1
        # cube['texture'] = data_glumpy.get(abspath("lena.jpg"))/255.
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

# OpenGL initalization
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glPolygonOffset(1, 1)
gl.glEnable(gl.GL_LINE_SMOOTH)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


# Run
app.run()
