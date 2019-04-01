#version 440 core

uniform sampler2D draw_texture;
in vec2 TexCoord;

out vec4 fragColor;

void main() {
	fragColor = vec4(texture(draw_texture, TexCoord).rgb, 0.5);
}