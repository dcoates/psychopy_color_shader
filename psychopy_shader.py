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

siz = (256,256)

noise = np.random.uniform(0, 1, siz)

noise_tex = psychopy.visual.GratingStim(
    win=win,
    tex=noise,
    mask=None,
    size=siz
)

shader_frag_new = '''
    uniform sampler2D texture,mask;
    uniform float test_u;
    void main() {
        vec4 textureFrag = texture2D(texture,gl_TexCoord[0].st);
        vec4 maskFrag = texture2D(mask,gl_TexCoord[1].st);
        float color1 = (textureFrag.r*(gl_Color.r*2.0-1.0)+1.0)/2.0;
        gl_FragColor.rgb = vec3(color1,0.0,test_u);
        gl_FragColor.a = gl_Color.a * textureFrag.a * 1.0;
    }
    '''

program_new = psychopy.visual.shaders.compileProgram(
    vertexSource=shaders.vertSimple,
    fragmentSource=shader_frag_new
)

phase = 0.0

frames_per_cycle = 100

phase_inc = 1.0 / frames_per_cycle

noise_tex.color = 1.0

keep_going = True


# Replace the shader for the grating with our own custom shader (defined above)
# updateList() changes the OpenGL Display List that is executed in Draw()
# Not sure why this must be called twice... ?
win._progSignedTexMask = program_new
noise_tex._updateList()
win._progSignedTexMask = program_new
noise_tex._updateList()
win._progSignedTexMask = default_shader

# Can do this anytime, but only need to do once:
loc=GL.glGetUniformLocation(program_new,b'test_u');

while keep_going: 

    noise_tex.draw()

    win.flip()

    keys = psychopy.event.getKeys()

    keep_going = ("q" not in keys)

    # Modulate the "phase" variable between 0 and 1
    phase = np.mod(phase + phase_inc, 1)

    # shouldn't need to rebuild the OpenGL list when we change a parameter like color
    # This confirms that. (rebuilding the list may take time)
    noise_tex.color = 0.75
    noise_tex._needUpdate = False 

    GL.glProgramUniform1f(program_new,loc, phase)


win.close()

