import unittest
import pdb

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

def ranges_overlap(r1, r2):
    return r2[0] >= r1[0] and r2[0] <= r1[-1]

def reconcile_ranges(ranges):
    ranges = sort_ranges(ranges)

    i = 0
    while(i < len(ranges) - 1):
        while ranges_overlap(ranges[i], ranges[i+1]):

            ranges[i] = combine_ranges(ranges[i], ranges[i+1])
            del(ranges[i+1])

            if i == len(ranges) - 1:
                break

        i += 1
    
    return ranges

def combine_ranges(r1, r2):
    start = min([r1[0], r2[0]])
    end = max([r1[-1], r2[-1]]) + 1
    return range(start, end)

def sort_ranges(ranges):
    return sorted(ranges, key=lambda r: r[0])

def count_in_ranges(ranges):
    total = 0
    for r in ranges:
        total += r[-1]+1 - r[0]

    return total

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

    def test_reconcile_ranges(self):
        ranges, _ = parse_ranges_and_available("test_input.txt")

        self.assertEqual([
            range(3, 6),
            range(10, 21),
        ], reconcile_ranges(ranges))

        ranges, _ = parse_ranges_and_available("test4_input.txt")

        self.assertEqual([
            range(1, 7),
        ], reconcile_ranges(ranges))

    def test_combine_ranges(self):
        r1 = range(10, 15)
        r2 = range(12, 19)
        self.assertEqual(range(10, 19), combine_ranges(r1, r2))

        r1 = range(3, 6)
        r2 = range(3, 5)
        self.assertEqual(range(3, 6), combine_ranges(r1, r2))

    def test_ranges_overlap(self):
        r1 = range(10, 15)
        r2 = range(12, 19)
        self.assertTrue(ranges_overlap(r1, r2))

        r1 = range(3, 6)
        r2 = range(4, 5)
        self.assertTrue(ranges_overlap(r1, r2))

        r1 = range(3, 6)
        r2 = range(3, 5)
        self.assertTrue(ranges_overlap(r1, r2))

        r1 = range(3, 6)
        r2 = range(10, 15)
        self.assertFalse(ranges_overlap(r1, r2))

        r1 = range(3, 6)
        r2 = range(10, 15)
        self.assertFalse(ranges_overlap(r1, r2))


    def test_sort_ranges(self):
        ranges, _ = parse_ranges_and_available("test_input.txt")

        self.assertEqual([
            range(3, 6),
            range(10, 15),
            range(12, 19),
            range(16, 21),
        ], sort_ranges(ranges))

    def test_get_count_in_ranges(self):
        ranges, _ = parse_ranges_and_available("test_input.txt")
        ranges = reconcile_ranges(ranges)
        print(ranges)
        self.assertEqual(14, count_in_ranges(ranges))

        ranges, _ = parse_ranges_and_available("test2_input.txt")
        ranges = reconcile_ranges(ranges)
        self.assertEqual(7, count_in_ranges(ranges))

        ranges, _ = parse_ranges_and_available("test3_input.txt")
        ranges = reconcile_ranges(ranges)
        print(ranges)
        self.assertEqual(12, count_in_ranges(ranges))




# unittest.main()

ranges, available = parse_ranges_and_available("input.txt")
ranges = reconcile_ranges(ranges)
count = count_in_ranges(ranges)

# 300293422924867 too low
# 327282643062114 too low
# 361788656151615 not correct
print("Fresh count:", count)
