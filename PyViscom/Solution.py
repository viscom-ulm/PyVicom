import glm

def index(coord, res):
    return int(res[0] * res[1] * coord[2] + res[0] * coord[1] + coord[0])


def get_vec4(data, idx, data_dim):
    val = glm.vec4(data[idx])
    for i in range(1, data_dim):
        val[i] = data[idx + i]
    return val


def uniform_grid_volume_get_linear(data, coord, res, data_dim):
    if len(data) <= 0:
        return glm.vec4(0.0)
    # Clamp to nearly one to avoid issus
    c = glm.clamp(coord, 0.0, 0.9999)
    p = glm.floor(c * glm.vec3(res - 1))
    cc = glm.fract(c * glm.vec3(res - 1))

    # Get all samples
    v000 = get_vec4(data, index(p + glm.vec3(0, 0, 0), res) * data_dim, data_dim)
    v100 = get_vec4(data, index(p + glm.vec3(1, 0, 0), res) * data_dim, data_dim)
    v010 = get_vec4(data, index(p + glm.vec3(0, 1, 0), res) * data_dim, data_dim)
    v110 = get_vec4(data, index(p + glm.vec3(1, 1, 0), res) * data_dim, data_dim)
    v001 = get_vec4(data, index(p + glm.vec3(0, 0, 1), res) * data_dim, data_dim)
    v101 = get_vec4(data, index(p + glm.vec3(1, 0, 1), res) * data_dim, data_dim)
    v011 = get_vec4(data, index(p + glm.vec3(0, 1, 1), res) * data_dim, data_dim)
    v111 = get_vec4(data, index(p + glm.vec3(1, 1, 1), res) * data_dim, data_dim)

    # Interpolate x
    v00 = glm.mix(v000, v100, cc[0])
    v01 = glm.mix(v010, v110, cc[0])
    v10 = glm.mix(v001, v101, cc[0])
    v11 = glm.mix(v011, v111, cc[0])

    # Interpolate y
    v0 = glm.mix(v00, v01, cc[1])
    v1 = glm.mix(v10, v11, cc[1])

    # Interpolate z
    v = glm.mix(v0, v1, cc[2])
    return v
