import unittest
import re
import pdb
import resource

def limit_memory(maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))

def parse_input(filename):
    machines = []
    with open(filename, "r") as file:
        for line in file:
            target_state = get_lights(line)
            buttons = get_buttons(line)
            machines.append(Machine([0]*len(target_state), target_state, buttons))

    return machines

def get_lights(line):
    p = re.compile(r"[.#]")
    matches = p.findall(line)

    lights = []
    for match in matches:
        if match == "#":
            lights.append(1)
        elif match == ".":
            lights.append(0)

    return lights

def get_buttons(line):
    p = re.compile(r"\((?:[0-9],)*[0-9]\)")
    matches = p.findall(line)
    
    buttons = []
    for match in matches:
        subbed = match.replace("(", "").replace(")", "")
        buttons.append([int(n) for n in subbed.split(",")])

    return buttons

class Machine:
    def __init__(self, lights, target_state, buttons):
        self.lights = lights
        self.target_state = target_state
        self.buttons = buttons

    def get_light_str(self):
        return "".join([str(l) for l in self.lights])
    
    def press_button(self, button):
        lights_to_toggle = self.buttons[button]

        for light in lights_to_toggle:
            self.lights[light] = 1 if self.lights[light] == 0 else 0

    def score(self):
        correct = 0
        for i, light in enumerate(self.lights):
            if light == self.target_state[i]:
                correct += 1

        return correct / len(self.lights)

def find_shortest_sequence(machine):
    def aux(machines, current_step):
        # Base case - one of the machines has score of 1
        for machine in machines:
            if machine.score() == 1:
                return current_step

        # Recursive case - get machines for next step
        next_machines = []
        next_machines_dict = {}
        for machine in machines:
            for i, _ in enumerate(machine.buttons):
                new_machine = Machine(
                    machine.lights.copy(),
                    machine.target_state.copy(),
                    machine.buttons.copy(),
                )
                new_machine.press_button(i)

                # keep track of which machines we've added so we don't repeat outselves
                if new_machine.get_light_str() not in next_machines_dict:
                    next_machines.append(new_machine)
                    next_machines_dict[new_machine.get_light_str()] = 1

        return aux(next_machines, current_step + 1)

    return aux([machine], 0)

class MyTest(unittest.TestCase):
    float_error = 0.01

    def assertFloatWithinError(self, expected, answer):
        self.assertTrue(abs(expected - answer) <= self.float_error)

    def test_parse_input(self):
        machines = parse_input("test_input.txt")
        self.assertEqual(4, len(machines[0].lights))
        self.assertEqual(0, sum(machines[0].lights))
        self.assertEqual([0, 1, 1, 0], machines[0].target_state)
        self.assertEqual(6, len(machines[0].buttons))

        self.assertEqual(5, len(machines[1].lights))
        self.assertEqual(0, sum(machines[1].lights))
        self.assertEqual(5, len(machines[1].buttons))

        self.assertEqual(6, len(machines[2].lights))
        self.assertEqual(0, sum(machines[2].lights))
        self.assertEqual(4, len(machines[2].buttons))

    def test_get_lights(self):
        lines = []
        with open("test_input.txt", "r") as file:
            lines = [line for line in file]

        self.assertEqual([0, 1, 1, 0], get_lights(lines[0]))
        self.assertEqual([0, 0, 0, 1, 0], get_lights(lines[1]))
        self.assertEqual([0, 1, 1, 1, 0, 1], get_lights(lines[2]))
        
    def test_get_buttons(self):
        lines = []
        with open("test_input.txt", "r") as file:
            lines = [line for line in file]

        self.assertEqual([
            [3],
            [1, 3],
            [2],
            [2, 3],
            [0, 2],
            [0, 1]
        ], get_buttons(lines[0]))
        self.assertEqual([
            [0, 2, 3, 4],
            [2, 3],
            [0, 4],
            [0, 1, 2],
            [1, 2, 3, 4]
        ], get_buttons(lines[1]))
        self.assertEqual([
            [0, 1, 2, 3, 4],
            [0, 3, 4],
            [0, 1, 2, 4, 5],
            [1, 2]
        ], get_buttons(lines[2]))

    def test_press_button(self):
        machines = parse_input("test_input.txt")
        machines[0].press_button(0)
        self.assertEqual([0, 0, 0, 1], machines[0].lights)

        machines[0].press_button(1)
        self.assertEqual([0, 1, 0, 0], machines[0].lights)

    def test_score(self):
        machines = parse_input("test_input.txt")
        self.assertFloatWithinError(0.5, machines[0].score())

        machines[0].press_button(2)
        self.assertFloatWithinError(0.75, machines[0].score())

    def test_find_shortest_sequence(self):
        machines = parse_input("test_input.txt")
        self.assertEqual(2, find_shortest_sequence(machines[0]))
        self.assertEqual(3, find_shortest_sequence(machines[1]))
        self.assertEqual(2, find_shortest_sequence(machines[2]))

    def test_get_light_str(self):
        machines = parse_input("test_input.txt")
        self.assertEqual("0000", machines[0].get_light_str())
        

# unittest.main()

limit_memory(6000000000)
machines = parse_input("input.txt")

steps = []
for i, machine in enumerate(machines):
    steps.append(find_shortest_sequence(machine))

answer = sum(steps)

print("Answer:", answer)

