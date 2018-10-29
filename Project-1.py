import copy as cp

description  = "Welcome to Carlos Gomez's 8-puzzle solver.\n"
description += 'Type "1" to use a default puzzle, or "2" to enter your own puzzle.\n'
description += '\tEnter your puzzle, use a zero to represent the blank'
description += '\tEnter the first row, use space or tabs between numbers'

"""
function general-search(problem, QUEUEING-FUNCTION)
    nodes = MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
    loop do
        if EMPTY(nodes) then return "failure"
        node = REMOVE-FRONT(nodes)
        if problem.GOAL-TEST(node.STATE) succeeds then return node
        nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
    end
"""
class Node:
    
    def __init__(self, state):
        self.state = state

    def get_state(self):
        return self.state

class Problem:

    def __init__(self, input_array):
        self.input_array = input_array
        self.map_attempts = set()
        self.goal_state = [1,2,3,4,5,6,7,8,0]

    def goal_test(self):
        return self.goal_state == self.input_array

    def diff_test(self):
        total_diff = 0
        for goal_val, input_val in zip(self.goal_state, self.input_array):
            if goal_val != input_val:
                total_diff += 1
        return total_diff

    def test_attempt(self, node_state):
        if node_state in self.map_attempts:
            return False
        else:
            self.map_attempts.add(node_state)
            return True
    def find_blank(self):
        for index, value in enumerate(self.input_array):
            if value == 0:
                return index

    def operators(self):
        operator_list = list()
        zero_index = self.find_blank()
        
        # Move up allowed
        if zero_index > 2:
            operator_list.append(self.move_up(zero_index))

        # Move down allowed
        if zero_index < 6:
            operator_list.append(self.move_down(zero_index))

        # Move left allowed
        if zero_index % 3 > 0:
            operator_list.append(self.move_left(zero_index))

        # Move right allowed
        if zero_index % 3 < 2:
            operator_list.append(self.move_right(zero_index))
        
        return operator_list

    def move_up(self, index):
        up_list = cp.deepcopy(self.input_array)
        up_list[index], up_list[index-3] = up_list[index-3], up_list[index]
        return up_list

    def move_down(self, index):
        down_list = cp.deepcopy(self.input_array)
        down_list[index], down_list[index+3] = down_list[index+3], down_list[index]
        return down_list

    def move_left(self, index):
        left_list = cp.deepcopy(self.input_array)
        left_list[index], left_list[index-1] = left_list[index-1], left_list[index]
        return left_list

    def move_right(self, index):
        right_list = cp.deepcopy(self.input_array)
        right_list[index], right_list[index+1] = right_list[index+1], right_list[index]
        return right_list

    def state(self):
        return self.input_array

def uniform(nodes, new_nodes):
    pass

def expand(node, problem_operators):
    new_nodes = list()


def general_search(problem, q_function):
    print('1')

if __name__ == '__main__':
    test_val = [1,2,3,4,5,6,7,8,0]
    test = Problem(test_val)
    test.find_blank()
    test_list = test.operators()
    for single_list in test_list:
        for index, value in enumerate(single_list):
            print(value, end=' ')
            if index % 3 == 2:
                print()
        print()