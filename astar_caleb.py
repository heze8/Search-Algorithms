import os
import sys
import heapq
import copy
import time

class Puzzle(object):

    @staticmethod
    def heuristic_function(state, goal_state): #estimated cost to get from the node to the goal
        hstate = copy.deepcopy(state)
        if hstate == goal_state:
          return 0
        h = 0
        length = len(hstate)

        #Do a swap
        def search(hstate, value):
            x = 0
            for i in range(0,len(hstate)):
                try:
                    x = hstate[i].index(value)
                    break;
                except:
                    error = "Not in row"
                
            return i,x
        
        for i in range(0, length):
            for j in range(0, length):
                #print(hstate[i][j], goal_state[i][j])
                if hstate[i][j] != goal_state[i][j]:
                    #find actual number that should be at the place
                    pos = search(hstate,goal_state[i][j])
                    row = pos[1]
                    col = pos[0]
                    #print("Position", pos)
                    #Swap (Append state number to goal number, vice versa)
                    hstate[col][row] = hstate[i][j] 
                    hstate[i][j] = goal_state[i][j]
                    #print("Heuristic State ", hstate)
                    #print("Goal State ",goal_state)
                    #print("Actual State ", state)
                break;

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
        
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = ["LEFT", "RIGHT", "UP", "DOWN"] # ’LEFT’, ’RIGHT’, ’UP’, ’DOWN’, and ’UNSOLVABLE’
        self.successors = []
        self.memory = set()
        
    class Node():
        def __init__(self, state, g):
            self.state = state
            self.g = g
            self.h = Puzzle.heuristic_function(state, goal_state)
            self.f = self.g + self.h
            self.parent = None
            self.prev_action = None

        def __lt__(self, node):
            return self.f < node.f
    
    def make_init_node(self, init_state):
        self.memory.add(str(init_state))
        init_node = self.Node(init_state, 0)
        heapq.heapify(self.successors)
        heapq.heappush(self.successors, init_node)
        return init_node
        
    def node_after_action(self, node, action):
        new_state = copy.deepcopy(node.state)
        
        def find_empty(matrix): # return a pair of i j values
            length = len(matrix)
            for i in range(0, length):
                for j in range(0, length):
                    if matrix[i][j] == 0:
                        return [i, j]
        
        def swap(matrix, i1, j1, i2, j2): # swaps two elements
            matrix[i1][j1], matrix[i2][j2] = matrix[i2][j2], matrix[i1][j1]
             

        max = len(new_state) - 1
        if action == "LEFT":
            index_empty = find_empty(new_state)
            i = index_empty[0]
            j = index_empty[1]
            if j == max:
                return
            swap(new_state, i, j, i, j + 1)
        
        if action == "RIGHT":
            index_empty = find_empty(new_state)
            i = index_empty[0]
            j = index_empty[1]
            if j == 0:
                return
            swap(new_state, i, j, i, j - 1)
        
        if action == "UP":
            index_empty = find_empty(new_state)
            i = index_empty[0]
            j = index_empty[1]
            if i == max:
                return
            swap(new_state, i, j, i + 1, j)
        
        if action == "DOWN":
            index_empty = find_empty(new_state)
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

        while current_node.parent != None:
          action_path.append(current_node.prev_action)
          current_node = current_node.parent
        
        if not action_path:
            return "Already Solved" 
        
        action_path.reverse()
        return action_path

    def best_first_search(self, node, f_limit):
        while self.successors:
            node = heapq.heappop(self.successors) 

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
        return self.best_first_search(self.make_init_node(self.init_state),99)
    
    # you may add more functions if you think is useful

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    sys.argv = []
    sys.argv.append("CS3243_p1_99_2.py")
    sys.argv.append("input_3.txt")
    sys.argv.append("output_1.txt")

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
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    start = time.time()
    ans = puzzle.solve()
    end = time.time()
    t = end - start
    print(t)
    
    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







