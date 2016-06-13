from display import *
from matrix import *
from gmath import calculate_dot
from math import cos, sin, pi

MAX_STEPS = 100

def add_polygon( points, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point( points, x0, y0, z0 )
    add_point( points, x1, y1, z1 )
    add_point( points, x2, y2, z2 )
    
def draw_polygons( points, screen, color ):

    if len(points) < 3:
        print 'Need at least 3 points to draw a polygon!'
        return

    p = 0
    while p < len( points ) - 2:

        if calculate_dot( points, p ) < 0:
            draw_line( screen, points[p][0], points[p][1],
                       points[p+1][0], points[p+1][1], color )
            draw_line( screen, points[p+1][0], points[p+1][1],
                       points[p+2][0], points[p+2][1], color )
            draw_line( screen, points[p+2][0], points[p+2][1],
                       points[p][0], points[p][1], color )
        p+= 3


def zdraw_polygons( points, screen, color, zbuffer, lightsources ):

    if len(points) < 3:
        print 'Need at least 3 points to draw a polygon!'
        return

    p = 0
    while p < len( points ) - 2:

        if calculate_dot( points, p ) < 0:
            #color = lighting(color, light_normal(points, p), lightsources)

            zdraw_line( screen, points[p][0], points[p][1], points[p][2],
                       points[p+1][0], points[p+1][1], points[p+1][2], color, zbuffer )

            zdraw_line( screen, points[p+1][0], points[p+1][1], points[p+1][2],
                       points[p+2][0], points[p+2][1], points[p+2][2], color, zbuffer )

            zdraw_line( screen, points[p+2][0], points[p+2][1], points[p+2][2],
                       points[p][0], points[p][1],  points[p][2], color, zbuffer )

            scanline_conversion([points[p], points[p + 1], points[p + 2]], screen, color, zbuffer)
        p+= 3

def lighting( color, normal, lightsource ):
    ambient = color
    diffuse = [0, 0, 0]
    specular = [0, 0, 0]
    for source in lightsource:
        if (source[0] == "diffuse"):
            pass
        if (source[0] == "specular"):
            pass
    return [ambient[0] + diffuse[0] + specular[0], ambient[1] + diffuse[1] + specular[1], ambient[2] + diffuse[2] + specular[2]]

        
def scanline_conversion(points, screen, color, zbuffer):
    if len(points) < 3:
        print 'Need at least 3 points to fill'
    p = 0
    while p < len(points)-2:
        points = sorted(points,key=lambda x:x[1])
        
        counter = 0
        pb = points[p]
        pm = points[p+1]
        pt = points[p+2]

        tx = pt[0]
        ty = pt[1]
        tz = pt[2]
        mx = pm[0]
        my = pm[1]
        mz = pm[2]
        bx = pb[0]
        by = pb[1]
        bz = pb[2]

        d1 = 1
        dz1 = 1
        d2 = 1
        dz2 = 1
        
        if (my != ty):
            d1 = (mx - tx) / (my - ty)
            dz1 = (mz - tz) / (my - ty)
        if (by != my):
            d2 = (bx - mx) / (by - my)
            dz2 = (bz - mz) / (by - my)
        
        d0 = (tx - bx)/(ty - by)
        dz0 = (tz - bz)/(ty - by)
            
        while by + counter < ty:

            newx0 = tx + counter * d0
            newy = ty + counter
            newz = tz + counter * dz0
            if (newy < my):
                newx1 = tx + counter * d1
                newz1 = tz + counter * dz1
            else:
                newx1 = mx + (newy - my) * d2
                newz1 = mz + (newy - my) * dz2

            zdraw_line( screen, newx0, newy, newz, newx1, newy, newz1, color, zbuffer)

            counter += 1
            
        p+=3
            
def add_box( points, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon( points, 
                 x, y, z, 
                 x, y1, z,
                 x1, y1, z)
    add_polygon( points, 
                 x1, y1, z, 
                 x1, y, z,
                 x, y, z)
    #back
    add_polygon( points, 
                 x1, y, z1, 
                 x1, y1, z1,
                 x, y1, z1)
    add_polygon( points, 
                 x, y1, z1, 
                 x, y, z1,
                 x1, y, z1)
    #top
    add_polygon( points, 
                 x, y, z1, 
                 x, y, z,
                 x1, y, z)
    add_polygon( points, 
                 x1, y, z, 
                 x1, y, z1,
                 x, y, z1)
    #bottom
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y1, z,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y1, z1,
	         x1, y1, z1)
    #right side
    add_polygon( points, 
                 x1, y, z, 
                 x1, y1, z,
                 x1, y1, z1)
    add_polygon( points, 
                 x1, y1, z1, 
                 x1, y, z1,
                 x1, y, z)
    #left side
    add_polygon( points, 
                 x, y, z1, 
                 x, y1, z1,
                 x, y1, z)
    add_polygon( points, 
                 x, y1, z, 
                 x, y, z,
                 x, y, z1) 


def add_sphere( points, cx, cy, cz, r, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_sphere( temp, cx, cy, cz, r, step )
    num_points = len( temp )

    lat = 0
    lat_stop = num_steps
    longt = 0
    longt_stop = num_steps

    num_steps += 1

    while lat < lat_stop:
        longt = 0
        while longt < longt_stop:
            
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]
            
            if longt != longt_stop - 1:
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]
            else:
                px2 = temp[ (index + 1) % num_points ][0]
                py2 = temp[ (index + 1) % num_points ][1]
                pz2 = temp[ (index + 1) % num_points ][2]
                
            px3 = temp[ index + 1 ][0]
            py3 = temp[ index + 1 ][1]
            pz3 = temp[ index + 1 ][2]
      
            if longt != 0:
                add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 )

            if longt != longt_stop - 1:
                add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 )
            
            longt+= 1
        lat+= 1

def generate_sphere( points, cx, cy, cz, r, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle <= circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = r * cos( pi * circ ) + cx
            y = r * sin( pi * circ ) * cos( 2 * pi * rot ) + cy
            z = r * sin( pi * circ ) * sin( 2 * pi * rot ) + cz
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step

def add_torus( points, cx, cy, cz, r0, r1, step ):
    
    num_steps = MAX_STEPS / step
    temp = []

    generate_torus( temp, cx, cy, cz, r0, r1, step )
    num_points = len(temp)

    lat = 0
    lat_stop = num_steps
    longt_stop = num_steps
    
    while lat < lat_stop:
        longt = 0

        while longt < longt_stop:
            index = lat * num_steps + longt

            px0 = temp[ index ][0]
            py0 = temp[ index ][1]
            pz0 = temp[ index ][2]

            px1 = temp[ (index + num_steps) % num_points ][0]
            py1 = temp[ (index + num_steps) % num_points ][1]
            pz1 = temp[ (index + num_steps) % num_points ][2]

            if longt != num_steps - 1:            
                px2 = temp[ (index + num_steps + 1) % num_points ][0]
                py2 = temp[ (index + num_steps + 1) % num_points ][1]
                pz2 = temp[ (index + num_steps + 1) % num_points ][2]

                px3 = temp[ (index + 1) % num_points ][0]
                py3 = temp[ (index + 1) % num_points ][1]
                pz3 = temp[ (index + 1) % num_points ][2]
            else:
                px2 = temp[ ((lat + 1) * num_steps) % num_points ][0]
                py2 = temp[ ((lat + 1) * num_steps) % num_points ][1]
                pz2 = temp[ ((lat + 1) * num_steps) % num_points ][2]

                px3 = temp[ (lat * num_steps) % num_points ][0]
                py3 = temp[ (lat * num_steps) % num_points ][1]
                pz3 = temp[ (lat * num_steps) % num_points ][2]


            add_polygon( points, px0, py0, pz0, px1, py1, pz1, px2, py2, pz2 );
            add_polygon( points, px2, py2, pz2, px3, py3, pz3, px0, py0, pz0 );        
            
            longt+= 1
        lat+= 1


def generate_torus( points, cx, cy, cz, r0, r1, step ):

    rotation = 0
    rot_stop = MAX_STEPS
    circle = 0
    circ_stop = MAX_STEPS

    while rotation < rot_stop:
        circle = 0
        rot = float(rotation) / MAX_STEPS
        while circle < circ_stop:
            
            circ = float(circle) / MAX_STEPS
            x = (cos( 2 * pi * rot ) *
                 (r0 * cos( 2 * pi * circ) + r1 ) + cx)
            y = r0 * sin(2 * pi * circ) + cy
            z = (sin( 2 * pi * rot ) *
                 (r0 * cos(2 * pi * circ) + r1))
            
            add_point( points, x, y, z )

            circle+= step
        rotation+= step



def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy

    t = step
    while t<= 1:
        
        x = r * cos( 2 * pi * t ) + cx
        y = r * sin( 2 * pi * t ) + cy

        add_edge( points, x0, y0, cz, x, y, cz )
        x0 = x
        y0 = y
        t+= step
    add_edge( points, x0, y0, cz, cx + r, cy, cz )

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    xcoefs = generate_curve_coefs( x0, x1, x2, x3, curve_type )
    ycoefs = generate_curve_coefs( y0, y1, y2, y3, curve_type )
        
    t =  step
    while t <= 1:
        
        x = xcoefs[0][0] * t * t * t + xcoefs[0][1] * t * t + xcoefs[0][2] * t + xcoefs[0][3]
        y = ycoefs[0][0] * t * t * t + ycoefs[0][1] * t * t + ycoefs[0][2] * t + ycoefs[0][3]

        add_edge( points, x0, y0, 0, x, y, 0 )
        x0 = x
        y0 = y
        t+= step

def draw_lines( matrix, screen, color ):
    if len( matrix ) < 2:
        print "Need at least 2 points to draw a line"
        
    p = 0
    while p < len( matrix ) - 1:
        draw_line( screen, matrix[p][0], matrix[p][1],
                   matrix[p+1][0], matrix[p+1][1], color )
        p+= 2

def zdraw_lines( matrix, screen, color, zbuffer ):
    if len( matrix ) < 2:
        print "Need at least 2 points to draw a line"

    p = 0
    while p < len( matrix ) - 1:
        zdraw_line( screen, matrix[p][0], matrix[p][1], matrix[p][2],
                   matrix[p+1][0], matrix[p+1][1], matrix[p+1][2], color, zbuffer )
        p+= 2


def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point( matrix, x0, y0, z0 )
    add_point( matrix, x1, y1, z1 )

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )


def draw_line( screen, x0, y0, x1, y1, color ):
    dx = x1 - x0
    dy = y1 - y0
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
    
    if dx == 0:
        y = y0
        while y <= y1:
            plot(screen, color,  x0, y)
            y = y + 1
    elif dy == 0:
        x = x0
        while x <= x1:
            plot(screen, color, x, y0)
            x = x + 1
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, x, y)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            d = d - dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, x, y)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            d = d - dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        while x <= x1:
            plot(screen, color, x, y)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            d = d + dy
    else:
        d = 0
        x = x0
        y = y0
        while y <= y1:
            plot(screen, color, x, y)
            if d > 0:
                x = x + 1
                d = d - dy
            y = y + 1
            d = d + dx

def zdraw_line( screen, x0, y0, z0, x1, y1, z1, color, zbuffer ):
    dx = x1 - x0
    dy = y1 - y0
    dz = z1 - z0
    if dx + dy < 0:
        dx = 0 - dx
        dy = 0 - dy
        dz = 0 -dz
        tmp = x0
        x0 = x1
        x1 = tmp
        tmp = y0
        y0 = y1
        y1 = tmp
        tmp = z0
        z0 = z1
        z1 = tmp

    if dx == 0 and dy == 0:
        zplot(screen, color, x0, y0, max(z0, z1), zbuffer)
    elif dx == 0:
        y = y0
        z = z0
        while y <= y1:
            zplot(screen, color, x0, y, z, zbuffer)
            y = y + 1
            z += dz/dy
    elif dy == 0:
        x = x0
        z = z0
        while x <= x1:
            zplot(screen, color, x, y0, z, zbuffer)
            x = x + 1
            z += dz/dx
    elif dy < 0:
        d = 0
        x = x0
        y = y0
        z = z0
        while x <= x1:
            zplot(screen, color, x, y, z, zbuffer)
            if d > 0:
                y = y - 1
                d = d - dx
            x = x + 1
            z += dz/dy
            d = d - dy
    elif dx < 0:
        d = 0
        x = x0
        y = y0
        z = z0
        while y <= y1:
            zplot(screen, color, x, y, z, zbuffer)
            if d > 0:
                x = x - 1
                d = d - dy
            y = y + 1
            z += dz/dy
            d = d - dx
    elif dx > dy:
        d = 0
        x = x0
        y = y0
        z = z0
        while x <= x1:
            zplot(screen, color, x, y, z, zbuffer)
            if d > 0:
                y = y + 1
                d = d - dx
            x = x + 1
            z += dz/dx
            d = d + dy

            
