import unittest
import re
import math
import pdb


class Homework:

    def __init__(self, filename):
        with open(filename, "r") as file:
            self.rows = [row[:-1] for row in file]

    def get_operator_row(self):
        return re.findall("[*+]", self.rows[-1])

    def get_problems(self):
        problem_rows = self.rows[:-1]

        problems = []
        problem = []
        for i in range(len(problem_rows[0]) - 1, -1, -1):
            number = ""
            for row in problem_rows:
                number += row[i]

            if re.findall("^\s+$", number):
                problems.append(problem)
                problem = []
            else:
                number = int(number)
                problem.append(number)

        problems.append(problem)

        self.problems = problems

        return problems


    def complete_problems(self):
        answers = []
        problems = [p for p in reversed(self.problems)]
        for i, operator in enumerate(self.get_operator_row()):
            if operator == "+":
                answers.append(sum(problems[i]))
            elif operator == "*":
                answers.append(math.prod(problems[i]))

        return answers

    def check(self, answers):
        return sum(answers)
        

class MyTest(unittest.TestCase):
    # def test_read_input(self):
    #     hw = Homework("test_input.txt")
    #     print(hw.rows)
    #     self.assertEqual(4, len(hw.rows))
    #     self.assertEqual("*", hw.rows[3][0])

    def test_get_operator_row(self):
        hw = Homework("test_input.txt")
        operator_row = hw.get_operator_row()
        self.assertEqual("*", operator_row[0])

    def test_get_problems(self):
        hw = Homework("test_input.txt")
        problems = hw.get_problems()
        self.assertEqual([
            [4, 431, 623],
            [175, 581, 32],
            [8, 248, 369],
            [356, 24, 1],
        ], problems)

    def test_complete_problems(self):
        hw = Homework("test_input.txt")
        hw.get_problems()
        answers = hw.complete_problems()
        self.assertEqual([8544, 625, 3253600, 1058], answers)

    def test_check(self):
        hw = Homework("test_input.txt")
        hw.get_problems()
        answers = hw.complete_problems()
        self.assertEqual(3263827, hw.check(answers))
        


# unittest.main()

hw = Homework("input.txt")
hw.get_problems()
answers = hw.complete_problems()
print("Check value:", hw.check(answers))
