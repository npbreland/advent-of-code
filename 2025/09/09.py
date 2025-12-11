import unittest
import itertools

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


    
# unittest.main()

corners = parse_input("input.txt")
area = get_largest_possible_rectangle(corners)
print("Largest area possible:", area)
