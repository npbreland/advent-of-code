import unittest
import math
import pdb

def parse_instruction_line(line):
    direction = line[0]
    clicks = int(line[1:])
    return direction, clicks

def right_turn(position, clicks):
    position += clicks
    return position

def left_turn(position, clicks):
    position -= clicks
    return position

def correct_position(position):
    return position % 100

def move(position, direction, clicks):
    if direction == "L":
        position = left_turn(position, clicks)
    elif direction == "R":
        position = right_turn(position, clicks)

    position = correct_position(position)
    return position


def count_zero_hits(position, direction, clicks):
    if direction == "L":
        new_position = left_turn(position, clicks)
    elif direction == "R":
        new_position = right_turn(position, clicks)


    if position == 0 and abs(new_position) < 100:
        return 0

    if new_position == 0:
        return 1

    if new_position > 0 and new_position < 100:
        return 0

    if new_position < 0:
        new_position = abs(new_position)
        zero_hits = math.ceil(new_position / 100)
        if move(position, direction, clicks) == 0 and position != 0:
            zero_hits += 1
        return zero_hits
    else:
        zero_hits = new_position // 100
        return zero_hits


class MyTest(unittest.TestCase):
    def test_parse_instruction_line_1_digit(self):
        line = "L5"
        direction, clicks = parse_instruction_line(line)
        self.assertEqual("L", direction)
        self.assertEqual(5, clicks)

    def test_parse_instruction_line_2_digits(self):
        line = "R18"
        direction, clicks = parse_instruction_line(line)
        self.assertEqual("R", direction)
        self.assertEqual(18, clicks)

    def test_parse_instruction_line_3_digits(self):
        line = "L168"
        direction, clicks = parse_instruction_line(line)
        self.assertEqual("L", direction)
        self.assertEqual(168, clicks)

    def test_right_turn_advances_position(self):
        position = 50
        position = right_turn(50, 20)
        self.assertEqual(70, position)

    def test_correct_position_over_100(self):
        position = 150
        position = correct_position(position)
        self.assertEqual(50, position)

    def test_correct_position_over_200(self):
        position = 250
        position = correct_position(position)
        self.assertEqual(50, position)

    def test_correct_position_under_200(self):
        position = -230
        position = correct_position(position)
        self.assertEqual(70, position)

    def test_correct_position_under_0(self):
        position = -20
        position = correct_position(-20)
        self.assertEqual(80, position)

    def test_correct_position_100(self):
        position = 100
        position = correct_position(100)
        self.assertEqual(0, position)

    def test_left_turn_reverses_position(self):
        position = 50
        position = left_turn(position, 20)
        self.assertEqual(30, position)

    def test_instructions(self):
        position = 50
        timesDialAtZero = 0

        direction, clicks = parse_instruction_line("L68")
        position = move(position, direction, clicks)
        self.assertEqual(82, position)

        direction, clicks = parse_instruction_line("L30")
        position = move(position, direction, clicks)
        self.assertEqual(52, position)

        direction, clicks = parse_instruction_line("R48")
        position = move(position, direction, clicks)
        self.assertEqual(0, position)
        timesDialAtZero += 1
        
        direction, clicks = parse_instruction_line("L5")
        position = move(position, direction, clicks)
        self.assertEqual(95, position)

        direction, clicks = parse_instruction_line("R60")
        position = move(position, direction, clicks)
        self.assertEqual(55, position)

        direction, clicks = parse_instruction_line("L55")
        position = move(position, direction, clicks)
        self.assertEqual(0, position)
        timesDialAtZero += 1

        direction, clicks = parse_instruction_line("L1")
        position = move(position, direction, clicks)
        self.assertEqual(99, position)

        direction, clicks = parse_instruction_line("L99")
        position = move(position, direction, clicks)
        self.assertEqual(0, position)
        timesDialAtZero += 1

        direction, clicks = parse_instruction_line("R14")
        position = move(position, direction, clicks)
        self.assertEqual(14, position)

        direction, clicks = parse_instruction_line("L82")
        position = move(position, direction, clicks)
        self.assertEqual(32, position)

        self.assertEqual(timesDialAtZero, 3)

    # Part 2
    def test_count_zero_hits(self):
        position = 50

        direction, clicks = parse_instruction_line("L68")
        zero_hits = count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(1, zero_hits)
        self.assertEqual(82, position)

        direction, clicks = parse_instruction_line("L30")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(1, zero_hits)
        self.assertEqual(52, position)

        direction, clicks = parse_instruction_line("R48")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(2, zero_hits)
        self.assertEqual(0, position)

        direction, clicks = parse_instruction_line("L5")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(2, zero_hits)
        self.assertEqual(95, position)

        direction, clicks = parse_instruction_line("R60")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(3, zero_hits)
        self.assertEqual(55, position)

        direction, clicks = parse_instruction_line("L55")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(4, zero_hits)
        self.assertEqual(0, position)

        direction, clicks = parse_instruction_line("L1")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(4, zero_hits)
        self.assertEqual(99, position)

        direction, clicks = parse_instruction_line("L99")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(5, zero_hits)
        self.assertEqual(0, position)

        direction, clicks = parse_instruction_line("R14")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(5, zero_hits)
        self.assertEqual(14, position)

        direction, clicks = parse_instruction_line("L82")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(6, zero_hits)
        self.assertEqual(32, position)

        position = 0
        zero_hits = 0
        direction, clicks = parse_instruction_line("R853")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(53, position)
        self.assertEqual(8, zero_hits)

        position = 2
        zero_hits = 0
        direction, clicks = parse_instruction_line("L796")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(6, position)
        self.assertEqual(8, zero_hits)

        position = 52
        zero_hits = 0
        direction, clicks = parse_instruction_line("L752")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(0, position)
        self.assertEqual(8, zero_hits)

        position = 52
        zero_hits = 0
        direction, clicks = parse_instruction_line("L752")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(0, position)
        self.assertEqual(8, zero_hits)
        
        position = 15
        zero_hits = 0
        direction, clicks = parse_instruction_line("L717")
        zero_hits += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        self.assertEqual(98, position)
        self.assertEqual(8, zero_hits)

# unittest.main()

# Part 1
position = 50
timesDialAtZero = 0
with open("input.txt", "r") as file:
    for line in file:
        direction, clicks = parse_instruction_line(line)
        position = move(position, direction, clicks)

        if position == 0:
            timesDialAtZero += 1

print("Password (number of times pointing at 0):", timesDialAtZero)

# Part 2
position = 50
timesDialAtZero = 0
with open("input.txt", "r") as file:
    for line in file:
        direction, clicks = parse_instruction_line(line)
        timesDialAtZero += count_zero_hits(position, direction, clicks)
        position = move(position, direction, clicks)
        print(line, position, timesDialAtZero)

print("Password (number of times pointing at 0):", timesDialAtZero)
