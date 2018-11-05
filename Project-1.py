import copy as cp
import queue
import time
import sys

def startProject(puzzle):
    default_puzzle = puzzle
    description1  = "Welcome to Carlos Gomez's 8-puzzle solver.\n"
    description1 += 'Type "1" to use a default puzzle, or "2" to enter your own puzzle.'
    print(description1)
    option_puzzle = int(input())

    puzzle = []

    if option_puzzle == 1:
        puzzle = default_puzzle
        

    elif option_puzzle == 2:
        description_init = '\tEnter your puzzle, use a zero to represent the blank'
        print(description_init)

        description_1stR = '\tEnter the first row, use space or tabs between numbers\t\t'
        description_2ndR = '\tEnter the second row, use space or tabs between numbers\t\t'
        description_3rdR = '\tEnter the third row, use space or tabs between numbers\t\t'
        entry_puzzle  = [int(x) for x in input(description_1stR).split()]
        entry_puzzle += [int(x) for x in input(description_2ndR).split()]
        entry_puzzle += [int(x) for x in input(description_3rdR).split()]
        
        puzzle = entry_puzzle

    else:
        print("Please select an option")
        sys.exit(0)

    problem = Problem(puzzle)
        
    alg_description  = "\tEnter your choice of algorithm\n"
    alg_description += "\t\t1. Uniform Cost Search\n"
    alg_description += "\t\t2. A* with the Misplaced Tile heuristic\n"
    alg_description += "\t\t3. A* with the Manhattan distance heuristic\n"

    print(alg_description)
    
    alg_input = str(input("\t\t"))

    input_dict = {'1':uniform, '2':a_star_search_misplaced, '3':a_star_search_manhattan}
    start = time.time()
    node = general_search(problem, input_dict[alg_input])
    end = time.time()
    print("Time to finish: {}".format(end-start))
    return node


class Node:
    
    def __init__(self, state):
        self.state = state

    def __repr__(self):
        return str(self.state)

    def get_state(self):
        return self.state

    def set_gn(self, gn):
        self.gn = gn
    
    def get_gn(self):
        return self.gn

    def set_hn(self, hn):
        self.hn = hn

    def get_hn(self):
        return self.hn
    
    def set_fn(self, fn):
        self.fn = fn

    def get_fn(self):
        return self.fn
    
    def __lt__(self, otherNode):
        return self.fn < otherNode.fn

class Problem:

    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.map_attempts = set()
        self.goal_state = [1,2,3,4,5,6,7,8,0]
        self.test_attempt(self.initial_state)
        self.node_count = 0

    def goal_test(self, node_state):
        return self.goal_state == node_state

    def diff_test(self, curr_state):
        total_diff = 0
        for goal_val, input_val in zip(self.goal_state, curr_state):
            if goal_val != input_val:
                total_diff += 1
        return total_diff

    def get_node_count(self):
        return self.node_count

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

    def operators(self, input_node):
        self.node_count += 1
        curr_state = input_node.get_state()
        operator_list = list()
        zero_index = self.find_blank(curr_state)
        
        # Move up allowed
        if zero_index > 2:
            up_node = Node(self.move_up(zero_index, curr_state))
            up_node.set_gn(input_node.get_gn()+1)
            if self.test_attempt(up_node.get_state()):
                operator_list.append(up_node)

        # Move down allowed
        if zero_index < 6:
            down_node = Node(self.move_down(zero_index, curr_state))
            down_node.set_gn(input_node.get_gn()+1)
            if self.test_attempt(down_node.get_state()):
                operator_list.append(down_node)

        # Move left allowed
        if zero_index % 3 > 0:
            left_node = Node(self.move_left(zero_index, curr_state))
            left_node.set_gn(input_node.get_gn()+1)
            if self.test_attempt(left_node.get_state()):
                operator_list.append(left_node)

        # Move right allowed
        if zero_index % 3 < 2:
            right_node = Node(self.move_right(zero_index, curr_state))
            right_node.set_gn(input_node.get_gn()+1)
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
    prioQueue = nodes
    for node in new_nodes:
        node.set_hn(0)
        curr_gn = node.get_gn()
        node.set_fn(curr_gn + 0)
        prioQueue.put(node)
    return prioQueue

def manhattan_distance(test_state):
    goal_state = [1,2,3,4,5,6,7,8,0]
    total_distance = 0
    for index, (test,goal) in enumerate(zip(test_state,goal_state)):
        if test == goal or test == 0:
            continue
        else:
            test_row = (test-1) // 3
            test_col = (test-1) % 3

            index_row = index // 3
            index_col = index % 3

            abs_diff = abs(test_row - index_row) + abs(test_col - index_col)
            total_distance += abs_diff

    return total_distance

def a_star_search_manhattan(nodes, new_nodes):
    prioQueue = nodes
    for node in new_nodes:
        man_distance = manhattan_distance(node.get_state())
        node.set_hn(man_distance)
        curr_gn = node.get_gn()
        node.set_fn(curr_gn + man_distance)
        prioQueue.put(node)
    return prioQueue

def misplaced_distance(test_state):
    goal_state = [1,2,3,4,5,6,7,8,0]
    mis_distance = 0
    for test,goal in zip(test_state, goal_state):
        if test == 0:
            continue
        if test != goal:
            mis_distance += 1
    return mis_distance

def a_star_search_misplaced(nodes, new_nodes):
    prioQueue = nodes
    for node in new_nodes:
        mis_distance = misplaced_distance(node.get_state())
        node.set_hn(mis_distance)
        curr_gn = node.get_gn()
        node.set_fn(curr_gn + mis_distance)
        prioQueue.put(node)
    return prioQueue

def general_search(problem, q_function):
    nodes = queue.PriorityQueue()
    first_node = Node(problem.state())
    first_node.set_gn(0)
    first_node.set_hn(0)
    first_node.set_fn(0)
    nodes.put(first_node)
    print("Expanding state")
    tile_print(first_node)

    maxQueueSize = nodes.qsize()
    while(1):
        if nodes.empty():
            return "failure"
        node = nodes.get()
        if problem.goal_test(node.get_state()):
            print("Goal!!")
            print("To solve this problem the search algorithm expanded a total of {node_total} nodes".format(node_total = problem.get_node_count()))
            print("The maximum number of nodes in the queue at any one time was {max_queue_nodes}.".format(max_queue_nodes=maxQueueSize))
            print("The depth of the goal node was {depth}".format(depth=node.get_gn()))
            return node
        print("The best state to expand with a g(n) = {gn} and h(n) = {hn} is ...".format(gn=node.get_gn(), hn=node.get_hn()))
        tile_print(node)
        nodes = q_function(nodes, problem.operators(node))
        # Check for max queue size
        trySize = nodes.qsize()
        if trySize > maxQueueSize:
            maxQueueSize = trySize

def tile_print(input_node):
    for index, tile in enumerate(input_node.get_state()):
        if tile == 0:
            print("b", end=' ')
        else:
            print(tile, end=' ')
        if index % 3 == 2:
            print()
    print()

if __name__ == '__main__':
    puzzles = [[1,2,3,4,5,6,7,8,0],[1,2,3,4,5,6,7,0,8],[1,2,0,4,5,3,7,8,6],[0,1,2,4,5,3,7,8,6],[8,7,1,6,0,2,5,4,3],[1,2,3,4,5,6,8,7,0]]
    for puzzle in puzzles:
        startProject(puzzle)
