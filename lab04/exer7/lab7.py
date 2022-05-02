import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


def main():
    filename = input("Write the name of the .obj file you would like to load: ")
    ext = ".obj"
    indices = []
    vertices = []
    num_of_vertices = 0
    num_of_polygons = 0

    file = open(filename + ext, "r")
    for line in file:
        if line.startswith("v"):
            num_of_vertices += 1
            split = line.split(" ")
            vertices.append((float(split[1].strip()), float(split[2].strip()), float(split[3].strip())))
        if line.startswith("f"):
            num_of_polygons += 1
            split = line.split(" ")
            indices.append((int(split[1].strip()), int(split[2].strip()), int(split[3].strip())))
    file.close()

    print("\nSuccessfully loaded {}".format(filename + ext))
    print("Number of vertices: {}".format(num_of_vertices))
    print("Number of polygons: {}".format(num_of_polygons))

    # GOURAUD
    normals = []
    for index in indices:
        normals.append(calc_normals(index, vertices))

    light_source_input = input("\nWrite the light source coordinates with a space in between: ")
    split = light_source_input.split(" ")
    light_source = (float(split[0].strip()), float(split[1].strip()), float(split[2].strip()))

    pygame.init()
    res = (1000, 1000)
    pygame.display.set_caption("Shading")
    pygame.display.set_mode(res, pygame.DOUBLEBUF | pygame.OPENGL)

    center = find_center(vertices)
    glediste = center
    ociste = (2.0, 3.0, 3.0)

    glViewport(0, 0, 1000, 1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 1, 0.5, 8.0)
    gluLookAt(ociste[0], ociste[1], ociste[2], glediste[0], glediste[1], glediste[2], 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    flat = False
    gouraud = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    # FLAT SHADING
                    gouraud = False
                    flat = not flat
                if event.key == pygame.K_g:
                    # GOURAUD SHADING
                    flat = False
                    gouraud = not gouraud
                if event.key == pygame.K_LEFT:
                    temp = ociste[0]
                    temp = temp - 0.2
                    ociste = (temp, ociste[1], ociste[2])
                    glMatrixMode(GL_PROJECTION)
                    glLoadIdentity()
                    gluPerspective(45.0, 1, 0.5, 8.0)
                    gluLookAt(ociste[0], ociste[1], ociste[2], glediste[0], glediste[1], glediste[2], 0, 1, 0)
                    glMatrixMode(GL_MODELVIEW)
                if event.key == pygame.K_RIGHT:
                    temp = ociste[0]
                    temp = temp + 0.2
                    ociste = (temp, ociste[1], ociste[2])
                    glMatrixMode(GL_PROJECTION)
                    glLoadIdentity()
                    gluPerspective(45.0, 1, 0.5, 8.0)
                    gluLookAt(ociste[0], ociste[1], ociste[2], glediste[0], glediste[1], glediste[2], 0, 1, 0)
                    glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_object(vertices, indices, ociste, glediste, light_source, normals, flat, gouraud)
        pygame.display.flip()


def calc_gouraud_intensity(vertex, vertices, indices, light, normals):
    index_of_vertex = vertices.index(vertex)
    index_of_vertex += 1
    dio_kojih_lica_je_vertex = []
    for i in indices:
        if index_of_vertex in i:
            dio_kojih_lica_je_vertex.append(indices.index(i))
    vertex_normal_x = vertex_normal_y = vertex_normal_z = 0

    for polygon_number in dio_kojih_lica_je_vertex:
        vertex_normal_x += normals[polygon_number][0]
        vertex_normal_y += normals[polygon_number][1]
        vertex_normal_z += normals[polygon_number][0]

    vertex_normal_x = vertex_normal_x / len(dio_kojih_lica_je_vertex)
    vertex_normal_y = vertex_normal_y / len(dio_kojih_lica_je_vertex)
    vertex_normal_z = vertex_normal_z / len(dio_kojih_lica_je_vertex)

    vertex_normal = (vertex_normal_x, vertex_normal_y, vertex_normal_z)
    N = normalize(vertex_normal)
    L = (light[0] - N[0], light[1] - N[1], light[2] - N[2])
    L = normalize(L)
    Id = np.dot(N, L)
    if Id > 0:
        intensity = 10 + 200 * Id
    else:
        intensity = 0
    return intensity


def calc_normals(index, vertices):
    test_vertices = []
    for i in index:
        test_vertices.append(vertices[i - 1])
    x1, y1, z1 = test_vertices[0]
    x2, y2, z2 = test_vertices[1]
    x3, y3, z3 = test_vertices[2]
    v1 = (x2 - x1, y2 - y1, z2 - z1)
    v2 = (x3 - x2, y3 - y2, z3 - z2)
    N1 = np.cross(v1, v2)
    return N1


def calc_flat_intensity(index, vertices, light):
    test_vertices = []
    for i in index:
        test_vertices.append(vertices[i - 1])
    x1, y1, z1 = test_vertices[0]
    x2, y2, z2 = test_vertices[1]
    x3, y3, z3 = test_vertices[2]
    v1 = (x2 - x1, y2 - y1, z2 - z1)
    v2 = (x3 - x2, y3 - y2, z3 - z2)
    N1 = np.cross(v1, v2)
    centroid_x = (x1 + x2 + x3) / 3
    centroid_y = (y1 + y2 + y3) / 3
    centroid_z = (z1 + z2 + z3) / 3
    L1 = (light[0] - centroid_x, light[1] - centroid_y, light[2] - centroid_z)
    L1 = normalize(L1)
    N1 = normalize(N1)
    Id = np.dot(N1, L1)
    if Id > 0:
        intensity = 10 + 200 * Id
    else:
        intensity = 0
    return intensity


def normalize(vector):
    x = vector[0]
    y = vector[1]
    z = vector[2]
    res = np.sqrt(x*x + y*y + z*z)
    vector_normalized = (x / res, y / res, z / res)
    return vector_normalized


def backface_culling(ociste, glediste, index, vertices):
    N1 = calc_normals(index, vertices)
    x1, y1, z1 = ociste
    x2, y2, z2 = glediste
    v1 = (x2 - x1, y2 - y1, z2 - z1)
    result = np.dot(N1, v1)
    if result >= 0:
        return False
    else:
        return True


def draw_object(vertices, indices, ociste, glediste, light, normals, flat, gouraud):
    for index in indices:
        glColor3f(1, 1, 1)
        isRemoved = backface_culling(ociste, glediste, index, vertices)
        if isRemoved:
            if flat:
                intensity = (calc_flat_intensity(index, vertices, light)) / 210
                glColor3f(intensity, 0, intensity)
            if flat or gouraud:
                glBegin(GL_TRIANGLES)
            else:
                glBegin(GL_LINE_LOOP)
            for vertex in index:
                if gouraud:
                    intensity = (calc_gouraud_intensity(vertices[vertex - 1], vertices, indices, light, normals)) / 210
                    glColor3f(intensity, 0, intensity)
                glVertex3fv(vertices[vertex - 1])
            glEnd()
        else:
            continue


def find_center(vertices):
    xmin = xmax = vertices[0][0]
    ymin = ymax = vertices[0][1]
    zmin = zmax = vertices[0][2]
    for i in range(1, len(vertices)):
        if xmin > vertices[i][0]:
            xmin = vertices[i][0]
        if xmax < vertices[i][0]:
            xmax = vertices[i][0]
        if ymin > vertices[i][1]:
            ymin = vertices[i][1]
        if ymax < vertices[i][1]:
            ymax = vertices[i][1]
        if zmin > vertices[i][2]:
            zmin = vertices[i][2]
        if zmax < vertices[i][2]:
            zmax = vertices[i][2]
    center = (((xmax + xmin) / 2), ((ymax + ymin) / 2), ((zmax + zmin) / 2))
    return center


if __name__ == "__main__":
    main()
