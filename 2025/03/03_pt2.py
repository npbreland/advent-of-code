import unittest
import pdb

def get_maximum_joltage(bank, n_batteries):

    # Return the sequence of n batteries with the highest voltage (must retain order)
    def aux(places_after, acc, start):
        # Base case - length of accumulator equals the number of batteries
        if len(acc) == n_batteries:
            return int(acc)

        # Recursive case: get highest digit within bounds
        highest = None
        highest_index = None

        for i in range(start, len(bank)-places_after):
            int_digit = int(bank[i])
            if highest is None:
                highest = int_digit
                highest_index = i
            elif int_digit > highest:
                highest = int_digit
                highest_index = i

        # Update accumulator
        acc += str(highest)

        # Update bounds for next iteration
        places_after = 0 if places_after == 0 else places_after - 1

        return aux(places_after, acc, highest_index+1)

    return aux(n_batteries-1, "", 0)

class MyTest(unittest.TestCase):
    def test_get_maximum_joltage(self):
        bank = "987654321111111"
        self.assertEqual(98, get_maximum_joltage(bank, 2))

        bank = "811111111111119"
        self.assertEqual(89, get_maximum_joltage(bank, 2))

        bank = "234234234234278"
        self.assertEqual(78, get_maximum_joltage(bank, 2))

        bank = "818181911112111"
        self.assertEqual(92, get_maximum_joltage(bank, 2))

        # Twelves
        bank = "987654321111111"
        self.assertEqual(987654321111, get_maximum_joltage(bank, 12))

        bank = "811111111111119"
        self.assertEqual(811111111119, get_maximum_joltage(bank, 12))

        bank = "234234234234278"
        self.assertEqual(434234234278, get_maximum_joltage(bank, 12))

        bank = "818181911112111"
        self.assertEqual(888911112111, get_maximum_joltage(bank, 12))

        # Fours
        bank = "987654321111111"
        self.assertEqual(9876, get_maximum_joltage(bank, 4))

        bank = "811111111111119"
        self.assertEqual(8119, get_maximum_joltage(bank, 4))

        bank = "234234234234278"
        self.assertEqual(4478, get_maximum_joltage(bank, 4))

        bank = "818181911112111"
        self.assertEqual(9211, get_maximum_joltage(bank, 4))


unittest.main()

total_joltage = 0
with open("input.txt", "r") as file:
    for line in file:
        total_joltage += get_maximum_joltage(line.rstrip(), 12)

print("Total output joltage:", total_joltage)

