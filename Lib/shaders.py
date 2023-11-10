"""
 Universidad del Valle de Guatemala
  Facultad de Ingenieria
  Departamento de Ciencia de la Computacion.
  Graficas por Computadora.
  Sección: 20

  OGL1: OGL1: 3D Models & Transforms

  @version 1.0
  @author Adrian Fulladolsa Palma | Carne 21592
"""

vertex_shader = """
    #version 450 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec2 texCoords;
    layout (location = 2) in vec3 normals;
    
    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
    
    out vec2 UVs;
    out vec3 normal;
    
    void main() {
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
        UVs = texCoords;
        normal = (modelMatrix * vec4(normals, 0.0)).xyz;
    }
"""

fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        fragColor = texture(tex, UVs);
    }
"""

gourad_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;

    uniform float lightIntensity;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;
        fragColor = texture(tex, UVs) * intensity;
    }
"""

cell_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    float rand(vec2 co) {
        return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
    }

    void main() {
        float edgeSens = 0.4 + 0.1 * sin(time + rand(UVs));
        float intensity = 0.85 + 0.15 * sin(time + rand(UVs));

        float gouraudIntensity = dot(normal, -dirLight) * lightIntensity;
        vec4 color = texture(tex, UVs) * gouraudIntensity;
        
        float gintensity = 0.2989 * color.r + 0.5870 * color.g + 0.1140 * color.b;
        
        if (gintensity > edgeSens) {
            fragColor = color;
        } else if (gintensity > intensity) {
            fragColor = vec4(0, 0, 0, 1);
        } else {
            fragColor = vec4(0, 0, 0, 1);
        }
    }

"""

multicolor_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;
        vec3 gradientColor = vec3(UVs.y + sin(time * normal.x), UVs.x + cos(time * normal.y), 1.0 - UVs.x + tan(time * normal.z));
        fragColor = vec4(gradientColor, 1.0) * intensity;
    }
"""

candy_cane_fragment_shader = """
    #version 450 core

layout (binding = 0) uniform sampler2D tex;

uniform vec3 dirLight;
uniform float lightIntensity;
uniform float time;

in vec2 UVs;
in vec3 normal;
out vec4 fragColor;

void main() {
    float intensity = dot(normal, -dirLight) * lightIntensity;
    vec4 color = texture(tex, UVs) * intensity;

    float gintensity = 0.2989 * color.r + 0.5870 * color.g + 0.1140 * color.b;
    float edgeSens = 0.4 + 0.1 * sin(time + sin(UVs.x * 12.9898 + UVs.y * 78.233) * 43758.5453);

    // Introduce a stronger glitch effect
    float glitchIntensity = sin(UVs.x * 12.9898 + UVs.y * 78.233 + time * 10.0) * 0.2; // Increase glitch amplitude
    if (gintensity > edgeSens) {
        fragColor = color + vec4(glitchIntensity, glitchIntensity, glitchIntensity, 0.0);
    } else {
        fragColor = vec4(0, 0, 0, 1);
    }
}
"""
glitch_vertex_shader = """
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 UVs;
out vec3 normal;

void main() {
    float time = 0.1 * float(gl_VertexID); // Time-based manipulation
    vec3 glitchOffset = vec3(
        sin(position.x + time) * 0.1, // Manipulate X position
        cos(position.y + time) * 0.1, // Manipulate Y position
        sin(position.z + time) * 0.1  // Manipulate Z position
    );

    vec4 distortedPosition = vec4(position + glitchOffset, 1.0);
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * distortedPosition;
    UVs = texCoords;
    normal = (modelMatrix * vec4(normals, 0.0)).xyz;
}
"""

color_shift_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;
        vec4 color = texture(tex, UVs) * intensity;

        float gintensity = 0.2989 * color.r + 0.5870 * color.g + 0.1140 * color.b;
        float edgeSens = 0.4 + 0.1 * sin(time + sin(UVs.x * 12.9898 + UVs.y * 78.233) * 43758.5453);

        // Introduce a color distortion
        float distortion = sin(time * 2.0) * 0.1; // Adjust the strength of color distortion
        color.r += distortion; // Manipulate the red channel
        color.g -= distortion; // Manipulate the green channel

        // Apply the glitch pattern based on luminance
        if (gintensity > edgeSens) {
            fragColor = color;
        } else {
            fragColor = vec4(0, 0, 0, 1);
        }
    }
"""

moving_vertex_shader = """
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

out vec2 UVs;
out vec3 normal;

void main() {
    mat4 rotationMatrix = mat4(
        cos(time), 0, sin(time), 0,
        0, 1, 0, 0,
        -sin(time), 0, cos(time), 0,
        0, 0, 0, 1
    );

    vec3 rotatedPosition = (rotationMatrix * vec4(position, 1.0)).xyz;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(rotatedPosition, 1.0);
    UVs = texCoords;
    normal = (modelMatrix * vec4(normals, 0.0)).xyz;
}
"""


