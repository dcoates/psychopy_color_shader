// Minimal shader for testing that uses a uniform for the blue
// channel, and just the red from the input texture

uniform sampler2D texture,mask;
uniform float test_u;
void main() {
	vec4 textureFrag = texture2D(texture,gl_TexCoord[0].st);
	vec4 maskFrag = texture2D(mask,gl_TexCoord[1].st);
	float color1 = (textureFrag.r*(gl_Color.r*2.0-1.0)+1.0)/2.0;
	gl_FragColor.rgb = vec3(color1,0.0,test_u);
	gl_FragColor.a = gl_Color.a * textureFrag.a * 1.0;
}
