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
            target_state = get_joltage_counters(line)
            buttons = get_buttons(line)
            machines.append(Machine([0]*len(target_state), target_state, buttons))

    return machines

def get_buttons(line):
    p = re.compile(r"\((?:[0-9],)*[0-9]\)")
    matches = p.findall(line)
    
    buttons = []
    for match in matches:
        subbed = match.replace("(", "").replace(")", "")
        buttons.append([int(n) for n in subbed.split(",")])

    return buttons

def get_joltage_counters(line):
    pattern = re.compile(r"\{(?:[0-9]+,)*[0-9]+\}")
    match = pattern.search(line)

    # if match == None:
    #     breakpoint()

    string = match.group(0)

    subbed = string.replace("{", "").replace("}", "")

    counters = [int(n) for n in subbed.split(",")]

    return counters

    
class Machine:
    def __init__(self, start_state, target_state, buttons):
        self.state = start_state
        self.target_state = target_state
        self.buttons = buttons

    def in_target_state(self):
        return self.get_state_str() == self.get_target_state_str()

    def past_point_of_no_return(self):
        for i, counter in enumerate(self.state):
            if counter > self.target_state[i]:
                breakpoint()
                return True
        
        return False

    def get_state_str(self):
        return ",".join([str(l) for l in self.state])

    def get_target_state_str(self):
        return ",".join([str(l) for l in self.target_state])
    
    def press_button(self, button):
        counters_to_increment = self.buttons[button]

        for counter in counters_to_increment:
            self.state[counter] += 1

# Implementation of breadth-first search
def find_shortest_sequence(machine):
    def aux(machines, current_step):
        # Base case - one of the machines is in the target state
        for machine in machines:
            if machine.in_target_state():
                return current_step

        # Recursive case - get machines for next step
        next_machines = []
        next_machines_dict = {}
        for machine in machines:
            for i, _ in enumerate(machine.buttons):
                new_machine = Machine(
                    machine.state.copy(),
                    machine.target_state.copy(),
                    machine.buttons.copy(),
                )
                new_machine.press_button(i)

                if new_machine.past_point_of_no_return():
                    continue

                # keep track of which machines we've added so we don't repeat outselves
                if new_machine.get_state_str() not in next_machines_dict:
                    next_machines.append(new_machine)
                    next_machines_dict[new_machine.get_state_str()] = 1

        return aux(next_machines, current_step + 1)

    return aux([machine], 0)

class MyTest(unittest.TestCase):
    def test_parse_input(self):
        machines = parse_input("test_input.txt")
        self.assertEqual([3, 5, 4, 7], machines[0].target_state)
        self.assertEqual([7, 5, 12, 7, 2], machines[1].target_state)
        self.assertEqual([10, 11, 11, 5, 10, 5], machines[2].target_state)


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

    def test_get_joltage_counters(self):
        lines = []
        with open("test_input.txt", "r") as file:
            lines = [line for line in file]
        self.assertEqual([3, 5, 4, 7], get_joltage_counters(lines[0]))

    def test_press_button(self):
        machines = parse_input("test_input.txt")
        self.assertEqual([0, 0, 0, 0], machines[0].state)

        machines[0].press_button(0)
        self.assertEqual([0, 0, 0, 1], machines[0].state)

        machines[0].press_button(1)
        self.assertEqual([0, 1, 0, 2], machines[0].state)

    def test_in_target_state(self):
        machines = parse_input("test_input.txt")
        self.assertFalse(machines[0].in_target_state())

        machines[0].press_button(0)

        machines[0].press_button(1)
        machines[0].press_button(1)
        machines[0].press_button(1)

        machines[0].press_button(3)
        machines[0].press_button(3)
        machines[0].press_button(3)

        machines[0].press_button(4)
        
        machines[0].press_button(5)
        machines[0].press_button(5)

        self.assertTrue(machines[0].in_target_state())

    def test_find_shortest_sequence(self):
        machines = parse_input("test_input.txt")
        self.assertEqual(10, find_shortest_sequence(machines[0]))
        self.assertEqual(12, find_shortest_sequence(machines[1]))
        self.assertEqual(11, find_shortest_sequence(machines[2]))

    def test_get_state_str(self):
        machines = parse_input("test_input.txt")
        self.assertEqual("0,0,0,0", machines[0].get_state_str())

    def test_get_target_state_str(self):
        machines = parse_input("test_input.txt")
        self.assertEqual("3,5,4,7", machines[0].get_target_state_str())
        

# unittest.main()

limit_memory(6000000000)
machines = parse_input("input.txt")

steps = []
skip = [3]
for i, machine in enumerate(machines):
    if i in skip:
        continue
    print(i)
    s = find_shortest_sequence(machine)
    print("Steps:", s)
    steps.append(s)

answer = sum(steps)

print("Answer:", answer)

