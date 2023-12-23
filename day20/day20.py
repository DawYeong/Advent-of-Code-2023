from operator import add
import copy
import math


def day20(filename, part2):
    with open(filename, "r") as file:
        data = file.read()

    modules_map = {}
    broadcast = []
    lines = data.split("\n")
    switches = {}
    conjunctions = set()
    conjunctions_map = {}

    for line in lines:
        line = line.replace(" ", "").replace("->", ",").split(",")
        if line[0][0] == "%":
            modules_map[line[0][1:]] = (line[0][0], line[1:])
            switches[line[0][1:]] = 0
        elif line[0][0] == "&":
            modules_map[line[0][1:]] = (line[0][0], line[1:])
            conjunctions.add(line[0][1:])
        else:
            broadcast = line[1:]

    for conjunction in conjunctions:
        conjunctions_map[conjunction] = {}
        for key, value in modules_map.items():
            find = len([v for v in value[1] if v == conjunction])
            if find != 0:
                conjunctions_map[conjunction][key] = 0

    # button sends low pulse signal to broadcast
    # 0 for low/OFF, 1 for high/ON
    def push_button(check=None):
        pulse_counts = [1, 0]
        work_list = [(0, "broadcast", module_id) for module_id in broadcast]
        sent = copy.deepcopy(work_list)
        test = None
        while work_list:
            pulse = work_list.pop(0)
            pulse_counts[pulse[0]] += 1

            if check and check == pulse[2] and pulse[0] == 1:
                test = pulse[1]

            module = modules_map.get(pulse[2], None)
            if not module:
                continue

            # flip flop => ignore if high signal was sent
            # else => flips switch and sends HIGH if was OFF, LOW if was ON
            if module[0] == "%":
                if pulse[0] == 1:
                    continue
                for connection in module[1]:
                    next_pulse = int(not switches[pulse[2]])
                    work_list.append((next_pulse, pulse[2], connection))
                    # check if sending pulse to conjunction
                    conjunction = conjunctions_map.get(connection, None)
                    if conjunction:
                        conjunction[pulse[2]] = next_pulse

                    sent.append((int(not switches[pulse[2]]), pulse[2], connection))
                switches[pulse[2]] = (switches[pulse[2]] + 1) % 2

            elif module[0] == "&":
                check_all_high = all(list(conjunctions_map[pulse[2]].values()))

                for connection in module[1]:
                    next_pulse = int(not check_all_high)
                    conjunction = conjunctions_map.get(connection, None)
                    if conjunction:
                        conjunction[pulse[2]] = next_pulse
                    work_list.append((next_pulse, pulse[2], connection))
                    sent.append((next_pulse, pulse[2], connection))

        return pulse_counts, sent, test

    if not part2:
        pulses = []
        seen = []
        cycle_start = 0
        while True and len(pulses) < 1000:
            pulse_state, sent, _ = push_button()
            state = str(sent) + str(switches)
            if state in seen:
                cycle_start = seen.index(state)
                break

            pulses.append(pulse_state)
            seen.append(state)

        partial_sum = [0, 0]
        cycle_sum = [0, 0]

        cycles = (1000 - cycle_start) // (len(pulses) - cycle_start)
        rem = (1000 - cycle_start) % (len(pulses) - cycle_start)

        for i in range(cycle_start):
            partial_sum = list(map(add, partial_sum, pulses[i]))

        for i in range(cycle_start, len(pulses)):
            if i < rem:
                partial_sum = list(map(add, partial_sum, pulses[i]))
            cycle_sum = list(map(add, cycle_sum, pulses[i]))

        total_pulses = list(map(add, partial_sum, map(lambda x: x * cycles, cycle_sum)))

        print(f"result1: {total_pulses[0] * total_pulses[1]}")
    else:
        # PART 2

        # find out which module sends to rx
        # currently assuming all inputs are going to be conjunctions
        # this part will only work with input.txt => samples do not have rx

        # test = conjunctions_map["rx"]
        rx_input = ""
        for key, value in modules_map.items():
            if "rx" in value[1]:
                # there is a single input to rx
                rx_input = key
                break

        # print(conjunctions_map[rx_input])
        input_list = list(conjunctions_map[rx_input].keys())
        high_values = {}

        for t in input_list:
            high_values[t] = 0

        button_presses = 0
        while not all(list(high_values.values())):
            _, _, high_key = push_button(rx_input)
            button_presses += 1

            if high_key and high_values[high_key] == 0:
                high_values[high_key] = button_presses

        result2 = 1
        for val in high_values.values():
            result2 = result2 * val // math.gcd(result2, val)

        print(f"result2: {result2}")


# day20("sample1.txt")
# day20("sample2.txt")
day20("input.txt", False)
day20("input.txt", True)
