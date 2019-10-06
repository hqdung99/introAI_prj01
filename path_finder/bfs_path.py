from .BasePathFinder import BasePathFinder
import numpy as np
from collections import deque
# Note: deque is double linked list of Python


class BFS(BasePathFinder):
    def __init__(self, start, goal, 
                list_move=[(0, 1), (0, -1), (1, 0), (-1, 0)]):
        self.start = np.array(start)
        self.goal = np.array(goal)
        self.list_move = list_move
        self.queue = deque()
        self.closed = None

    def search(self, matrix_graph):
        # Init queue
        # Queue data struct: <coor, prev_pos> 
        self.push(self.start, -1)


        # Init closed set
        # Closed data struct: np array for backtrack    
        closed_shape = (*matrix_graph.shape, len(matrix_graph.shape))
        self.closed = np.zeros(closed_shape, dtype=int)
        self.closed.fill(-1)


        while len(self.queue) != 0:
            current_position, pre_pos = self.pop()
            self.close(current_position, pre_pos)

            for i, m in enumerate(self.list_move):
                next_pos = current_position + m

                # Check if next position is a valid position
                if self.check_position(next_pos, matrix_graph):
                    continue

                if (next_pos == self.goal).all():
                    self.close(next_pos, current_position)
                    # Backtrack the path from goal
                    return self.backtrack(self.goal)

                self.push(next_pos, current_position)

        return False



    def check_closed(self, position):
        '''Check if position is in closed set'''
        _temp = self.closed
        for index in position:
            _temp = _temp[index]
        return _temp[0] != -1


    def check_queue(self, position):
        '''Check if position is in open set'''
        for x in self.queue:
            if (x[0] == position).all():
                return True
                    




    def check_position(self, position, matrix_graph):
        ''' Check if player can move to position or not
        Input: 
            position: Position need to check
            matrix_graph: State of matrix
        
        Output:
            return True if cannot move to that position
        '''
        if (position < 0).any():
            return True

        if (position >= self.closed.shape[:-1]).any():
            return True 

        if matrix_graph[tuple(position)] > 0:
            return True

        # Check if next position is already exist in closed set
        if self.check_closed(position):
            return True

        # Check if next position is already exist in queue set
        if self.check_queue(position): 
            return True

    def close(self, position, prev_position):
        self.closed[tuple(position)] = prev_position


    def push(self, position, prev_pos):
        self.queue.append((position, prev_pos))


    def pop(self):
        return self.queue.popleft()

    def backtrack(self, goal):
        '''
        Return path from goal
        '''
        path = []
        current_position = tuple(goal)
        while (current_position != self.start).any():
            path.append(current_position)
            current_position = tuple(self.closed[current_position])

        path.append(tuple(self.start))
        path.reverse()
        return path



