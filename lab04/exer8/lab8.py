import pygame
from OpenGL.GL import *
import numpy as np
import time


# Mandelbrot
# 100 16 -1.5 0.5 -1 1 0 0
# Julia
# 100 16 -1 1 -1.2 1.2 0.32 0.043
def main():
    fractal = input("Type 'm' to draw the Mandelbrot set and 'j' to draw the Julia set fractals> ")
    i = input("Epsilon value, number of iterations, min/max u, min/max v, complex constant> ")
    i = i.split(" ")
    eps = int(i[0])
    m = int(i[1])
    u = (float(i[2]), float(i[3]))
    v = (float(i[4]), float(i[5]))
    c = complex(float(i[6]), float(i[7]))

    pygame.init()
    res = (1000, 1000)
    pygame.display.set_caption("Fractals")
    pygame.display.set_mode(res, pygame.DOUBLEBUF | pygame.OPENGL)

    mandelbrot = True
    if fractal == 'j':
        glScale(0.8, 0.8, 0.8)
        mandelbrot = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_fractal(res, u, v, m, eps, c, mandelbrot)
        pygame.display.flip()
        time.sleep(20000)


def draw_fractal(res, u, v, m, eps, c, mandelbrot):
    glBegin(GL_POINTS)
    screen_x = res[0]
    screen_y = res[1]
    u_min = u[0]
    u_max = u[1]
    v_min = v[0]
    v_max = v[1]
    for x in range(res[0]):
        if (x % 5) == 0:
            print("Loading", round(x / screen_x * 100), "%")
        for y in range(res[1]):
            u0 = (x * (u_max - u_min) / screen_x) + u_min
            v0 = (y * (v_max - v_min) / screen_y) + v_min
            k = -1
            if mandelbrot:
                c = complex(u0, v0)
                z = complex(0, 0)
            else:
                z = complex(u0, v0)
            while True:
                k += 1
                z = z * z + c
                r = np.sqrt((z.real * z.real) + (z.imag * z.imag))
                if r >= eps or k >= m:
                    break
            glColor3f(k / m, k / m - 0.3, k / m + 0.4)
            if mandelbrot:
                glVertex2f(u0 + 0.5, v0)
            else:
                glVertex2f(u0, v0)
    glEnd()


if __name__ == "__main__":
    main()
