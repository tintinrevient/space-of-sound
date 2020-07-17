var bin_frag = 
`
uniform float u_red;
uniform float u_green;
uniform float u_blue;

void main() {

	gl_FragColor = vec4(u_red, u_green + 0.5, u_blue, 1.0);

}
`