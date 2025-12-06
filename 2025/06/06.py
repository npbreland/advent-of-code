import unittest
import re
import math


class Homework:

    def __init__(self, filename):
        self.rows = []
        with open(filename, "r") as file:
            self.rows = [row.rstrip() for row in file]

    def get_operator_row(self):
        return re.findall("[*+]", self.rows[-1])

    def transpose_cols_into_problems(self):
        self.problems = []
        for row in self.rows:
            numbers = re.findall("[0-9]+", row)
            for i, number in enumerate(numbers):
                # Start a new problem if it's not there
                if len(self.problems) == i:
                    self.problems.append([])

                self.problems[i].append(int(number))

    def complete_problems(self):
        answers = []
        for i, operator in enumerate(self.get_operator_row()):
            if operator == "+":
                answers.append(sum(self.problems[i]))
            elif operator == "*":
                answers.append(math.prod(self.problems[i]))

        return answers

    def check(self, answers):
        return sum(answers)
        

class MyTest(unittest.TestCase):
    def test_read_input(self):
        hw = Homework("test_input.txt")
        self.assertEqual(4, len(hw.rows))
        self.assertEqual("*", hw.rows[3][0])

    def test_get_operator_row(self):
        hw = Homework("test_input.txt")
        operator_row = hw.get_operator_row()
        self.assertEqual("*", operator_row[0])

    def test_transpose_cols_into_problems(self):
        hw = Homework("test_input.txt")
        hw.transpose_cols_into_problems()
        self.assertEqual([123, 45, 6], hw.problems[0])
        self.assertEqual([64, 23, 314], hw.problems[-1])

    def test_complete_problems(self):
        hw = Homework("test_input.txt")
        hw.transpose_cols_into_problems()
        answers = hw.complete_problems()
        self.assertEqual([33210, 490, 4243455, 401], answers)

    def test_check(self):
        hw = Homework("test_input.txt")
        hw.transpose_cols_into_problems()
        answers = hw.complete_problems()
        self.assertEqual(4277556, hw.check(answers))
        


# unittest.main()

hw = Homework("input.txt")
hw.transpose_cols_into_problems()
answers = hw.complete_problems()
print("Check value:", hw.check(answers))
