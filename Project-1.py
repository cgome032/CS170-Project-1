import copy as cp
import queue

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

    def __repr__(self):
        return str(self.state)

    def get_state(self):
        return self.state
    

class Problem:

    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.map_attempts = set()
        self.goal_state = [1,2,3,4,5,6,7,8,0]
        self.test_attempt(self.initial_state)

    def goal_test(self, node_state):
        return self.goal_state == node_state

    def diff_test(self, curr_state):
        total_diff = 0
        for goal_val, input_val in zip(self.goal_state, curr_state):
            if goal_val != input_val:
                total_diff += 1
        return total_diff

    def test_attempt(self, node_state):
        if tuple(node_state) in self.map_attempts:
            return False
        else:
            self.map_attempts.add(tuple(node_state))
            return True

    def find_blank(self, curr_state):
        for index, value in enumerate(curr_state):
            if value == 0:
                return index

    def operators(self, curr_state):
        operator_list = list()
        zero_index = self.find_blank(curr_state)
        
        # Move up allowed
        if zero_index > 2:
            up_node = Node(self.move_up(zero_index, curr_state))
            if self.test_attempt(up_node.get_state()):
                operator_list.append(up_node)

        # Move down allowed
        if zero_index < 6:
            down_node = Node(self.move_down(zero_index, curr_state))
            if self.test_attempt(down_node.get_state()):
                operator_list.append(down_node)

        # Move left allowed
        if zero_index % 3 > 0:
            left_node = Node(self.move_left(zero_index, curr_state))
            if self.test_attempt(left_node.get_state()):
                operator_list.append(left_node)

        # Move right allowed
        if zero_index % 3 < 2:
            right_node = Node(self.move_right(zero_index, curr_state))
            if self.test_attempt(right_node.get_state()):
                operator_list.append(right_node)
        
        return operator_list

    def move_up(self, index, curr_state):
        up_list = cp.deepcopy(curr_state)
        up_list[index], up_list[index-3] = up_list[index-3], up_list[index]
        return up_list

    def move_down(self, index, curr_state):
        down_list = cp.deepcopy(curr_state)
        down_list[index], down_list[index+3] = down_list[index+3], down_list[index]
        return down_list

    def move_left(self, index, curr_state):
        left_list = cp.deepcopy(curr_state)
        left_list[index], left_list[index-1] = left_list[index-1], left_list[index]
        return left_list

    def move_right(self, index, curr_state):
        right_list = cp.deepcopy(curr_state)
        right_list[index], right_list[index+1] = right_list[index+1], right_list[index]
        return right_list

    def state(self):
        return self.initial_state

def uniform(nodes, new_nodes):
    newQueue = nodes
    for node in new_nodes:
        newQueue.put(node)
    return newQueue


def general_search(problem, q_function):
    nodes = queue.Queue()
    first_node = Node(problem.state())
    nodes.put(first_node)

    while(1):
        if nodes.empty():
            return "failure"
        node = nodes.get()
        tile_print(node.get_state())
        if problem.goal_test(node.get_state()):
            return node
        nodes = q_function(nodes, problem.operators(node.get_state()))

def tile_print(input_list):
    for index, tile in enumerate(input_list):
        print(tile, end=' ')
        if index % 3 == 2:
            print()
    print()

if __name__ == '__main__':
    test_val = [1, 2, 3, 4, 0, 6, 7, 5, 8]
    test = Problem(test_val)
    node = general_search(test, uniform)
    print(node)