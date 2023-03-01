import sys
import math
from PIL import Image, ImageDraw


# grid_type either "triangle", "square", or "hex" for the shape
# grid size is the apothem of the polygon
# rotation is final rotation angle ontop of image in rads
def draw_grid(image_path, grid_type = 0, grid_size = 25, grid_width = 5, angle = 0):
    im = Image.open(image_path)
    len_x, len_y = im.size
    grid_rotation = float(angle) * (math.pi/180)
    # print("Rotation Angle: ")
    # print(grid_rotation)
    center = ((len_x)/2 - 1 , (len_y) /2  -1)
    radius = float(grid_size)
    if grid_type == "triangle":
        vertex_pairs = getTrianglePoints(len_x, len_y, radius, grid_rotation, center)
    elif grid_type == "square":
        vertex_pairs = getSquarePoints(len_x, len_y, radius, grid_rotation, center)
    elif grid_type == "hex":
        vertex_pairs = getHexagonPoints(len_x, len_y, radius, grid_rotation, center)
    else:
        print("Shape not supported")
        return

    drawLines(im, vertex_pairs, int(grid_width))
    im.show()
    im.save("grid.jpg")


def getTrianglePoints(len_x, len_y, radius, grid_rotation, center):
    n = 3
    side_length = 2 * radius * math.sin(math.pi/n)
    apothem = radius  * math.cos(math.pi/n)
    #print(apothem, side_length, radius )
    points = []
    x =  -2*len_x
    while x < 2*len_x:
        y =  -2*len_x
        while y < 2*len_y:
            points = points + getPolygonVertices(x, y, radius, n, center, grid_rotation)
            points = points + getPolygonVertices(x + side_length/4 , y + (radius + apothem)/2, radius, n, center, grid_rotation)
            y = y + (radius + apothem)
        x = x + side_length/2
    return points

def getSquarePoints(len_x, len_y, radius, grid_rotation, center):
    n = 4
    side_length = 2 * radius * math.sin(math.pi/n)
    apothem = radius  * math.cos(math.pi/n)
    #print(apothem, side_length, radius )

    points = []
    x = -3*len_x
    while x < 3*len_x :
        y =  -3*len_x
        while y < 3*len_y :
            points = points + getPolygonVertices(x, y, radius, n, center, grid_rotation + math.pi/4)
            y = y + radius
        x = x + radius
    return points

def getHexagonPoints(len_x, len_y, radius, grid_rotation, center):
    n = 6
    side_length = 2 * radius * math.sin(math.pi/n)
    apothem = radius  * math.cos(math.pi/n)
    #print(apothem, side_length, radius )
    points = []
    x = 0
    while x < 2*len_x:
        y =  0
        while y < 2*len_y:
            #print(x,y)
            points = points + getPolygonVertices(x, y, radius, n, center, grid_rotation)
            points = points + getPolygonVertices(x + apothem, y + radius + side_length/2 , radius, 6, center, grid_rotation)
            y = y  + 2*radius + side_length
        x = x + 2*apothem
    return points

def getPolygonVertices(x, y, radius, numPoints, center, grid_rotation):
    vertices = []
    vertex_pairs = [] # [[(x1,y1),(x2,y2)],...,[(xn,yn),(x1,y1)]]
    angle = 2 * math.pi / numPoints
    for i in range(numPoints):
        vX = (x + float(radius) * math.sin(float(i) * angle))
        vY = (y + float(radius) * math.cos(float(i) * angle))
        point = (vX, vY)
        point = rotatePoint(point, grid_rotation, center)
        vertices.append(point)
    for i in range(len(vertices)):
        pair = [vertices[i],vertices[(i+1)%len(vertices)]]
        vertex_pairs.append(pair)
    #print(vertex_pairs)
    #print(" ")
    return vertex_pairs

def drawLines(im, vertex_pairs, grid_width):
    draw = ImageDraw.Draw(im)
    for pair in vertex_pairs:
        draw.line(pair, 0, grid_width)

def rotatePoints(points, grid_rotation, center):
    rotated_points = []
    for point in points:
        #rotatePoint(point, grid_rotation)
        rotated_points = rotated_points + rotatePoint(point, grid_rotation, center)
    return rotated_points

def rotatePoint(point, angle, center):
    x, y = point
    cx, cy = center
    s = math.sin(angle)
    c = math.cos(angle)
    x = x - cx
    y = y - cy
    x_rot = x * c - y * s
    y_rot = x * s + y * c
    x_rot = x_rot + cx
    y_rot = y_rot + cy
    # print(x,y , "->",   x_rot, y_rot)
    #print(x_rot, y_rot)
    return x_rot, y_rot

if __name__ == "__main__":
    image_path = sys.argv[1]
    grid_type = sys.argv[2]
    grid_size = sys.argv[3]
    grid_width = sys.argv[4]
    angle = sys.argv[5]
    draw_grid(image_path, grid_type, grid_size, grid_width, angle)
