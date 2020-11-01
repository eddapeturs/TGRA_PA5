uniform sampler2D u_diff_tex;
uniform float u_opacity;
varying vec2 v_uv;

void main(void)
{
    vec4 color = texture2D(u_diff_tex, v_uv);
    float opacity = u_opacity;

    gl_FragColor = color;
}

