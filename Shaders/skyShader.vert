attribute vec3 a_position; // Vertex position
attribute vec3 a_normal;	// Vertex normal
attribute vec2 a_uv; // For texture mapping

uniform mat4 u_model_matrix;
uniform mat4 u_projection_matrix;
uniform mat4 u_view_matrix;

varying vec2 v_uv;

void main(void)
{
	// Global coordinates
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	// Local coordinated
	position = u_model_matrix * position;

    v_uv = a_uv;

	gl_Position = u_projection_matrix * u_view_matrix * position;
}