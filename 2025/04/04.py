import unittest
import pdb


class Grid:

    def __init__(self, filename):
        self.grid = []
        
        with open(filename, "r") as file:
            for line in file:
                self.grid.append(list(line.rstrip()))

    def get_adjacent_spaces(self, x, y):
        a = (x - 1, y - 1)
        b = (x, y - 1)
        c = (x + 1, y - 1)
        d = (x + 1, y)
        e = (x + 1, y + 1)
        f = (x, y + 1)
        g = (x - 1, y + 1)
        h = (x - 1, y)
        positions = [a, b, c, d, e, f, g, h]
        positions = [p for p in positions if p[0] >= 0 and p[1] >= 0]
        positions = [p for p in positions if p[0] < len(self.grid[0]) and p[1] < len(self.grid)]

        return positions

    def is_paper_roll(self, c):
        return c == "@"

    def get_adjacent_roll_count(self, x, y):
        adjacent_spaces = self.get_adjacent_spaces(x, y)
        total = 0
        for adj_x, adj_y in adjacent_spaces:
            if self.is_paper_roll(self.grid[adj_y][adj_x]):
                total += 1
        return total

    def get_accessible_rolls(self):
        total = 0
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if not self.is_paper_roll(self.grid[i][j]):
                    continue

                if self.get_adjacent_roll_count(j, i) < 4:
                    total += 1

        return total





class MyTest(unittest.TestCase):
    def test_create_grid(self):
        grid = Grid("test_input.txt")

        self.assertEqual(10, len(grid.grid))
        self.assertEqual(10, len(grid.grid[0]))
        self.assertEqual("@", grid.grid[0][2])
        self.assertEqual(".", grid.grid[0][9])

    def test_get_adjacent_spaces(self):
        grid = Grid("test_input.txt")
        self.assertEqual(
            set([(1, 0), (0, 1), (1, 1)]),
            set(grid.get_adjacent_spaces(0, 0))
        )
        self.assertEqual(
            set([(8, 0), (9, 1), (8, 1)]),
            set(grid.get_adjacent_spaces(9, 0))
        )

    def test_is_paper_roll(self):
        grid = Grid("test_input.txt")
        self.assertTrue(grid.is_paper_roll("@"))
        self.assertFalse(grid.is_paper_roll("."))

    def test_get_adjacent_roll_count(self):
        grid = Grid("test_input.txt")
        self.assertEqual(3, grid.get_adjacent_roll_count(2, 0))
        self.assertEqual(3, grid.get_adjacent_roll_count(3, 0))
        self.assertEqual(3, grid.get_adjacent_roll_count(5, 0))

    def test_get_accessible_rolls(self):
        grid = Grid("test_input.txt")
        self.assertEqual(13, grid.get_accessible_rolls())
        



# unittest.main()
grid = Grid("input.txt")
print("Accessible rolls:", grid.get_accessible_rolls())
