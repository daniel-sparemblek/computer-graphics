import pygame


def main():
    pygame.init()
    res = (2000, 2000)
    pygame.display.set_caption("Bresenham's line algorithm")
    screen = pygame.display.set_mode(res)

    v1 = ()
    v2 = ()
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
    finished_input = False
    not_enter = True
    while True:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(v1) > 0 and len(v2) == 0:
                v2 = pygame.mouse.get_pos()
                finished_input = True
            elif len(v2) == 0:
                v1 = pygame.mouse.get_pos()

        if finished_input and not_enter:
            finished_input = False
            not_enter = False

            # Bresenham's line algorithm
            new_my_line = line(v1[0], v1[1], v2[0], v2[1])

            screen.blit(new_my_line, (0, 0))
            pygame.draw.line(screen, (255, 0, 0), (v1[0], v1[1] + 20), (v2[0], v2[1] + 20))
            pygame.display.flip()

    pygame.quit()


def line(x0, y0, x1, y1):
    white = (255, 255, 255)
    my_line = pygame.Surface((2000, 2000))
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            my_line.set_at((x, y), white)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            my_line.set_at((x, y), white)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    my_line.set_at((x, y), white)
    return my_line


if __name__ == '__main__':
    main()
