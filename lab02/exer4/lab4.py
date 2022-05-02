import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


def main():
    print("Usage: Space to start and stop rotation, left-mouse button to check if point is within a convex polygon.")
    print("NOTE: Point checking only works on convex polygons.")
    filename = input("Write the name of the .obj file you would like to load: ")
    ext = ".obj"
    indices = []
    vertices = []
    num_of_vertices = 0
    num_of_polygons = 0

    file = open(filename+ext, "r")
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

    print("\nSuccessfully loaded {}".format(filename+ext))
    print("Number of vertices: {}".format(num_of_vertices))
    print("Number of polygons: {}".format(num_of_polygons))

    rotate = True
    center, max_span = find_center(vertices)
    correct_scale = scale(max_span)  # Ne vraca dubinu objekta
    vertices_trans = []
    for v in vertices:
        vertices_trans.append(((v[0] - center[0]), (v[1] - center[1]), (v[2] - center[2])))
    coefs = calc_coefs(vertices_trans, indices)

    pygame.init()
    res = (1000, 1000)
    pygame.display.set_caption(".obj importing")
    pygame.display.set_mode(res, pygame.DOUBLEBUF | pygame.OPENGL)
    glScale(correct_scale, correct_scale, correct_scale)
    gluPerspective(0, 1, 0.001, 50.0)
    glPushMatrix()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rotate = not rotate
                    glPopMatrix()
                    glPushMatrix()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not rotate:
                        mx, my = pygame.mouse.get_pos()
                        real_x = (((mx / res[0]) * 2) - 1) / correct_scale
                        real_y = -(((my / res[1]) * 2) - 1) / correct_scale
                        check_point(real_x, real_y, coefs)
                    else:
                        print("Stop rotation to check if point is within polygon.")
        if rotate:
            glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_object(vertices_trans, indices)
        pygame.display.flip()


def draw_object(vertices, indices):
    for index in indices:
        glBegin(GL_LINE_LOOP)
        for vertex in index:
            glVertex3fv(vertices[vertex - 1])
        glEnd()


def calc_coefs(vertices, indices):
    coefs = []
    coords = []
    for index in indices:
        for i in range(3):
            for j in range(3):
                coords.append(vertices[index[j] - 1][i])
        x1, x2, x3, y1, y2, y3, z1, z2, z3 = coords

        A = (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)
        B = - (x2 - x1) * (z3 - z1) + (z2 - z1) * (x3 - x1)
        C = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        D = -x1 * A - y1 * B - z1 * C
        coefs.append((A, B, C, D))
        coords.clear()
    return coefs


def check_point(x, y, coefs):
    outside = False
    for coef in coefs:
        # kao sto je navedeno u zadatku uvijek vrijedi z=0
        if coef[0] * x + coef[1] * y + coef[2] * 0 + coef[3] > 0:
            outside = True
    if outside:
        print("Point is outside of polygon")
    else:
        print("Point is inside polygon")


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
    max_span = max(abs(xmax - xmin), abs(ymax - ymin))
    return center, max_span


def scale(max_value):
    value = round(1 / max_value, 4)
    return 1.1 * value


if __name__ == "__main__":
    main()
