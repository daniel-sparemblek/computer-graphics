import pygame


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Edge:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class Polygon:
    def __init__(self, point=(0, 0), edge=(0, 0, 0), left=True):
        self.vertex = point
        self.edge = edge
        self.left = left


def main():
    print("Usage: Left click to draw, Right click to finish drawing, Space to fill and Middle button to check if "
          "point is within polygon")
    pygame.init()
    res = (800, 800)
    pygame.display.set_caption("Polygon coloring")
    screen = pygame.display.set_mode(res)

    drawn = False
    polygon_list = []

    while True:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                poly = Polygon(Point(mx, my), Edge(0, 0, 0), False)
                polygon_list.append(poly)
            elif event.button == 3:
                draw_polygon(polygon_list, screen)
                pygame.display.flip()
                calc_coefs(polygon_list)
                drawn = True
            elif event.button == 2:
                mx, my = pygame.mouse.get_pos()
                check_point(mx, my, polygon_list)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if drawn:
                    fill(polygon_list, screen)


def check_point(x, y, polygons):
    outside = False
    if polygons:
        for poly in polygons:
            if (poly.edge.a * x + poly.edge.b * y + poly.edge.c) < 0:
                outside = True
        if outside:
            print("Point is outside of polygon")
        else:
            print("Point is inside polygon")
    else:
        print("No polygons")


def draw_polygon(polygons, screen):
    white = (255, 255, 255)
    num_of_items = len(polygons)
    j = num_of_items - 1
    for i in range(0, num_of_items):
        pygame.draw.line(screen, white, (polygons[j].vertex.x, polygons[j].vertex.y),
                         (polygons[i].vertex.x, polygons[i].vertex.y))
        j = i


def fill(polygons, screen):
    white = (255, 255, 255)
    xmin = xmax = polygons[0].vertex.x
    ymin = ymax = polygons[0].vertex.y
    num_of_items = len(polygons)
    for i in range(1, num_of_items):
        if xmin > polygons[i].vertex.x:
            xmin = polygons[i].vertex.x
        if xmax < polygons[i].vertex.x:
            xmax = polygons[i].vertex.x
        if ymin > polygons[i].vertex.y:
            ymin = polygons[i].vertex.y
        if ymax < polygons[i].vertex.y:
            ymax = polygons[i].vertex.y
    for y in range(ymin, ymax+1):
        L = xmin
        D = xmax
        j = num_of_items - 1
        for i in range(0, num_of_items):
            if polygons[j].edge.a == 0:
                if polygons[j].vertex.y == y:
                    if polygons[j].vertex.x < polygons[i].vertex.x:
                        L = polygons[j].vertex.x
                        D = polygons[i].vertex.x
                    else:
                        L = polygons[i].vertex.x
                        D = polygons[j].vertex.x
                    break
            else:
                x = (-polygons[j].edge.b*y-polygons[j].edge.c)/polygons[j].edge.a
                if polygons[j].left:
                    if L < x:
                        L = x
                else:
                    if D > x:
                        D = x
            j = i
        pygame.draw.line(screen, white, (round(L), y), (round(D), y))
        pygame.display.flip()


def calc_coefs(polygons):
    num_of_items = len(polygons)
    j = num_of_items - 1
    for i in range(0, num_of_items):
        polygons[j].edge.a = polygons[j].vertex.y - polygons[i].vertex.y
        polygons[j].edge.b = -(polygons[j].vertex.x - polygons[i].vertex.x)
        polygons[j].edge.c = polygons[j].vertex.x * polygons[i].vertex.y - polygons[j].vertex.y * polygons[i].vertex.x
        polygons[j].left = polygons[j].vertex.y > polygons[i].vertex.y
        j = i


if __name__ == "__main__":
    main()
