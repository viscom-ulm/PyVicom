#version 440 core

layout(location = 0) in vec3 pos;
layout (location = 1) in vec2 texCoord;

uniform mat4 P;
uniform mat4 V;
uniform mat4 M;

out vec2 TexCoord;

void main() {
	TexCoord = texCoord;
	gl_Position = P * V * M * vec4(pos, 1.0);
}