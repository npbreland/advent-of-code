import unittest

def get_maximum_joltage(bank):
    # Find the highest digit in the bank, excluding the last

    bank_less_1 = bank[:-1]

    highest = None
    highest_index = None
    for i, digit in enumerate(bank_less_1):
        int_digit = int(digit)
        if highest is None:
            highest = int_digit
            highest_index = i
        elif int_digit > highest:
            highest = int_digit
            highest_index = i

    # Find the second highest digit in the bank AFTER the highest_index

    bank_from_highest = bank[highest_index+1:]

    second_highest = None
    for digit in bank_from_highest:
        int_digit = int(digit)
        if second_highest is None:
            second_highest = int_digit
        elif int_digit > second_highest:
            second_highest = int_digit

    # Concatenate digits and cast as int

    return int(str(highest) + str(second_highest))


class MyTest(unittest.TestCase):
    def test_get_maximum_joltage(self):
        bank = "987654321111111"
        self.assertEqual(98, get_maximum_joltage(bank))

        bank = "811111111111119"
        self.assertEqual(89, get_maximum_joltage(bank))

        bank = "234234234234278"
        self.assertEqual(78, get_maximum_joltage(bank))

        bank = "818181911112111"
        self.assertEqual(92, get_maximum_joltage(bank))


# unittest.main()

total_joltage = 0
with open("input.txt", "r") as file:
    for line in file:
        total_joltage += get_maximum_joltage(line.rstrip())

print("Total output joltage:", total_joltage)

