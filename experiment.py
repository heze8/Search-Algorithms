import os
import sys
import heapq
import copy
import random


class Puzzle(object):
    @staticmethod
    def heuristic_function_misplaced(state, goal_state): #estimated cost to get from the node to the goal
        if state == goal_state:
          return 0
        h = 0
        length = len(state)
        for i in range(0, length):
            for j in range(0, length):
                if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                    h += 1

        return h

    @staticmethod
    def heuristic_function_manhatten(state, goal_state): #estimated cost to get from the node to the goal
        if state == goal_state:
          return 0
        h = 0
        length = len(state)
        for i in range(0, length):
            for j in range(0, length):
                if state[i][j] != 0: 
                    x = int((state[i][j] - 1) / length) #horizontal distance
                    y = int((state[i][j] - 1) % length) #vertical distance
                else:
                    x = length - 1 
                    y = length - 1
                h += (abs(i - x) + abs(j - y)) #sum of horizontal + vertical distance
        return h

    @staticmethod
    def heuristic_function_caleb(state, goal_state): #estimated cost to get from the node to the goal
        if state == goal_state:
          return 0
        h = 0
        length = len(state)

        #Do a swap
        def search(matrix, value): # return a pair of i j values
            length = len(matrix)
            for i in range(0, length):
                for j in range(0, length):
                    if matrix[i][j] == value:
                        return [i, j]
        
        for i in range(0, length):
            for j in range(0, length):
    
                if state[i][j] and state[i][j] != goal_state[i][j]:
                    #find actual number that should be at the place
                    pos = search(state, goal_state[i][j])
                    row = pos[0]
                    col = pos[1]
                    h += 1
                    state[row][col] = state[i][j] 
                    state[i][j] = goal_state[i][j]


        #Do a manhatten
        for i in range(0, length):
            for j in range(0, length):
                #obtain actual goal position
                if hstate[i][j] != 0: 
                    goal_row = int((hstate[i][j] - 1) / length) 
                    goal_col = (hstate[i][j] - 1) % length
                else: #0 is at the bottom right
                    goal_row = length - 1 
                    goal_col = length - 1
                h += (abs(i - goal_row) + abs(j - goal_col))
        return h

    class Experimental_evaluation():
        def __init__(self):
            self.average_f = 0
            self.number_of_nodes = 0
            self.sum_of_f = 0
            self.effective_branching_factor = 0
            self.solution_depth = 0

        def evaluate(self, node):
            self.number_of_nodes += 1
            self.sum_of_f += node.f

        def conclude(self):
            if self.number_of_nodes != 0 and self.solution_depth != 0:
                self.average_f = self.sum_of_f / self.number_of_nodes
                self.effective_branching_factor = self.number_of_nodes ** (1 / self.solution_depth)
                return [self.average_f, self.number_of_nodes, self.effective_branching_factor, self.solution_depth]
            else:
                return None
            
        
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = ["LEFT", "RIGHT", "UP", "DOWN"] # ’LEFT’, ’RIGHT’, ’UP’, ’DOWN’, and ’UNSOLVABLE’
        self.successors = []
        self.memory = set()
        self.experiment = self.Experimental_evaluation()
        
    class Node():
        def __init__(self, state, g):
            self.state = state
            self.g = g
            self.h = Puzzle.heuristic_function_misplaced(state, goal_state) #use of heuristic here
            self.f = self.g + self.h
            self.parent = None
            self.prev_action = None

        def __lt__(self, node):
            return self.f < node.f

    def find_empty(self, matrix): # return a pair of i j values
        length = len(matrix)
        for i in range(0, length):
            for j in range(0, length):
                if matrix[i][j] == 0:
                    return [i, j]

    def get_inv_count(self, matrix):
        inv_count = 0; 
        n = len(matrix)

        for i in range(0, n * n - 1):
            for j in range(i, n * n):
                r = (int) (i / n)
                c = i % n
                r2 = (int) (j / n)
                c2 = j % n
                # count pairs(i, j) such that i appears 
                # before j, but i > j. 
                if matrix[r][c] and matrix[r2][c2] and matrix[r][c] > matrix[r2][c2]: 
                    inv_count+=1 

        return inv_count

    def is_solvable(self, state):
        # Count inversions in given k puzzle 
        inv_count = self.get_inv_count(state) 
        length = len(state)
        if length % 2 != 0: #odd n
            # return true if inversion count is even. 
            return (inv_count % 2 == 0)

        else:
            index_empty = self.find_empty(state)
            if index_empty[0] % 2 == 0:
                return inv_count % 2 != 0
            else:
                return inv_count % 2 == 0


    def make_init_node(self, init_state):
        self.memory.add(str(init_state))
        init_node = self.Node(init_state, 0)
        heapq.heapify(self.successors)
        heapq.heappush(self.successors, init_node)
        return init_node
        
    def node_after_action(self, node, action):
        new_state = copy.deepcopy(node.state)
        
        def swap(matrix, i1, j1, i2, j2): # swaps two elements
            matrix[i1][j1], matrix[i2][j2] = matrix[i2][j2], matrix[i1][j1]
             

        max = len(new_state) - 1
        if action == "LEFT":
            index_empty = self.find_empty(new_state)
            i = index_empty[0]
            j = index_empty[1]
            if j == max:
                return
            swap(new_state, i, j, i, j + 1)
        
        if action == "RIGHT":
            index_empty = self.find_empty(new_state)
            i = index_empty[0]
            j = index_empty[1]
            if j == 0:
                return
            swap(new_state, i, j, i, j - 1)
        
        if action == "UP":
            index_empty = self.find_empty(new_state)
            i = index_empty[0]
            j = index_empty[1]
            if i == max:
                return
            swap(new_state, i, j, i + 1, j)
        
        if action == "DOWN":
            index_empty = self.find_empty(new_state)
            i = index_empty[0]
            j = index_empty[1]
            if i == 0:
                return
            swap(new_state, i, j, i - 1, j)
        
        if new_state == node.state:
          return

        new_node = self.Node(new_state, node.g + 1)
        new_node.parent = node
        new_node.prev_action = action
        return new_node

    def solution(self, node):
        current_node = node
        action_path = []
        d = 0

        while current_node.parent != None:
          action_path.append(current_node.prev_action)
          current_node = current_node.parent
          d+= 1
        
        if not action_path:
            return "Already Solved" 
        
        action_path.reverse()
        self.experiment.solution_depth = d
        return action_path

    def evaluate_heuristic(self):
        return self.experiment.conclude()


    def best_first_search(self, node, f_limit):
        while self.successors:
            node = heapq.heappop(self.successors)
            self.experiment.evaluate(node)
            if node.state == self.goal_state:
                return self.solution(node)

            if node.f > f_limit:
                return ['UNSOLVABLE']

            for action in self.actions:
                s = self.node_after_action(node, action)

                if s is None:
                    continue

                string_s = str(s.state)
                if string_s in self.memory:
                    continue
                self.memory.add(string_s)
                
                heapq.heappush(self.successors, s)
            
            #alternative = self.successors[1].f
            
        return ['UNSOLVABLE']
        
    def solve(self):
        if not self.is_solvable(self.init_state):
            return ['UNSOLVABLE_F']
        return self.best_first_search(self.make_init_node(self.init_state), 70)

    
    # you may add more functions if you think is useful

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    sys.argv = []
    sys.argv.append("CS3243_p1_99_2.py")
    input_file = "input_5"
    sys.argv.append(input_file + ".txt")
    sys.argv.append("experimental_output.txt")

    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    
    #Creates a random problem
    def generate_random_problem():
        def matrix_after_action(matrix, action):
            def swap(matrix, i1, j1, i2, j2): # swaps two elements
                matrix[i1][j1], matrix[i2][j2] = matrix[i2][j2], matrix[i1][j1]

            def find_empty(matrix): # return a pair of i j values
                length = len(matrix)
                for i in range(0, length):
                    for j in range(0, length):
                        if matrix[i][j] == 0:
                            return [i, j]

            max = len(matrix) - 1
            state = copy.deepcopy(matrix)

            if action == "LEFT":
                index_empty = find_empty(state)
                i = index_empty[0]
                j = index_empty[1]
                if j == max:
                    return
                swap(state, i, j, i, j + 1)
            
            if action == "RIGHT":
                index_empty = find_empty(state)
                i = index_empty[0]
                j = index_empty[1]
                if j == 0:
                    return
                swap(state, i, j, i, j - 1)
            
            if action == "UP":
                index_empty = find_empty(state)
                i = index_empty[0]
                j = index_empty[1]
                if i == max:
                    return
                swap(state, i, j, i + 1, j)
            
            if action == "DOWN":
                index_empty = find_empty(state)
                i = index_empty[0]
                j = index_empty[1]
                if i == 0:
                    return
                swap(state, i, j, i - 1, j)

            return state

        def complement(action):
            if action == "LEFT":
                return "RIGHT"
            
            if action == "RIGHT":
                return "LEFT"

            if action == "UP":
                return "DOWN"
            
            if action == "DOWN":
                return "UP"

        estimate_d = random.randrange(5, 25)
        
        state = copy.deepcopy(goal_state)

        i=0
        choice = ["LEFT", "RIGHT", "UP", "DOWN"]
        last_action = random.choice(choice)

        while i < estimate_d:
            actions = copy.copy(choice)
            actions.remove(complement(last_action))
            action = random.choice(actions)
            last_action = action
            
            new_state = matrix_after_action(state, action)
            if new_state is None:
                continue
            else:
                i += 1
                state = new_state

        return state
        
    class Table:
        def __init__(self):
            self.store = dict()

        class Data:
            def __init__(self, d):
                self.total_f = 0
                self.total_n = 0
                self.total_b = 0
                self.d = d
                self.num = 0

            def key(self, f, n, b):
                self.total_f += f
                self.total_n += n
                self.total_b += b
                self.num += 1
            
            def retrieve(self):
                num = self.num
                return "f : " + str(self.total_f/num), "n : " + str( (int) (self.total_n/num)), "b : " + str(self.total_b/num)

        def enter(self, d, f, n, b):
            if d in self.store:
                self.store.get(d).key(f, n, b)
            else:
                data = self.Data(d)
                data.key(f,n,b)
                self.store[d] = data
        
        def retrieve(self):
            for d,data in self.store.items():
                print (d, "=>", data.retrieve())

    table = Table()
    for i in range(1000):
        random_puzzle = generate_random_problem()
        
        puzzle = Puzzle(random_puzzle, goal_state)
        puzzle.solve()
        ans = puzzle.evaluate_heuristic()
        
        if ans is None:
            continue
        # returns [self.average_f, self.number_of_nodes, self.effective_branching_factor, self.solution_depth]
        d = ans[3]
        table.enter(d, ans[0], ans[1], ans[2])
        
    table.retrieve()

    #with open(sys.argv[2], 'a') as f:
        #for answer in ans:
           # f.write(str(answer)+'\n')







