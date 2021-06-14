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
    normalize(normal)
    normalize(light[LOCATION])
    normalize(view)

    ambient = calculate_ambient(ambient, areflect)
    diffuse = calculate_diffuse(light, dreflect, normal)
    specular = calculate_specular(light, sreflect, view, normal)

    r = ambient[0] + diffuse[0] + specular[0]
    g = ambient[1] + diffuse[1] + specular[1]
    b = ambient[2] + diffuse[2] + specular[2]

    return limit_color([r, g, b])

def calculate_ambient(alight, areflect):
    r = alight[0] * areflect[0]
    g = alight[1] * areflect[1]
    b = alight[2] * areflect[2]

    return limit_color([r, g, b])

def calculate_diffuse(light, dreflect, normal):
    color = dot_product(normal, light[LOCATION])
    r = light[COLOR][0] * dreflect[0] * color
    g = light[COLOR][1] * dreflect[1] * color
    b = light[COLOR][2] * dreflect[2] * color

    return limit_color([r, g, b])

def calculate_specular(light, sreflect, view, normal):
    cos = 2 * dot_product(light[LOCATION], normal)

    r = [normal[0] * cos - light[LOCATION][0],
             normal[1] * cos - light[LOCATION][1],
             normal[2] * cos - light[LOCATION][2]]

    spec = dot_product(r, view)

    if spec <= 0:
        return [0, 0, 0]

    spec = spec ** SPECULAR_EXP

    r = light[COLOR][0] * sreflect[0] * spec
    g = light[COLOR][1] * sreflect[1] * spec
    b = light[COLOR][2] * sreflect[2] * spec

    return limit_color([r, g, b])

def limit_color(color):
    return [max(min(int(color[i]), 255), 0) for i in range(len(color))]

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
