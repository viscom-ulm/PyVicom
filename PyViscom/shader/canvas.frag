#version 440 core

uniform sampler2D draw_texture;
in vec2 TexCoord;

out vec4 fragColor;

void main() {
	fragColor = texture(draw_texture, TexCoord).rgba;
}