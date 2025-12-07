import unittest
import pdb

class Game:
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = [line for line in file]

        self.beam_cols = []
        self.current = 0
        self.splits = 0

    def find_start_point(self):
        first_line = self.lines[0]
        return first_line.find("S")

    def find_splitters(self, line):
        indices = []

        index = 0
        while index != -1:
            index = self.lines[line].find("^", index)
            
            if index != -1:
                indices.append(index)
                index += 1

        return indices

    def start_beam(self):
        start_col = self.find_start_point()
        
        self.beam_cols = []

        if start_col not in self.find_splitters(1):
            self.beam_cols = [start_col]

    def next_line(self):
        self.current += 1
        if self.current == len(self.lines):
            return False

        new_beam_cols = []
        splitters = self.find_splitters(self.current)
        for col in self.beam_cols:
            if col in splitters:
                new_beam_cols.extend([col-1, col+1])
                self.splits += 1
            else:
                new_beam_cols.append(col)

        self.beam_cols = sorted(list(set(new_beam_cols)))

        return True

    def play_game(self):
        self.start_beam()
        next = True
        while next:
            next = self.next_line()

        

        




class MyTest(unittest.TestCase):
    def test_init(self):
        game = Game("test_input.txt")
        self.assertEqual("S", game.lines[0][7])

    def test_find_start_point(self):
        game = Game("test_input.txt")
        self.assertEqual(7, game.find_start_point())

    def test_find_splitters(self):
        game = Game("test_input.txt")
        self.assertEqual([], game.find_splitters(1))
        self.assertEqual([7], game.find_splitters(2))

        self.assertEqual([6, 8], game.find_splitters(4))

    def test_start_beam(self):
        game = Game("test_input.txt")
        game.start_beam()
        self.assertEqual(7, game.beam_cols[0])

    def test_next_line(self):
        game = Game("test_input.txt")
        game.start_beam()

        game.next_line()
        game.next_line()
        
        self.assertEqual(1, game.splits)
        self.assertEqual([6, 8], game.beam_cols)

        game.next_line()
        self.assertEqual(1, game.splits)
        self.assertEqual([6, 8], game.beam_cols)

        game.next_line()
        self.assertEqual(3, game.splits)
        self.assertEqual([5, 7, 9], game.beam_cols)

        game.next_line()
        self.assertEqual(3, game.splits)
        self.assertEqual([5, 7, 9], game.beam_cols)

        game.next_line()
        self.assertEqual(6, game.splits)
        self.assertEqual([4, 6, 8, 10], game.beam_cols)

    def test_play_game(self):
        game = Game("test_input.txt")
        game.play_game()
        self.assertEqual(21, game.splits)

# unittest.main()

game = Game("input.txt")
game.play_game()
print("Splits:", game.splits)

