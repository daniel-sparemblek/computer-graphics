import pygame
from OpenGL.GL import *
import numpy as np


def main():
    print("Usage: WASDQE to rotate and arrow keys to pan.")
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

    pygame.init()
    res = (1000, 1000)
    pygame.display.set_caption("Translation and projection")
    pygame.display.set_mode(res, pygame.DOUBLEBUF | pygame.OPENGL)
    ociste, glediste = points()
    ociste = (2.0, 2.0, 3.0)
    glediste = find_center(vertices)
    T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
    vertices_T = transform_object(vertices, T_matrix, homogeno)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    x, y, z = ociste
                    z = z - 0.1
                    ociste = (x, y, z)
                    T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
                    vertices_T = transform_object(vertices, T_matrix, homogeno)
                if event.key == pygame.K_q:
                    x, y, z = ociste
                    x = x - 0.1
                    ociste = (x, y, z)
                    T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
                    vertices_T = transform_object(vertices, T_matrix, homogeno)
                if event.key == pygame.K_e:
                    x, y, z = ociste
                    x = x + 0.1
                    ociste = (x, y, z)
                    T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
                    vertices_T = transform_object(vertices, T_matrix, homogeno)
                if event.key == pygame.K_w:
                    x, y, z = ociste
                    z = z + 0.1
                    ociste = (x, y, z)
                    T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
                    vertices_T = transform_object(vertices, T_matrix, homogeno)
                if event.key == pygame.K_a:
                    x, y, z = ociste
                    y = y + 0.1
                    ociste = (x, y, z)
                    T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
                    vertices_T = transform_object(vertices, T_matrix, homogeno)
                if event.key == pygame.K_d:
                    x, y, z = ociste
                    y = y - 0.1
                    ociste = (x, y, z)
                    T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
                    vertices_T = transform_object(vertices, T_matrix, homogeno)
                if event.key == pygame.K_DOWN:
                    x, y, z = glediste
                    z = z + 0.1
                    glediste = (x, y, z)
                    T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
                    vertices_T = transform_object(vertices, T_matrix, homogeno)
                if event.key == pygame.K_UP:
                    x, y, z = glediste
                    z = z - 0.1
                    glediste = (x, y, z)
                    T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
                    vertices_T = transform_object(vertices, T_matrix, homogeno)
                if event.key == pygame.K_LEFT:
                    x, y, z = glediste
                    y = y + 0.1
                    glediste = (x, y, z)
                    T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
                    vertices_T = transform_object(vertices, T_matrix, homogeno)
                if event.key == pygame.K_RIGHT:
                    x, y, z = glediste
                    y = y - 0.1
                    glediste = (x, y, z)
                    T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
                    vertices_T = transform_object(vertices, T_matrix, homogeno)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_object(vertices_T, indices)
        pygame.display.flip()


def calculate_transformation_matrix(ociste, glediste):
    x0, y0, z0 = ociste
    xg, yg, zg = glediste
    T1 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-x0, -y0, -z0, 1]])
    xg1 = xg - x0
    yg1 = yg - y0
    zg1 = zg - z0
    xg2 = np.sqrt(xg1 ** 2 + yg1 ** 2)
    zg2 = zg1
    sin_alpha = yg1 / xg2
    cos_alpha = xg1 / xg2
    T2 = np.array([[cos_alpha, -sin_alpha, 0, 0], [sin_alpha, cos_alpha, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    zg3 = np.sqrt(xg2 ** 2 + zg2 ** 2)
    sin_beta = xg2 / zg3
    cos_beta = zg2 / zg3
    T3 = np.array([[cos_beta, 0, sin_beta, 0], [0, 1, 0, 0], [-sin_beta, 0, cos_beta, 0], [0, 0, 0, 1]])
    T4 = np.array([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    T5 = np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    T = T1.dot(T2)
    T = T.dot(T3)
    T = T.dot(T4)
    T = T.dot(T5)
    return T, zg3  # Returning H


def transform_object(vertices, T_matrix, homogeno):
    P = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1 / homogeno], [0, 0, 0, 0]])
    vertices_T = []
    for vertex in vertices:
        x1, x2, x3 = vertex
        vertex_h = np.array([x1, x2, x3, 1])
        vertex_trans = vertex_h.dot(T_matrix)
        x1, x2, x3, h = vertex_trans
        vertex_p = np.array([x1, x2, x3, 1])
        vertex_proj = vertex_p.dot(P)
        vertices_T.append((vertex_proj[0], vertex_proj[1], vertex_proj[2]))
    return vertices_T


def draw_object(vertices, indices):
    for index in indices:
        glBegin(GL_LINE_LOOP)
        for vertex in index:
            glVertex3fv(vertices[vertex - 1])
        glEnd()


def points():
    ociste = []
    glediste = []
    file = open("points", "r")
    for line in file:
        if line.startswith("o"):
            split = line.split(" ")
            ociste.append((float(split[1].strip()), float(split[2].strip()), float(split[3].strip())))
        if line.startswith("g"):
            split = line.split(" ")
            glediste.append((float(split[1].strip()), float(split[2].strip()), float(split[3].strip())))
    file.close()
    return ociste, glediste


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
