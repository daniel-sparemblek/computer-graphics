import pygame
from OpenGL.GL import *
import numpy as np
import time


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

    pygame.init()
    res = (1000, 1000)
    pygame.display.set_caption("Bezier animation")
    pygame.display.set_mode(res, pygame.DOUBLEBUF | pygame.OPENGL)
    center = find_center(vertices)
    glediste = center
    bezier_cords = get_bezier_cords()
    points = calc_bezier(bezier_cords)
    i = 0
    boomerang = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # USED FOR DRAWING A BEZIER CURVE
        # glColor3f(1, 0, 0)
        # draw_bezier(points)
        # glColor3f(0, 1, 0)
        # draw_bezier(bezier_cords)
        # pygame.display.flip()

        # USED FOR ANIMATION
        if i < 0:
            pygame.quit()
            quit()
        ociste = points[i]
        draw_object(vertices, indices, ociste, glediste)
        pygame.display.flip()
        time.sleep(0.1)  # Animation lasts 10 secs and goes back
        if (i < len(points) - 1) and (i >= 0):
            if boomerang:
                i -= 1
            else:
                i += 1
        else:
            boomerang = not boomerang
            i -= 1


def get_bezier_cords():
    bezier_cords = []
    file = open("bezier", "r")
    for line in file:
        if line.startswith("v"):
            split = line.split(" ")
            bezier_cords.append((float(split[1].strip()), float(split[2].strip()), float(split[3].strip())))
    file.close()
    return bezier_cords


def draw_bezier(bezier_cords):
    num_of_items = len(bezier_cords)
    for i in range(0, num_of_items - 1):
        glBegin(GL_LINES)
        glVertex3fv(bezier_cords[i])
        glVertex3fv(bezier_cords[i + 1])
        glEnd()


def calc_bezier(bezier_cords):
    n = len(bezier_cords) - 1
    points = []
    t_range = np.linspace(0, 0.99, 100)
    for t in t_range:
        sum_x = sum_y = sum_z = 0
        for i in range(0, n + 1):
            b = (np.math.factorial(n) * (t ** i) * ((1 - t) ** (n - i))) / (
                    np.math.factorial(i) * np.math.factorial(n - i))
            x, y, z = bezier_cords[i]
            sum_x += x * b
            sum_y += y * b
            sum_z += z * b
        points.append((sum_x, sum_y, sum_z))
    return points


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


def backface_culling(ociste, glediste, index, vertices):
    test_vertices = []
    for i in index:
        test_vertices.append(vertices[i-1])
    x1, y1, z1 = test_vertices[0]
    x2, y2, z2 = test_vertices[1]
    x3, y3, z3 = test_vertices[2]
    v1 = (x2-x1, y2-y1, z2-z1)
    v2 = (x3-x2, y3-y2, z3-z2)
    N1 = np.cross(v1, v2)

    x1, y1, z1 = ociste
    x2, y2, z2 = glediste
    v1 = (x2-x1, y2-y1, z2-z1)
    result = np.dot(N1, v1)
    if result >= 0:
        return False
    else:
        return True


def draw_object(vertices, indices, ociste, glediste):
    for index in indices:
        isRemoved = backface_culling(ociste, glediste, index, vertices)
        if isRemoved:
            glBegin(GL_LINE_LOOP)
            for vertex in index:
                T_matrix, homogeno = calculate_transformation_matrix(ociste, glediste)
                vertices_T = transform_object(vertices, T_matrix, homogeno)
                glVertex3fv(vertices_T[vertex - 1])
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
