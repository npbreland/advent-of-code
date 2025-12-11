import unittest
import re
import pdb
import json
import pprint
import time

def parse_input(filename):
    nodes = {}
    with open(filename, "r") as file:
        for line in file:
            node_names = re.findall(r"[a-z]{3}", line)
            for name in node_names:
                if name not in nodes:
                    nodes[name] = Node(name)

            parent = node_names[0]
            parent_node = nodes[parent]

            child_nodes = [nodes[name] for name in node_names[1:]]
            parent_node.set_next(child_nodes)

    return nodes

class Node:
    def __init__(self, name):
        self.name = name
        self.next = []

    def __str__(self):
        return self.name

    def set_next(self, nexts):
        self.next = nexts

    def paths_to(self, dest, visited = [], paths = [], tracker = {}):
        visited.append(self)
        # print(self)
        # time.sleep(0.5)

        if self == dest:
            paths.append(visited.copy())
            for node in visited:
                if node.name not in tracker:
                    tracker[node.name] = 1
                else:
                    tracker[node.name] += 1
        elif len(self.next) == 0:
            for node in visited:
                if node.name not in tracker:
                    tracker[node.name] = 0
        else:
            for next in self.next:
                if next.name in tracker:
                    next_paths_count = tracker[next.name]
                    for node in visited:
                        if node.name not in tracker:
                            tracker[node.name] = next_paths_count
                        else:
                            tracker[node.name] += next_paths_count
                else:
                    next.paths_to(dest, visited, paths, tracker)

        # Cleanup
        visited.pop()

    # Didn't use this function - something not right about it
    def valid_paths_to(self, dest, visited = [], paths = [], tracker = {}, validTracker = {}, fftHit = False, dacHit = False):
        visited.append(self)
        # print([n.name for n in visited])

        print(self)

        if self.name == "fft":
            print("FFT")
            fftHit = True
        elif self.name == "dac":
            print("DAC")
            dacHit = True

        # print(fftHit, dacHit)
        if fftHit and dacHit:
            print([n.name for n in visited])
            print("BOTH")

        if self == dest:
            paths.append(visited.copy())
            for node in visited:
                if node.name not in tracker:
                    tracker[node.name] = 1
                else:
                    tracker[node.name] += 1

            if fftHit and dacHit:
                print("BOTH")
                for node in visited:
                    if node.name not in validTracker:
                        validTracker[node.name] = 1
                    else:
                        validTracker[node.name] += 1
        elif len(self.next) == 0:
            for node in visited:
                if node.name not in tracker:
                    tracker[node.name] = 0

                if node.name not in validTracker:
                    validTracker[node.name] = 0
        else:
            for next in self.next:
                if next.name in tracker:
                    next_paths_count = tracker[next.name]
                    for node in visited:
                        if node.name not in tracker:
                            tracker[node.name] = next_paths_count
                        else:
                            tracker[node.name] += next_paths_count

                        if fftHit and dacHit:
                            if node.name not in validTracker:
                                validTracker[node.name] = next_paths_count
                            else:
                                validTracker[node.name] += next_paths_count



                    # if next.name in validTracker:
                    #     valid_paths_count = validTracker[next.name]
                    #     for node in visited:

                    # if next.name in validTracker:
                    #     valid_paths_count = validTracker[next.name]
                    #     for node in visited:
                    #         if node.name not in validTracker:
                    #             validTracker[node.name] = valid_paths_count
                    #         else:
                    #             validTracker[node.name] += valid_paths_count
                else:
                    next.valid_paths_to(dest, visited, paths, tracker, validTracker, fftHit, dacHit)

        # Cleanup
        fftHit = False
        dacHit = False
        visited.pop()


def paths_visit_dac_and_fft(paths):
    valid = []
    for p in paths:
        names = [n.name for n in p]
        if "dac" in names and "fft" in names:
            valid.append(p)

    return valid

class MyTest(unittest.TestCase):
    def test_parse_input(self):
        nodes = parse_input("test_input.txt")
        self.assertTrue("you" in nodes)
        self.assertTrue("aaa" in nodes)
        self.assertTrue("bbb" in nodes)
        self.assertTrue("ccc" in nodes)
        self.assertTrue("ddd" in nodes)
        self.assertTrue("eee" in nodes)
        self.assertTrue("fff" in nodes)
        self.assertTrue("ggg" in nodes)
        self.assertTrue("hhh" in nodes)
        self.assertTrue("iii" in nodes)
        self.assertTrue("out" in nodes)

        self.assertEqual([nodes["bbb"], nodes["ccc"]], nodes["you"].next)
        self.assertEqual([nodes["you"], nodes["hhh"]], nodes["aaa"].next)
        self.assertEqual([nodes["ddd"], nodes["eee"]], nodes["bbb"].next)
        self.assertEqual([nodes["ddd"], nodes["eee"], nodes["fff"]], nodes["ccc"].next)
        self.assertEqual([nodes["ggg"]], nodes["ddd"].next)
        self.assertEqual([nodes["out"]], nodes["eee"].next)
        self.assertEqual([nodes["out"]], nodes["fff"].next)
        self.assertEqual([nodes["out"]], nodes["ggg"].next)
        self.assertEqual([nodes["ccc"], nodes["fff"], nodes["iii"]], nodes["hhh"].next)
        self.assertEqual([nodes["out"]], nodes["iii"].next)

    def test_paths_to(self):
        nodes = parse_input("test_input.txt")
        
        start = nodes["you"]

        visited = []
        paths = []
        tracker = {}
        start.paths_to(nodes["out"], visited, paths, tracker)

        self.assertEqual(5, tracker["you"])

    def test_valid_paths_to(self):
        nodes = parse_input("test_input_pt2.txt")
        
        start = nodes["svr"]
        visited = []
        paths = []
        tracker = {}
        validTracker = {}
        start.valid_paths_to(nodes["out"], visited, paths, tracker, validTracker)
        self.assertEqual(2, validTracker["svr"])


# unittest.main()

nodes = parse_input("input.txt")

start = nodes["svr"]
visited = []
paths = []
tracker = {}
start.paths_to(nodes["fft"], visited, paths, tracker)
print("Number of paths from 'srv' to 'fft':", tracker["svr"])
a = tracker["svr"]

start = nodes["fft"]
visited = []
paths = []
tracker = {}
start.paths_to(nodes["dac"], visited, paths, tracker)
print("Number of paths from 'fft' to 'dac':", tracker["fft"])
b = tracker["fft"]

start = nodes["dac"]
visited = []
paths = []
tracker = {}
start.paths_to(nodes["fft"], visited, paths, tracker)
print("Number of paths from 'fft' to 'dac':", tracker["dac"])

start = nodes["dac"]
visited = []
paths = []
tracker = {}
start.paths_to(nodes["out"], visited, paths, tracker)
print("Number of paths from 'dac' to 'out':", tracker["dac"])
c = tracker["dac"]

start = nodes["svr"]
visited = []
paths = []
tracker = {}
start.paths_to(nodes["out"], visited, paths, tracker)
print("Number of valid paths from 'svr' to 'out':", tracker["svr"])
total = tracker["svr"]

print("(ANSWER) Paths visiting 'dac' and 'fft':", a * b * c)

print("Percent:", ((a*b*c)/total)*100)


