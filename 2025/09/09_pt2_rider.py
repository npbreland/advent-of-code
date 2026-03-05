import unittest
import itertools
import pdb

def make_rectangle_from_opposite_corners(corner1, corner2):
    dx = abs(corner1[0] - corner2[0]) + 1
    dy = abs(corner1[1] - corner2[1]) + 1
    return dx * dy

def parse_input(filename):
    corners = []
    with open(filename, "r") as file:
        for line in file:
            nums = [int(n) for n in line.rstrip().split(",")]
            corners.append(tuple(nums))

    return corners

def get_largest_possible_rectangle(corners):
    pairs = itertools.combinations(corners, 2)

    max = 0
    for pair in pairs:
        area = make_rectangle_from_opposite_corners(pair[0], pair[1])
        if area > max:
            max = area

    return max

def build_polygon(red_tiles):
    segments = []

    for i, tile in enumerate(red_tiles[:-1]):
        segments.append((tile, red_tiles[i+1]))

    return segments

def build_rectangle_from_corners(corner1, corner2):
    corner3 = (corner2[0], corner1[1])
    corner4 = (corner1[0], corner2[1])

    return [
        (corner1, corner3),
        (corner3, corner2),
        (corner2, corner4),
        (corner4, corner1)
    ]

def crosses_polygon(polygon, rectangle):
    for segment in rectangle:
        for poly_segment in polygon:
            # breakpoint()
            if segments_cross(poly_segment, segment):
                return True

    return False


def rectangle_is_inside_shape(base, test):
    return (test[0][0] >= base[0][0] and test[1][0] <= base[1][0]) \
            and (test[0][1] >= base[0][1] and test[1][1] <= base[1][1]) 

def segments_cross(base, test):

    max_y_base = max(base[0][1], base[1][1])
    min_y_base = min(base[0][1], base[1][1])

    max_x_base = max(base[0][0], base[1][0])
    min_x_base = min(base[0][0], base[1][0])

    max_y_test = max(test[0][1], test[1][1])
    min_y_test = min(test[0][1], test[1][1])

    max_x_test = max(test[0][0], test[1][0])
    min_x_test = min(test[0][0], test[1][0])

    crosses_horizontal = min_y_test < min_y_base and max_y_test > max_y_base
    within_horizontal_bounds = min_x_test >= min_x_base and max_x_test <= max_x_base


    crosses_vertical = min_x_test < min_x_base and max_x_test > max_x_base
    within_vertical_bounds = min_y_test >= min_y_base and max_y_test <= max_y_base

    return (crosses_horizontal and within_horizontal_bounds) \
            or (crosses_vertical and within_vertical_bounds)


def get_largest_rectangle_not_crossing_polygon(polygon, red_tiles):
    pairs = itertools.combinations(red_tiles, 2)

    max = 0
    max_rectangle = None
    for pair in pairs:
        rectangle = build_rectangle_from_corners(pair[0], pair[1])
        area = make_rectangle_from_opposite_corners(pair[0], pair[1])
        midpoint = get_midpoint(pair[0], pair[1])

        # breakpoint()
        if area > max and not crosses_polygon(polygon, rectangle) and point_inside_polygon(polygon, midpoint):
            max = area
            max_rectangle = rectangle

    return max, max_rectangle

def get_midpoint(corner1, corner2):
    max_x = max(corner1[0], corner2[0])
    min_x = min(corner1[0], corner2[0])

    max_y = max(corner1[1], corner2[1])
    min_y = min(corner1[1], corner2[1])

    return (round((max_x + min_x) / 2, 1), round((max_y + min_y) / 2, 1))

def point_inside_polygon(polygon, point):
    origin = (0, point[1])
    ray = (origin, point)


    poly_edges = [edge for edge in polygon if edge[0][0] <= point[0]]
    poly_sorted = sorted(poly_edges, key=lambda x: x[0][0])

    hits = 0
    for base in poly_sorted:
        # breakpoint()
        if segments_cross(base, ray) or point_on_segment(base, point):
            hits += 1
    
    return hits % 2 == 1

def point_on_segment(segment, point):
    if segment[0][0] == segment[1][0]:
        min_y = min(segment[0][1], segment[1][1])
        max_y = max(segment[0][1], segment[1][1])
        return point[0] == segment[0][0] and point[1] >= min_y and point[1] <= max_y

    elif segment[0][1] == segment[1][1]:
        min_x = min(segment[0][0], segment[1][0])
        max_x = max(segment[0][0], segment[1][0])
        return point[1] == segment[0][1] and point[0] >= min_x and point[0] <= max_x


class MyTest(unittest.TestCase):

    def test_make_rectangle_from_opposite_corners(self):
        corner1 = (7, 1)
        corner2 = (11, 1)
        area = make_rectangle_from_opposite_corners(corner1, corner2)
        self.assertEqual(5, area)

        corner1 = (7, 1)
        corner2 = (11, 7)
        area = make_rectangle_from_opposite_corners(corner1, corner2)
        self.assertEqual(35, area)

        corner1 = (2, 5)
        corner2 = (9, 7)
        area = make_rectangle_from_opposite_corners(corner1, corner2)
        self.assertEqual(24, area)

        corner1 = (2, 5)
        corner2 = (11, 1)
        area = make_rectangle_from_opposite_corners(corner1, corner2)
        self.assertEqual(50, area)

        corner1 = (2, 3)
        corner2 = (7, 3)
        area = make_rectangle_from_opposite_corners(corner1, corner2)
        self.assertEqual(6, area)

    def test_parse_input(self):
        corners = parse_input("test_input.txt")
        self.assertEqual([
            (7, 1),
            (11, 1),
            (11, 7),
            (9, 7),
            (9, 5),
            (2, 5),
            (2, 3),
            (7, 3),
        ], corners)

    def test_get_largest_possible_rectangle(self):
        corners = parse_input("test_input.txt")
        self.assertEqual(50, get_largest_possible_rectangle(corners))

    def test_rectangle_is_inside_shape(self):

        base1 = (7, 1)
        base2 = (11, 7)

        corner1 = (7, 1)
        corner2 = (11, 1)
        self.assertTrue(rectangle_is_inside_shape((base1, base2), (corner1, corner2)))

        corner1 = (7, 1)
        corner2 = (10, 5)
        self.assertTrue(rectangle_is_inside_shape((base1, base2), (corner1, corner2)))

        corner1 = (6, 1)
        corner2 = (11, 1)
        self.assertFalse(rectangle_is_inside_shape((base1, base2), (corner1, corner2)))
        
        corner1 = (7, 1)
        corner2 = (12, 1)
        self.assertFalse(rectangle_is_inside_shape((base1, base2), (corner1, corner2)))

    def test_segments_cross(self):
        base1 = (7, 1)
        base2 = (11, 1)

        point1 = (8, 2)
        point2 = (8, 0)
        self.assertTrue(segments_cross((base1, base2), (point1, point2)))

        # point1 = (8, 2)
        # point2 = (8, 1)
        # self.assertFalse(segments_cross((base1, base2), (point1, point2)))

        # point1 = (7, 2)
        # point2 = (7, 0)
        # self.assertFalse(segments_cross((base1, base2), (point1, point2)))

        # point1 = (11, 2)
        # point2 = (11, 0)
        # self.assertFalse(segments_cross((base1, base2), (point1, point2)))

        base1 = (1, 7)
        base2 = (1, 11)

        point1 = (2, 8)
        point2 = (0, 8)
        self.assertTrue(segments_cross((base1, base2), (point1, point2)))

        # point1 = (2, 7)
        # point2 = (0, 7)
        # self.assertFalse(segments_cross((base1, base2), (point1, point2)))

    def test_build_polygon(self):
        red_tiles = parse_input("test_input.txt")
        self.assertEqual([
            ((7, 1), (11, 1)),
            ((11, 1), (11, 7)),
            ((11, 7), (9, 7)),
            ((9, 7), (9, 5)),
            ((9, 5), (2, 5)),
            ((2, 5), (2, 3)),
            ((2, 3), (7, 3)),
        ], build_polygon(red_tiles))

    def test_build_rectangle_from_corners(self):
        corner1 = (2, 5)
        corner2 = (9, 7)
        self.assertEqual([
            ((2, 5), (9, 5)),
            ((9, 5), (9, 7)),
            ((9, 7), (2, 7)),
            ((2, 7), (2, 5)),
        ], build_rectangle_from_corners(corner1, corner2))

        corner1 = (2, 5)
        corner2 = (11, 1)
        self.assertEqual([
            ((2, 5), (11, 5)),
            ((11, 5), (11, 1)),
            ((11, 1), (2, 1)),
            ((2, 1), (2, 5)),
        ], build_rectangle_from_corners(corner1, corner2))

    def test_crosses_polygon(self):
        red_tiles = parse_input("test_input.txt")
        polygon = build_polygon(red_tiles)

        rectangle = build_rectangle_from_corners((2,5), (11, 1))
        self.assertTrue(crosses_polygon(polygon, rectangle))

        rectangle = build_rectangle_from_corners((9,5), (2, 3))
        self.assertFalse(crosses_polygon(polygon, rectangle))

    def test_get_largest_rectangle_not_crossing_polygon(self):
        red_tiles = parse_input("test_input.txt")
        polygon = build_polygon(red_tiles)
        area, rectangle = get_largest_rectangle_not_crossing_polygon(polygon, red_tiles)
        self.assertEqual([
            ((9, 5), (2, 5)),
            ((2, 5), (2, 3)),
            ((2, 3), (9, 3)),
            ((9, 3), (9, 5)),
        ], rectangle)
        self.assertEqual(24, area)

    def test_get_midpoint(self):
        corner1 = (11, 1)
        corner2 = (2, 3)

        self.assertEqual((6.5, 2.0), get_midpoint(corner1, corner2))

    def test_point_inside_polygon(self):
        red_tiles = parse_input("test_input.txt")
        polygon = build_polygon(red_tiles)

        corner1 = (11, 1)
        corner2 = (2, 3)
        midpoint = get_midpoint(corner1, corner2)

        self.assertFalse(point_inside_polygon(polygon, midpoint))

        corner1 = (11, 3)
        corner2 = (2, 5)
        midpoint = get_midpoint(corner1, corner2)
        self.assertTrue(point_inside_polygon(polygon, midpoint))

        polygon = [((1,1), (1, 100))]
        point = (1, 5)
        self.assertTrue(point_inside_polygon(polygon, point))

    def test_point_on_segment(self):
        polygon = [((1,1), (1, 100))]
        point = (1, 5)
        self.assertTrue(point_on_segment(polygon[0], point))

    def test_print_polygon(self):
        polygon = [((1,1), (1, 100))]
        self.assertEqual()



# unittest.main()

red_tiles = parse_input("input.txt")
polygon = build_polygon(red_tiles)
area, rectangle = get_largest_rectangle_not_crossing_polygon(polygon, red_tiles)

# Too low: 1574349244
print("Largest area possible:", area)
