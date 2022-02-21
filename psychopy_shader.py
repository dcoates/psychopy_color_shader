# Ideas taken from this on PsychoPy forum:
# https://discourse.psychopy.org/t/change-color-of-each-pixel-as-a-function-of-frame/2538/3 
# (But needed update to work in latest PsychoPy)

import numpy as np

import psychopy.visual
import psychopy.event
#import shaders # Local local of psychopy.visual.shaders
import psychopy.visual.shaders
import psychopy.visual.shaders as shaders

import pyglet

from psychopy.colors import Color

win = psychopy.visual.Window(
    size=(1920, 1080),
    fullscr=True,
    units="pix"
)

GL = win.backend.GL # Get the OpenGL instance from PsychoPy 

default_shader = win._progSignedTexMask

siz = (1024,1024)

xvals=np.linspace(0,1,siz[0])
yvals=xvals*0

grid_x,grid_y=np.meshgrid(xvals,yvals)

#texture_bits = np.random.uniform(0, 1, siz)
texture_bits = grid_x

texture = psychopy.visual.GratingStim(
    win=win,
    tex=texture_bits,
    mask=None,
    size=siz
)

shader_frag_new = open('fragment_simple.c').readlines()

program_new = psychopy.visual.shaders.compileProgram(
    vertexSource=shaders.vertSimple,
    fragmentSource=shader_frag_new
)

phase = 0.0

frames_per_cycle = 100

phase_inc = 1.0 / frames_per_cycle

texture.color = 1.0

keep_going = True


# Replace the shader for the grating with our own custom shader (defined above)
# updateList() changes the OpenGL Display List that is executed in Draw()
# Not sure why this must be called twice... ?
win._progSignedTexMask = program_new
texture._updateList()
win._progSignedTexMask = program_new
texture._updateList()
win._progSignedTexMask = default_shader

# Can do this anytime, but only need to do once:
loc=GL.glGetUniformLocation(program_new,b'test_u');

modulate=True

while keep_going: 

    texture.draw()

    win.flip()

    keys = psychopy.event.getKeys()

    keep_going = ("q" not in keys)

    modulate = not(modulate) if ('m' in keys) else modulate

    # Modulate the "phase" variable between 0 and 1
    if modulate:
        phase = np.mod(phase + phase_inc, 1)

    # shouldn't need to rebuild the OpenGL list when we change a parameter like color
    # This confirms that. (rebuilding the OpenGL list may take time)
    texture.color = 0.75
    texture._needUpdate = False 

    GL.glProgramUniform1f(program_new,loc, phase)


win.close()

