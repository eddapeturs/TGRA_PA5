attribute vec3 a_position; // Vertex position
attribute vec3 a_normal;	// Vertex normal
attribute vec2 a_uv; // For texture mapping

// Uniform variable - a variable we can change the values of anytime (bf or after drawing)
// mat4 = 4 by 4 matrix
uniform mat4 u_model_matrix;
uniform mat4 u_projection_matrix;
uniform mat4 u_view_matrix;

// uniform vec4 u_color;
// uniform vec4 u_eye_position;

// Main light position
uniform vec4 u_light_position;  // Position of the light, in global coordinations when they are sent in
uniform vec4 u_light_diffuse;	// Diffuse of the light source
uniform vec4 u_light_specular;	// Specular of the light source
uniform vec4 u_light_ambient;	// Specular of the light source
// uniform DirectionalLight u_light;

// uniform vec4 orb1_light_position;  // Position of the light, in global coordinations when they are sent in

// uniform PointLight orb1;

// These will be passed into the fragment shader
varying vec4 v_color;  //Leave the varying variables alone to begin with
varying vec4 v_position;
varying vec4 v_light;
varying vec4 v_normal;

uniform int u_has_diffuse;
uniform int u_has_specular;
uniform int u_has_normal;

varying vec2 v_uv;
// varying vec4 v_s;
// varying vec4 v_h;

uniform vec4 u_fog_color;
// uniform vec4 u_fog_start;
// uniform vec4 u_fog_end;

// varying vec4 v_normal;

void main(void)
{
	// Global coordinates
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	// Local coordinated
	position = u_model_matrix * position;
	v_position = position;

	normal = u_model_matrix * normal; // Maybe normalize this, question about optimization
	v_normal = normalize(normal);

	if(u_has_diffuse == 1){
		v_uv = a_uv;
	}

	gl_Position = u_projection_matrix * u_view_matrix * position;

	// v_s = normalize(u_light_position - v_position);
    // v = normalize(u_eye_position - v_position);
	// vec4 h = normalize(s + v);
}