import unittest
import re
import pdb
import json
import pprint

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

    def __str__(self):
        return self.name

    def set_next(self, nexts):
        self.next = nexts

    def paths_to(self, dest, visited = [], paths = []):
        visited.append(self)

        if self == dest:
            paths.append(visited.copy())
        else:
            for next in self.next:
                next.paths_to(dest, visited, paths)

        visited.pop()


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
        start.paths_to(nodes["out"], visited, paths)

        self.assertEqual(["you", "bbb", "ddd", "ggg", "out"], [n.name for n in paths[0]])
        self.assertEqual(["you", "bbb", "eee", "out"], [n.name for n in paths[1]])
        self.assertEqual(["you", "ccc", "ddd", "ggg", "out"], [n.name for n in paths[2]])
        self.assertEqual(["you", "ccc", "eee", "out"], [n.name for n in paths[3]])
        self.assertEqual(["you", "ccc", "fff", "out"], [n.name for n in paths[4]])
        self.assertEqual(5, len(paths))


# unittest.main()

nodes = parse_input("input.txt")
start = nodes["you"]

visited = []
paths = []
start.paths_to(nodes["out"], visited, paths)

print("Number of paths to 'out':", len(paths))
