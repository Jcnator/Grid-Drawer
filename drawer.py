import sys
import math
import numpy as np
from PIL import Image, ImageDraw


# grid_type either "triangle", "square", or "hex" for the shape
# grid size is the apothem of the polygon
# rotation is final rotation angle ontop of image in rads
def draw_grid(image_path, grid_type = 0, grid_size = 25, grid_width = 5, angle = 0):
    im = Image.open(image_path)
    len_x, len_y = im.size
    grid_rotation = float(angle) * (180/math.pi)
    print("Rotation Angle: ")
    print(grid_rotation)
    center = ((len_x)/2 - 1 , (len_y) /2  -1)
    apothem = float(grid_size)
    if grid_type == "triangle":
        vertex_pairs = getTrianglePoints(len_x, len_y, apothem, grid_rotation, center)
    elif grid_type == "square":
        vertex_pairs = getSquarePoints(len_x, len_y, apothem, grid_rotation, center)
    elif grid_type == "hex":
        vertex_pairs = getHexagonPoints(len_x, len_y, apothem, grid_rotation, center)
    else:
        print("Shape not supported")
        return

    print(vertex_pairs )

    drawLines(im, vertex_pairs, int(grid_width))
    im.show()


def getTrianglePoints(len_x, len_y, apothem, grid_rotation, center):
    side_length = apothem * 2 * (math.pi / 3)
    radius = apothem / (math.cos(math.pi/3))
    off_set = math.sqrt(4 * apothem ** 2 - (side_length/4) ** 2)
    points = []
    x = 0
    while x < 2*len_x:
        y = 0
        while y < 2*len_y:
            # points = points + rotatePoints(getPolygonVertices(x, y, apothem, 3), grid_rotation, center)
            # points = points + rotatePoints(getPolygonVertices(x + side_length / 2, y - off_set , apothem, 3), grid_rotation + math.pi, center)
            points = points + getPolygonVertices(x, y, apothem, 3, center, grid_rotation)
            #points = points + getPolygonVertices(x + side_length / 2, y - off_set , apothem, 3, center,grid_rotation)
            y = y + side_length
        x = x + side_length
    return points

def getSquarePoints(len_x, len_y, apothem, grid_rotation, center):
    points = []
    x = 0
    while x < 2*len_x :
        y = 0
        while y < 2*len_y :
            points = points + getPolygonVertices(x, y, apothem, 4, center, grid_rotation)
            #points = points + getPolygonVertices(x, y, apothem, 4)
            y = y + apothem
        x = x + apothem
    return points


def getPolygonVertices(x, y, apothem, numPoints, center, grid_rotation):
    vertices = []
    vertex_pairs = [] # [[(x1,y1),(x2,y2)],...,[(xn,yn),(x1,y1)]]
    angle = 2 * math.pi / numPoints
    for i in range(numPoints):
        vX = (x + float(apothem) * math.sin(float(i) * angle))
        vY = (y + float(apothem) * math.cos(float(i) * angle))
        point = (vX, vY)
        #point = rotatePoint(point, grid_rotation, center)
        vertices.append(point)
    for i in range(0,len(vertices)):
        pair = [vertices[i],vertices[(i+1)%len(vertices)]]
        vertex_pairs.append(pair)
    #print(vertex_pairs)
    return vertex_pairs


def drawLines(im, vertex_pairs, grid_width):
    draw = ImageDraw.Draw(im)
    for pair in vertex_pairs:
        draw.line(pair, 0, grid_width)

def rotatePoints(points, grid_rotation, center):
    rotated_points = []
    for point in points:
        #rotatePoint(point, grid_rotation)
        rotated_points.append(rotatePoint(point, grid_rotation, center))
    return rotated_points

def rotatePoint(point, grid_rotation, center):
    x, y = point
    px, py = center
    grid_rotation = float(grid_rotation)
    x_rot = (x - px) * math.cos(grid_rotation) - (y - py) * math.sin(grid_rotation)
    y_rot = (y - py) * math.cos(grid_rotation) - (x - px) * math.sin(grid_rotation)
    print(x,y)
    print(x_rot, y_rot)
    return x_rot, y_rot

if __name__ == "__main__":
    image_path = sys.argv[1]
    grid_type = sys.argv[2]
    grid_size = sys.argv[3]
    grid_width = sys.argv[4]
    angle = sys.argv[5]
    draw_grid(image_path, grid_type, grid_size, grid_width, angle)
