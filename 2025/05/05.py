import unittest

def parse_ranges_and_available(filename):
    ranges = []
    available = []
    with open(filename, "r") as file:
        for line in file:
            if line.rstrip() == "":
                continue
            if "-" in line:
                split = line.rstrip().split("-")
                first = int(split[0])
                second = int(split[1])
                ranges.append(range(first, second+1))
            else:
                available.append(int(line.rstrip()))

    return ranges, available
    
def get_fresh_ids(ranges, available):
    ids = []
    for item in available:
        for r in ranges:
            if item in r:
                ids.append(item)

    return list(set(ids))


class MyTest(unittest.TestCase):
    def test_parse_ranges(self):
        ranges, available = parse_ranges_and_available("test_input.txt")
        self.assertEqual([
            range(3, 6),
            range(10, 15),
            range(16, 21),
            range(12, 19),
        ], ranges)

        self.assertEqual([1,5,8,11,17,32], available)

    def test_get_fresh_ids(self):
        ranges, available = parse_ranges_and_available("test_input.txt")

        fresh_ids = get_fresh_ids(ranges, available)
        self.assertEqual(set([5, 11, 17]), set(fresh_ids))

# unittest.main()

ranges, available = parse_ranges_and_available("input.txt")

fresh_ids = get_fresh_ids(ranges, available)

print("Fresh count:", len(fresh_ids))
