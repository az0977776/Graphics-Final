def calculate_normal( ax, ay, az, bx, by, bz ):
    normal = [0,0,0]
    normal[0] = ay * bz - az * by
    normal[1] = az * bx - ax * bz
    normal[2] = ax * by - ay * bx
    return normal

def light_normal( points, i ):
    ax = points[i + 1][0] - points[ i ][0]
    ay = points[i + 1][1] - points[ i ][1]
    az = points[i + 1][2] - points[ i ][2]

    bx = points[i + 2][0] - points[ i ][0]
    by = points[i + 2][1] - points[ i ][1]
    bz = points[i + 2][2] - points[ i ][2]

    normal = calculate_normal( ax, ay, az, bx, by, bz )

    return normal

def dot_product(v0, v1):
    return v0[0] * v1[0] + v0[1] * v1[1] + v0[2] * v1[2]

def scalar_product(v, s):
    a = vector[0] * scalar
    b = vector[1] * scalar
    c = vector[2] * scalar
    return [a,b,c]

def normal(v):
    magnitude = sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    if magnitude == 0:
        return 0
    a = v[0]/magnitude
    b = v[1]/magnitude
    c = v[2]/magnitude
    return [a,b,c]


def vector_subtract(v0, v1):
    a = v0[0] - v1[0]
    b = v0[1] - v1[1]
    c = v0[2] - v2[2]
    return [a,b,c]

def calculate_dot( points, i ):
    ax = points[i + 1][0] - points[ i ][0]
    ay = points[i + 1][1] - points[ i ][1]
    az = points[i + 1][2] - points[ i ][2]

    bx = points[i + 2][0] - points[ i ][0]
    by = points[i + 2][1] - points[ i ][1]
    bz = points[i + 2][2] - points[ i ][2]

    normal = calculate_normal( ax, ay, az, bx, by, bz )

    vx = 0
    vy = 0
    vz = -1

    dot = normal[0] * vx + normal[1] * vy + normal[2] * vz

    return dot
