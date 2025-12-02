import unittest
import re

def id_is_invalid(id):
    pattern = re.compile(r"([0-9]+)\1")
    return pattern.fullmatch(id)

def make_range(range_string):
    split = range_string.split("-")
    start = int(split[0])
    end = int(split[1]) + 1
    return range(start, end)

def make_id_list(content):
    return content.split(",")

def get_invalid_ids(content):
    id_list = make_id_list(content)
    invalid_ids = []
    for id_range_string in id_list:
        id_range = make_range(id_range_string)

        for id in id_range:
            if id_is_invalid(str(id)):
                invalid_ids.append(id)

    return invalid_ids

def sum_invalid_ids(content):
    return sum(get_invalid_ids(content))

class MyTest(unittest.TestCase):

    def test_id_is_invalid_true(self):
        id = "11"
        self.assertTrue(id_is_invalid(id))

        id = "123123"
        self.assertTrue(id_is_invalid(id))

    def test_id_is_invalid_false(self):
        id = "12"
        self.assertFalse(id_is_invalid(id))

        id = "101"
        self.assertFalse(id_is_invalid(id))

        id = "1995"
        self.assertFalse(id_is_invalid(id))

        id = "111"
        self.assertFalse(id_is_invalid(id))

    def test_make_id_range(self):
        range_string = "11-22"
        id_range = make_range(range_string)
        # Range excludes the "stop" index
        self.assertEqual(range(11, 23), id_range)

        range_string = "998-1012"
        id_range = make_range(range_string)
        self.assertEqual(range(998, 1013), id_range)

    def test_make_id_list(self):
        content = "11-22,998-1012"
        ids = make_id_list(content)
        # Range excludes the "stop" index
        self.assertEqual(["11-22", "998-1012"], ids)

    def test_get_invalid_ids(self):
        content = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
        invalid_ids = get_invalid_ids(content)
        self.assertEqual([
            11, 22, 99, 1010,
            1188511885, 222222,
            446446, 38593859
        ], invalid_ids)

    def test_sum_invalid_ids(self):
        content = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
        self.assertEqual(1227775554, sum_invalid_ids(content))

# unittest.main()

with open("input.txt", "r") as file:
    content = file.read()
    answer = sum_invalid_ids(content)
    print("Sum invalid IDs:", answer)





