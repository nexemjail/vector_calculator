from argparse import ArgumentParser
from itertools import combinations, permutations
from pprint import pprint
from copy import copy

from simp.tables import X, D, NOT_D, f1_table, f2_table,\
    f3_table, f4_table, f5_table, f6_table

EMPTY = 'O'


FUNCTION_INDICES_MAPPING = {
    0: [1, 2, 8],
    1: [3, 9],
    2: [5, 6, 10],
    3: [4, 7, 10, 11],
    4: [9, 11, 12],
    5: [8, 12, 13],
}


for k in FUNCTION_INDICES_MAPPING:
    FUNCTION_INDICES_MAPPING[k] = list(map(lambda x: x - 1,
                                           FUNCTION_INDICES_MAPPING[k]))


def get_next_element_index_in_cube(current_index):
    current_index_in_schema = current_index + 7
    path_blocks = dict(
        filter(lambda kv: current_index_in_schema in kv[1],
               FUNCTION_INDICES_MAPPING.items()))

    for block_index, in_out_indices in path_blocks.items():
        if current_index_in_schema in in_out_indices[:-1]:
            return in_out_indices[-1] - 7


def get_prev_element_index_in_cube(current_index):
        path_blocks = dict(
            filter(lambda kv: current_index in kv[1],
                   FUNCTION_INDICES_MAPPING.items()))

        for block_index, in_out_indices in path_blocks.items():
            if current_index == in_out_indices[-1]:
                return block_index


def f1(x1, x2):
    return not (x1 & x2)


def f2(x3):
    return not x3


def f3(x5, x6):
    return not (x5 | x6)


def f4(x4, out_f3, x7):
    return not (x4 & out_f3 & x7)


def f5(out_f2, out_f4):
    return out_f2 ^ out_f4


def f6(out_f1, out_f5):
    return out_f1 & out_f5


def intersect(x1, x2):
    if x1 == x2 == False:
        return False
    if x1 == False and x2 == X:
        return False
    if x1 == X and x2 == False:
        return False
    if x1 == x2 == X:
        return X

    if x1 == x2 == True:
        return True
    if x1 == True and x2 == X:
        return True
    if x1 == X and x2 == True:
        return True
    if x1 == True and x2 == False:
        return D
    if x1 == False and x2 == True:
        return NOT_D


def get_d_cube(table):
    d_cube = []
    for (line1, line2) in permutations(table, r=2):
        if line1[-1] == line2[-1]:
            continue
        d_cube.append([])
        for x1, x2 in zip(line1, line2):
            d_cube[-1].append(intersect(x1, x2))
        d_cube[-1] = tuple(d_cube[-1])
    return d_cube


CUBES = [get_d_cube(table)
         for table in
         [f1_table, f2_table, f3_table, f4_table, f5_table, f6_table]]


# pprint(CUBES)


def fill_value_or_calculate(index, outs, function_result):
    if outs[index] != -1:
        return outs[index]
    return function_result


def bin_to_array(value):
    return [b == '1' for b in value]


def int_to_bin(value, fill_length=7):
    return bin(value)[2:].zfill(fill_length)


def d_intersection(line1, line2):
    result = []
    for (a, b) in zip(line1, line2):
        if a == b or b == X:
            result.append(a)
        elif a == X or a == b:
            result.append(b)
        else:
            result.append(EMPTY)
    return result


def expand_line(line, indices):
    new_line = [X for _ in range(13)]
    for (i, value) in zip(indices, line):
        new_line[i] = value
    return tuple(new_line)


def get_expanded_lines_for_element(index):
    expanded_table = []
    for line in CUBES[index]:
        expanded_table.append(
            expand_line(line, FUNCTION_INDICES_MAPPING[index])
        )

    return set(expanded_table)


def get_expanded_lines_for_all_elements():
    return [get_expanded_lines_for_element(i) for i in range(len(CUBES))]


def forward_path(candidate_line, fault_index):
    fault_index_in_cube = fault_index - 1 - 7
    cube_element_index = fault_index - 1 - 7
    intersected_with = set([fault_index_in_cube])

    expanded_lines = get_expanded_lines_for_all_elements()

    current_line = copy(candidate_line)

    intersections_list = []

    while current_line[-1] == X:
        next_el_index = get_next_element_index_in_cube(cube_element_index)
        try:
            intersection = d_intersection(
                current_line,
                expanded_lines[next_el_index].pop())

            if EMPTY in intersection:
                continue
            else:
                intersected_with.add(next_el_index)
                intersections_list += [intersection]
                cube_element_index = next_el_index
                current_line = intersection
        except KeyError:
            cube_element_index = get_prev_element_index_in_cube(
                cube_element_index)
            current_line = intersections_list[-1]
            intersections_list = intersections_list[:-1]
            expanded_lines[cube_element_index + 1:] = [
                get_expanded_lines_for_element(i)
                for i in range(cube_element_index + 1, len(CUBES))]
            if cube_element_index == fault_index_in_cube:
                return None

    return current_line, intersected_with


def backward_path(forward_path_out, fault_index, intersected_with):
    element_indices = list(sorted(
        set(FUNCTION_INDICES_MAPPING.keys()) - intersected_with,
        reverse=True))
    intersection_counter = 0

    cube_element_index = element_indices[0]

    expanded_lines = get_expanded_lines_for_all_elements()
    current_line = forward_path_out

    intersections_list = []

    while cube_element_index != 0:
        prev_el_index = element_indices[intersection_counter]
        try:
            intersection = d_intersection(current_line,
                                          expanded_lines[prev_el_index].pop())

            if EMPTY in intersection:
                continue
            else:
                intersections_list += [intersection]
                cube_element_index = prev_el_index
                current_line = intersection
                intersection_counter += 1
        except KeyError:
            if len(intersections_list) < 1:
                return None
            intersection_counter -= 1
            current_line = intersections_list[-1]
            intersections_list = intersections_list[:-1]
            cube_element_index = element_indices[intersection_counter]
            expanded_lines[:element_indices[intersection_counter]] = [
                get_expanded_lines_for_element(i)
                for i in range(element_indices[intersection_counter])]

    return current_line


def get_candidate_lines(fault_index, fault_value):
    fault_alias = D if fault_value == 0 else NOT_D
    index = fault_index - 7 - 1

    table = CUBES[index]
    candidate_lines_no_index = filter(lambda x: x[-1] == fault_alias, table)
    candidate_lines = set(expand_line(line, FUNCTION_INDICES_MAPPING[index])
                          for line in candidate_lines_no_index)
    return candidate_lines


def main_algo():
    FAULT_INDEX = 11
    FAULT_VALUE = 0

    candidate_lines = \
        get_candidate_lines(fault_index=FAULT_INDEX, fault_value=FAULT_VALUE)

    for cl in candidate_lines:
        fp, intersected_with = forward_path(cl, FAULT_INDEX)
        result = backward_path(fp, FAULT_INDEX, intersected_with)
        if result is None:
            continue
        return result


print(main_algo())


def calculate_result(x_array, fault_location: str=None, fault_value=0):
    input_array = x_array.copy()
    outs = [-1 for _ in range(6)]

    if fault_location is not None:
        out_index = -1
        if 'x' in fault_location:
            input_array[int(fault_location[2]) - 1] = bool(fault_value)
        elif 'out_' in fault_location:
            out_index = int(fault_location[4])

        if out_index != -1:
            outs[out_index - 1] = bool(fault_value)

    outs[1 - 1] = fill_value_or_calculate(1 - 1, outs,
                                          f1(input_array[1 - 1],
                                             input_array[2 - 1])
                                          )
    outs[2 - 1] = fill_value_or_calculate(2 - 1,
                                          outs,
                                          f2(input_array[3 - 1]))
    outs[3 - 1] = fill_value_or_calculate(3 - 1,
                                          outs, f3(input_array[5 - 1],
                                                   input_array[6 - 1]))
    outs[4 - 1] = fill_value_or_calculate(4 - 1,
                                          outs, f4(input_array[4 - 1],
                                                   outs[3 - 1],
                                                   input_array[7 - 1]))
    outs[5 - 1] = fill_value_or_calculate(5 - 1,
                                          outs, f5(outs[2 - 1], outs[4 - 1]))
    outs[6 - 1] = fill_value_or_calculate(6 - 1,
                                          outs, f6(outs[1 - 1], outs[5 - 1]))

    return int(outs[-1])


def main(fault_location, fault_type):
    # print('Tests')
    for i in range(2**7):
        bin_value = int_to_bin(i)
        x_input = bin_to_array(bin_value)

        true_result = calculate_result(x_input)
        real_result = calculate_result(x_input, fault_location=fault_location,
                                       fault_value=fault_type)
        if true_result != real_result:
            print(bin_value)


if __name__ == '__main__':

    argparser = ArgumentParser()
    argparser.add_argument('--fault_location', '-fl',
                           type=str,
                           help='Enter fault location in format'
                                ' x_i i in [1, 7] or out_i  i in [1, 6]',
                           required=True)

    argparser.add_argument('--fault_value', '-fv',
                           choices=[0, 1],
                           type=int,
                           required=True,
                           help='Enter fault value 0 or 1')
    args = argparser.parse_args()

    main(args.fault_location, args.fault_value)
