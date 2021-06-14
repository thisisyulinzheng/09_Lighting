import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    a = calculate_ambient(ambient, areflect)
    d = calculate_diffuse(light, dreflect, normal)
    s = calculate_specular(light, sreflect, view, normal)
    I = [   int(a[0] + d[0] + s[0]),
            int(a[1] + d[1] + s[1]),
            int(a[2] + d[2] + s[2])     ]
    F = limit_color(I)

    return F

def calculate_ambient(alight, areflect):
    a = areflect[0]
    b = areflect[1]
    c = areflect[2]
    areflect = [alight[0] * a, alight[1] * b, alight[2] * c]
    return areflect

def calculate_diffuse(light, dreflect, normal):

    P = light[1]
    a0 = dreflect[0]
    b0 = dreflect[1]
    c0 = dreflect[2]
    dreflect = [P[0] * a0, P[1] * b0, P[2] * c0]

    L = light[0]
    normalize(L)
    normalize(normal)
    d = dot_product(normal, L)

    a1 = dreflect[0]
    b1 = dreflect[1]
    c1 = dreflect[2]
    dreflect = [a1*d, b1*d, c1*d]

    return (dreflect)

def calculate_specular(light, sreflect, view, normal):
    L = light[0]
    normalize(L)
    normalize(normal)
    d0 = dot_product(normal, L)
    T2 = [2*normal[0]*d0, 2*normal[1]*d0, 2*normal[2]*d0]

    R = [T2[0] - L[0], T2[1] - L[1], T2[2] - L[2]]
    V = view
    normalize(V)
    d1 = dot_product(R, V) ** 2 #played around a bit and an exp of 2 just looked better


    P = light[1]
    a0 = sreflect[0]
    b0 = sreflect[1]
    c0 = sreflect[2]
    sreflect = [P[0]*a0*d1, P[1]*b0*d1, P[2]*c0*d1]

    return (sreflect)

def limit_color(color):
    c1 = color[0] % 255
    c2 = color[1] % 255
    c3 = color[2] % 255
    return [c1, c2, c3]

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
