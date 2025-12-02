import unittest
import pdb

def parse_instruction_line(line):
    direction = line[0]
    clicks = int(line[1:])
    return direction, clicks

def right_turn(current, clicks):
    for i in range(clicks):
        current = current.next

    return current

def left_turn(current, clicks):
    for i in range(clicks):
        current = current.previous

    return current

def move(current, direction, clicks):
    if direction == "L":
        new = left_turn(current, clicks)
    elif direction == "R":
        new = right_turn(current, clicks)

    return new

class Node:
    def __init__(self, number):
        self.number = number
        self.previous = None
        self.next = None

nodes = [Node(i) for i in range(100)]

nodes[0].previous = nodes[99]
nodes[0].next = nodes[1]

for i in range(1,99):
    nodes[i].next = nodes[i+1]
    nodes[i].previous = nodes[i-1]

nodes[99].next = nodes[0]
nodes[99].previous = nodes[98]

# print("Node\tNext\tPrevious")
# for node in nodes:
#     print(f"{node.number}\t{node.next.number}\t{node.previous.number}")

class ZeroCounter:
    def __init__(self, nodes):
        self.nodes = nodes
        self.current = None
        self.count = 0

    def get_count(self):
        return self.count

    def set_current(self, node):
        self.current = node

    def increment_if_zero(self):
        if self.current.number == 0:
            self.count += 1

    def right_turn(self, clicks):
        for i in range(clicks):
            self.set_current(self.current.next)
            self.increment_if_zero()

    def left_turn(self, clicks):
        for i in range(clicks):
            self.set_current(self.current.previous)
            self.increment_if_zero()

    def turn(self, direction, clicks):
        if direction == "L":
            self.left_turn(clicks)
        elif direction == "R":
            self.right_turn(clicks)


class MyTest(unittest.TestCase):
    def test_parse_instruction_line_3_digits(self):
        line = "L168"
        direction, clicks = parse_instruction_line(line)
        self.assertEqual("L", direction)
        self.assertEqual(168, clicks)

    def test_parse_instruction_line_2_digits(self):
        line = "R18"
        direction, clicks = parse_instruction_line(line)
        self.assertEqual("R", direction)
        self.assertEqual(18, clicks)

    def test_parse_instruction_line_1_digit(self):
        line = "L5"
        direction, clicks = parse_instruction_line(line)
        self.assertEqual("L", direction)
        self.assertEqual(5, clicks)

    def test_right_turn_advances_position(self):
        current = nodes[50]
        new = right_turn(current, 20)
        self.assertEqual(new.number, 70)

    def test_left_turn_reverses_position(self):
        current = nodes[50]
        new = left_turn(current, 20)
        self.assertEqual(30, new.number)

    def test_instructions(self):
        current = nodes[50]
        timesDialAtZero = 0

        direction, clicks = parse_instruction_line("L68")
        current = move(current, direction, clicks)
        self.assertEqual(82, current.number)

        direction, clicks = parse_instruction_line("L30")
        current = move(current, direction, clicks)
        self.assertEqual(52, current.number)

        direction, clicks = parse_instruction_line("R48")
        current = move(current, direction, clicks)
        self.assertEqual(0, current.number)
        timesDialAtZero += 1
        
        direction, clicks = parse_instruction_line("L5")
        current = move(current, direction, clicks)
        self.assertEqual(95, current.number)

        direction, clicks = parse_instruction_line("R60")
        current = move(current, direction, clicks)
        self.assertEqual(55, current.number)

        direction, clicks = parse_instruction_line("L55")
        current = move(current, direction, clicks)
        self.assertEqual(0, current.number)
        timesDialAtZero += 1

        direction, clicks = parse_instruction_line("L1")
        current = move(current, direction, clicks)
        self.assertEqual(99, current.number)

        direction, clicks = parse_instruction_line("L99")
        current = move(current, direction, clicks)
        self.assertEqual(0, current.number)
        timesDialAtZero += 1

        direction, clicks = parse_instruction_line("R14")
        current = move(current, direction, clicks)
        self.assertEqual(14, current.number)

        direction, clicks = parse_instruction_line("L82")
        current = move(current, direction, clicks)
        self.assertEqual(32, current.number)

        self.assertEqual(timesDialAtZero, 3)

    def test_count_zero_hits(self):
        counter = ZeroCounter(nodes)
        counter.set_current(nodes[50])

        direction, clicks = parse_instruction_line("L68")
        counter.turn(direction, clicks)
        self.assertEqual(1, counter.get_count())
        self.assertEqual(82, counter.current.number)

        direction, clicks = parse_instruction_line("L30")
        counter.turn(direction, clicks)
        self.assertEqual(1, counter.get_count())
        self.assertEqual(52, counter.current.number)

        direction, clicks = parse_instruction_line("R48")
        counter.turn(direction, clicks)
        self.assertEqual(2, counter.get_count())
        self.assertEqual(0, counter.current.number)

        direction, clicks = parse_instruction_line("L5")
        counter.turn(direction, clicks)
        self.assertEqual(2, counter.get_count())
        self.assertEqual(95, counter.current.number)
        
        direction, clicks = parse_instruction_line("R60")
        counter.turn(direction, clicks)
        self.assertEqual(3, counter.get_count())
        self.assertEqual(55, counter.current.number)

        direction, clicks = parse_instruction_line("L55")
        counter.turn(direction, clicks)
        self.assertEqual(4, counter.get_count())
        self.assertEqual(0, counter.current.number)

        direction, clicks = parse_instruction_line("L1")
        counter.turn(direction, clicks)
        self.assertEqual(4, counter.get_count())
        self.assertEqual(99, counter.current.number)
        
        direction, clicks = parse_instruction_line("L99")
        counter.turn(direction, clicks)
        self.assertEqual(5, counter.get_count())
        self.assertEqual(0, counter.current.number)

        direction, clicks = parse_instruction_line("R14")
        counter.turn(direction, clicks)
        self.assertEqual(5, counter.get_count())
        self.assertEqual(14, counter.current.number)

        direction, clicks = parse_instruction_line("L82")
        counter.turn(direction, clicks)
        self.assertEqual(6, counter.get_count())
        self.assertEqual(32, counter.current.number)


current = nodes[50]
timesDialAtZero = 0
with open("input.txt", "r") as file:
    for line in file:
        direction, clicks = parse_instruction_line(line)
        current = move(current, direction, clicks)

        if current.number == 0:
            timesDialAtZero += 1

print("Password (number of times pointing at 0):", timesDialAtZero)

# Part 2
counter = ZeroCounter(nodes)
counter.set_current(nodes[50])

with open("input.txt", "r") as file:
    for line in file:
        direction, clicks = parse_instruction_line(line)
        counter.turn(direction, clicks)

print("Password (number of times pointing at 0):", counter.get_count())
