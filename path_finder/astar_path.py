from .greedy_search import GreedySearch
import numpy as np
import heapq
import random

from itertools import count as count_obj
tiebreaker = count_obj(step=-1)

class AStarSearch(GreedySearch):
    def __init__(self, start, goal, 
                list_move=[(0, 1), (0, -1), (1, 0), (-1, 0)],
                ):
        super().__init__(start, goal, list_move)
        self.distance_matrix = None


    def search(self, matrix_graph):
        # Init queue
        # Queue data struct: <coor, prev_pos> 
        self.push(self.start, -1, 0)


        # Init closed set
        # Closed data struct: np array for backtrack    
        closed_shape = (*matrix_graph.shape, len(matrix_graph.shape))
        self.closed = np.zeros(closed_shape, dtype=int)
        self.closed.fill(-1)
        self.distance_matrix = np.zeros(matrix_graph.shape, dtype=int)
        self.distance_matrix.fill(1e5)

        while len(self.queue) != 0:
            current_position, pre_pos, distance_to_start = self.pop()
            
            if not isinstance(pre_pos, int) and distance_to_start < self.distance_matrix[current_position[0], current_position[1]]:
                # Remapping current position to new pre-position
                self.close(current_position, pre_pos)
                self.distance_matrix[current_position[0], current_position[1]] = distance_to_start

            if self.check_closed(self.goal):
                # Backtrack the path from goal
                return self.backtrack(self.goal)

            for i, m in enumerate(self.list_move):
                next_pos = current_position + m

                # Check if next position is a valid position
                if self.check_position(next_pos, matrix_graph):
                    continue



                self.push(next_pos, current_position, distance_to_start)

        return False

    def push(self, position, prev_pos, distance_to_start):
        distance = sum(abs(self.goal - position)) + distance_to_start + 1
        heapq.heappush(self.queue, (distance, next(tiebreaker), distance_to_start+1, position, prev_pos))


    def check_queue(self, position):
        '''Check if position is in open set'''
        for x in self.queue:
            if (x[3] == position).all():
                return True

    def pop(self):
        v = heapq.heappop(self.queue)
        return v[3], v[4], v[2]
