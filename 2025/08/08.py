import unittest
import math
import itertools
from uuid import uuid4
import pdb

def parse_boxes(filename):
    boxes = []

    with open(filename, "r") as file:
        for line in file:
            id = uuid4()
            dims = [int(dim) for dim in line.split(",")]
            box = JunctionBox(id, dims[0], dims[1], dims[2])
            boxes.append(box)

    return boxes

def distance_3d(a, b):
    return math.sqrt(
        math.pow((a.x - b.x), 2) +  
        math.pow((a.y - b.y), 2) +  
        math.pow((a.z - b.z), 2)
    )

def get_pairwise_distances(boxes):
    pairwise_distances = [
        (pair[0], pair[1], distance_3d(pair[0], pair[1])) 
        for pair
        in itertools.combinations(boxes, 2)
    ]

    return sorted(pairwise_distances, key=lambda x: x[2])

def make_shortest_connections(boxes, n):
    pairs = get_pairwise_distances(boxes)
    shortest = pairs[0:n]

    for pair in shortest:
        pair[0].connect(pair[1])

class CircuitRegistry:


    def __init__(self, boxes):
        self.boxes = boxes
        self.registry = {}

        for box in boxes:
            self.registry[box.id] = box


    def get_circuits(self):
        circuits = []

        registry_copy = self.registry.copy()

        while (len(registry_copy) > 0):
            worklist = list(registry_copy.keys())
            box_id = worklist[0]
            box = self.registry[box_id]

            size, box_ids, _  = box.traverse_circuit(0, [], {})

            circuits.append((size, box_ids))

            for id in box_ids:
                del(registry_copy[id])

        return sorted(circuits, key=lambda x: x[0], reverse=True)

class JunctionBox:
    
    def __init__(self, id, x, y, z):
        self.neighbors = []
        self.neighbors_index = {}
        self.id = id
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.id}: ({self.x}, {self.y}, {self.z})"

    def connect(self, box):
        # breakpoint()

        if box == self:
            return None

        if box.id not in self.neighbors_index:
            self.neighbors.append(box)
            self.neighbors_index[box.id] = 1
            box.connect(self)

    def traverse_circuit(self, size, rsf, rsf_index):
        # Base case
        if self.id in rsf_index:
            return size, rsf, rsf_index

        # Recursive case

        size += 1
        rsf.append(self.id)
        rsf_index[self.id] = 1

        for neighbor in self.neighbors:
            if neighbor.id in rsf_index:
                continue

            size, rsf, rsf_index = neighbor.traverse_circuit(size, rsf, rsf_index)

        return size, rsf, rsf_index


class MyTest(unittest.TestCase):
    float_error = 0.01

    def assertFloatWithinError(self, expected, answer):
        self.assertTrue(abs(expected - answer) <= self.float_error)

    def test_parse_boxes(self):
        boxes = parse_boxes("test_input.txt")
        self.assertEqual((162, 817, 812), (boxes[0].x, boxes[0].y, boxes[0].z))
        self.assertEqual((425, 690, 689), (boxes[-1].x, boxes[-1].y, boxes[-1].z))

    def test_distance_3d(self):
        boxes = parse_boxes("test_input.txt")
        distance = distance_3d(boxes[0], boxes[-1])
        self.assertFloatWithinError(316.90, distance)

    def test_get_pairwise_distances(self):
        boxes = parse_boxes("test_input.txt")
        pairwise_distances = get_pairwise_distances(boxes)
        self.assertFloatWithinError(316.90, pairwise_distances[0][2])

    def test_connect(self):
        boxes = parse_boxes("test_input.txt")
        boxes[0].connect(boxes[-1])
        self.assertEqual([boxes[-1]], boxes[0].neighbors)
        self.assertEqual([boxes[0]], boxes[-1].neighbors)

    def test_circuit_registry(self):
        boxes = parse_boxes("test_input.txt")
        reg = CircuitRegistry(boxes)
        self.assertEqual(20, len(reg.registry))

    def test_traverse_circuit(self):
        boxes = parse_boxes("test_input.txt")

        a = boxes[0]
        b = boxes[1]
        c = boxes[2]
        d = boxes[3]
        e = boxes[4]

        a.connect(b)
        a.connect(c)
        a.connect(d)
        a.connect(e)

        b.connect(c)
        c.connect(d)


        size, box_ids, _ = a.traverse_circuit(0, [], {})

        self.assertEqual(5, size)

    def test_get_circuits(self):
        boxes = parse_boxes("test_input.txt")

        reg = CircuitRegistry(boxes)

        a = boxes[0]
        b = boxes[1]
        c = boxes[2]
        d = boxes[3]
        e = boxes[4]

        circuits = reg.get_circuits()
        self.assertEqual(20, len(circuits))
        self.assertEqual(1, circuits[0][0])

        a.connect(b)
        a.connect(c)
        a.connect(d)
        a.connect(e)

        circuits = reg.get_circuits()
        self.assertEqual(16, len(circuits))
        self.assertEqual(5, circuits[0][0])

        f = boxes[5]
        g = boxes[6]

        f.connect(g)

        circuits = reg.get_circuits()
        self.assertEqual(15, len(circuits))
        self.assertEqual(5, circuits[0][0])
        self.assertEqual(2, circuits[1][0])

    def test_make_shortest_connections(self):
        boxes = parse_boxes("test_input.txt")
        reg = CircuitRegistry(boxes)

        make_shortest_connections(boxes, 10)

        circuits = reg.get_circuits()
        self.assertEqual(11, len(circuits))
        self.assertEqual(40, circuits[0][0] * circuits[1][0] * circuits[2][0])


# unittest.main()

boxes = parse_boxes("input.txt")
reg = CircuitRegistry(boxes)
make_shortest_connections(boxes, 1000)
circuits = reg.get_circuits()
answer = circuits[0][0] * circuits[1][0] * circuits[2][0]

print("Answer:", answer)
