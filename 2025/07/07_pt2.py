import unittest

class Game:
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = [line for line in file]

        self.heads = {}
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
        
        if start_col not in self.find_splitters(1):
            self.heads[start_col] = 1

    def next_line(self):
        self.current += 1
        if self.current == len(self.lines):
            return False

        splitters = self.find_splitters(self.current)

        new_heads = {}
        for head, count in self.heads.items():
            if head in splitters:
                l = head - 1
                r = head + 1

                if l in new_heads:
                    new_heads[l] += count
                else:
                    new_heads[l] = count

                if r in new_heads:
                    new_heads[r] += count
                else:
                    new_heads[r] = count
            else:
                if head in new_heads:
                    new_heads[head] += count
                else:
                    new_heads[head] = count

        self.heads = new_heads
        
        return True

    def count_timelines(self):
        return sum(self.heads.values())

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
        self.assertEqual([7], list(game.heads.keys()))

    def test_next_line(self):
        game = Game("test_input.txt")
        game.start_beam()

        game.next_line()
        game.next_line()
        
        self.assertEqual([6, 8], list(game.heads))
        self.assertEqual(2, game.count_timelines())

        game.next_line()
        self.assertEqual([6, 8], list(game.heads))
        self.assertEqual(2, game.count_timelines())

        game.next_line()
        self.assertEqual([5, 7, 9], list(game.heads))
        self.assertEqual(4, game.count_timelines())

        game.next_line()
        self.assertEqual([5, 7, 9], list(game.heads))
        self.assertEqual(4, game.count_timelines())

        game.next_line()
        self.assertEqual([4, 6, 8, 10], list(game.heads))
        self.assertEqual(8, game.count_timelines())

    def test_play_game(self):
        game = Game("test_input.txt")
        game.play_game()
        self.assertEqual(40, game.count_timelines())


#unittest.main()

game = Game("input.txt")
game.play_game()
print("Timelines:", game.count_timelines())

