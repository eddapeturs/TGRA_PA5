// layout (location = 0) out vec4 FragColor;
// layout (location = 1) out vec4 BrightColor; 
uniform sampler2D u_diff_tex;
uniform sampler2D u_spec_tex;
uniform sampler2D u_norm_tex;

uniform int u_has_diffuse;
uniform int u_has_specular;
uniform int u_has_normal;

struct Material {
    vec4 ambient;       // The color the surface reflects under ambient lighting (usually the same as the surface's color)
    vec4 diffuse;       // Color of surface under diffuse lighting
    vec4 specular;      // Reflect
    float shininess;
}; 

struct DirectionalLight {
    vec4 position;
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;
};

struct PointLight {
    vec4 position;
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;

    // Attenuation properties, combined 100%
    float constant;
    float linear; 
    float quadratic;
};

struct FlashLight {
    vec4  position;
    vec4  direction;
    float cutoff;
    float attenuation;
};    
  
// Initializing material and light structs 
uniform Material u_material;
uniform DirectionalLight u_light;
// uniform PointLight orb1;
// uniform PointLight orb2;
// uniform PointLight orb3;
// uniform PointLight orb4;
// uniform PointLight orb5;
uniform mat4 u_model_matrix;

uniform vec4 u_orb1_pos;
uniform vec4 u_orb2_pos;
uniform vec4 u_orb3_pos;
uniform vec4 u_orb4_pos;
uniform vec4 u_orb5_pos;
uniform vec4 u_orb6_pos;
uniform vec4 u_orb7_pos;

uniform int u_orb1_visible;
uniform int u_orb2_visible;
uniform int u_orb3_visible;
uniform int u_orb4_visible;
uniform int u_orb5_visible;
uniform int u_orb6_visible;
uniform int u_orb7_visible;

uniform PointLight orb;

uniform FlashLight u_flash;


// varying vec4 v_color;
varying vec4 v_position;
varying vec4 v_normal;
varying vec4 v_light;

uniform vec4 u_eye_position;

uniform vec4 u_light_position;
uniform vec4 u_light_diffuse;	// Diffuse of the light source
uniform vec4 u_light_specular;
uniform vec4 u_light_ambient;

uniform float u_opacity;

// // Orb light
// uniform vec4 orb1_light_diffuse;	// Diffuse of the light source
// uniform vec4 orb1_light_specular;	// Specular of the light source
// uniform vec4 orb1_light_ambient;	// Specular of the light source

// Material variables
// uniform vec4 u_mat_diffuse;
// uniform vec4 u_mat_specular;
// // The ambient material vector defines what color the surface reflects under ambient lighting; this is usually the same as the surface's color.
// uniform vec4 u_mat_ambient; // 
// uniform float u_mat_shiny;

// varying vec4 s;
// varying vec4 v;
// varying vec4 h;

// For orb calculations
varying vec4 orb1_s;
varying vec4 orb1_v;
varying vec4 orb1_h;

varying vec2 v_uv;

uniform vec4 u_fog_color;
uniform float u_fog_start;
uniform float u_fog_end;

// varying float lambert;
// varying float phong;

vec4 CalculateDirLight(float lambert, float phong, vec4 diff, vec4 spec);
vec4 CalculatePointLight(vec4 pos, PointLight orb);
vec4 CalculateFlashLight(float lambert, float phong, vec4 diff, vec4 spec);

void main(void)
{
    
    vec4 mat_diffuse = u_material.diffuse;
    vec4 mat_specular = u_material.specular;
    vec4 norm = normalize(v_normal);
    // float opacity = u_opacity;

    // Add texture if appropriate
    // Ath. gert a min 23.17 i vertex buffer objects vidjo
    if(u_has_diffuse == 1){
        mat_diffuse = texture2D(u_diff_tex, v_uv); // Returns a color
    }
    if(u_has_specular == 1){
        mat_specular *= texture2D(u_spec_tex, v_uv); // Returns a color
    }
    if(u_has_normal == 1){
        // norm *= texture2D(u_norm_tex, v_uv);
        norm += texture2D(u_norm_tex, v_uv);
        // norm = normalize(norm * 2.0 - 1.0);
        // norm = normalize(texture2D(u_norm_tex, v_uv) * 2.0 - 1.0);
    }

    norm = normalize(norm);

	vec4 s = normalize(u_light_position - v_position);
    vec4 v = normalize(u_eye_position - v_position);
	vec4 h = normalize(s + v);

    float lambert = max(dot(norm, s), 0.0);
	float phong = max(dot(norm, h), 0.0);
    
    // vec4 dirColor = CalculateDirLight(lambert, phong, mat_diffuse, mat_specular);
    vec4 dirColor = CalculateFlashLight(lambert, phong, mat_diffuse, mat_specular);

    vec4 orb1_color = vec4(0.0);
    vec4 orb2_color = vec4(0.0);
    vec4 orb3_color = vec4(0.0);
    vec4 orb4_color = vec4(0.0);
    vec4 orb5_color = vec4(0.0);
    vec4 orb6_color = vec4(0.0);
    vec4 orb7_color = vec4(0.0);

    if(u_orb1_visible == 1){ orb1_color = CalculatePointLight(u_orb1_pos, orb); }
    if(u_orb2_visible == 1){ orb2_color = CalculatePointLight(u_orb2_pos, orb); }
    if(u_orb3_visible == 1){ orb3_color = CalculatePointLight(u_orb3_pos, orb); }
    if(u_orb4_visible == 1){ orb4_color = CalculatePointLight(u_orb4_pos, orb); }
    if(u_orb5_visible == 1){ orb5_color = CalculatePointLight(u_orb5_pos, orb); }
    if(u_orb6_visible == 1){ orb6_color = CalculatePointLight(u_orb6_pos, orb); }
    if(u_orb7_visible == 1){ orb7_color = CalculatePointLight(u_orb7_pos, orb); }
    

    vec4 color  = dirColor 
                + orb1_color 
                + orb2_color 
                + orb3_color
                + orb4_color
                + orb5_color
                + orb6_color
                + orb7_color;
    
    float fogDistance = length(u_eye_position - v_position);
    float fogAmount = smoothstep(u_fog_start, u_fog_end, fogDistance);
    // float fogAmount = smoothstep(10.0, 20.0, fogDistance);

    // vec4 flashLight = CalculateFlashLight();
    
    // gl_FragColor = color;
    gl_FragColor = color;
    gl_FragColor.a = u_opacity;
    // gl_FragColor.a = 0.1;
    // gl_FragColor = norm;
    // gl_FragColor = mix(color, u_fog_color, fogAmount);
}


vec4 CalculateDirLight(float lambert, float phong, vec4 diff, vec4 spec)
{
    vec4 color = u_light_ambient * u_material.ambient
                + u_light_diffuse * diff * lambert
                + u_light_specular * spec * pow(phong, u_material.shininess);
    return color;
}

vec4 CalculatePointLight(vec4 pos, PointLight orb)
{
    vec4 o_s = pos - v_position;    // Distance from light source to fragment
    vec4 o_v = normalize(u_eye_position - v_position);  // Eye to 
	vec4 o_h = normalize(o_s + o_v);

    float o_lambert = max(dot(v_normal, normalize(o_s)), 0.0);
    float o_phong = max(dot(v_normal, o_h), 0.0);

    vec4 o_ambi = orb.ambient * u_material.ambient;
    vec4 o_diff = orb.diffuse * u_material.diffuse * o_lambert;
    vec4 o_spec = orb.specular * u_material.specular * pow(o_phong, u_material.shininess);

    // Actual distance from light to v
    float dist = length(o_s);
    float attenuation = 1.0 / (orb.constant + orb.linear * dist + orb.quadratic * (dist * dist ));

    o_ambi *= attenuation;
    o_diff *= attenuation;
    o_spec *= attenuation;
    vec4 orb_color = o_ambi + o_diff + o_spec;
    return orb_color;
}

vec4 CalculateFlashLight(float lambert, float phong, vec4 diff, vec4 spec)
{
    vec4 lightDir = normalize(u_flash.position - v_position); // S
    vec4 spotDir = normalize(-u_flash.direction);
    vec4 rayDir = -lightDir;
    float theta = dot(rayDir, spotDir);
    float lightAttenuation = u_flash.attenuation;
    float lightLen = length(lightDir);

    vec4 color;
    if(theta > u_flash.cutoff){
        lightAttenuation = 0.0;
    }

    color = u_light_ambient * u_material.ambient
            + u_light_diffuse * diff * lambert
            + u_light_specular * spec * pow(phong, u_material.shininess);
    
    float attenuation = 1.0 / (1.0 + lightAttenuation * (lightLen * lightLen));

    return color * attenuation;
}

