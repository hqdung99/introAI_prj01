from .greedy_search import GreedySearch
import numpy as np
import heapq
import random


class AStarSearch(GreedySearch):
    def search(self, matrix_graph):
        # Init queue
        # Queue data struct: <coor, prev_pos> 
        self.push(self.start, -1, 0)


        # Init closed set
        # Closed data struct: np array for backtrack    
        closed_shape = (*matrix_graph.shape, len(matrix_graph.shape))
        self.closed = np.zeros(closed_shape, dtype=int)
        self.closed.fill(-1)


        while len(self.queue) != 0:
            current_position, pre_pos, count = self.pop()
            self.close(current_position, pre_pos)

            if self.check_closed(self.goal):
                # Backtrack the path from goal
                return self.backtrack(self.goal)

            for i, m in enumerate(self.list_move):
                next_pos = current_position + m

                # Check if next position is a valid position
                if self.check_position(next_pos, matrix_graph):
                    continue



                self.push(next_pos, current_position, count)

        return False

    def push(self, position, prev_pos, count):
        distance = np.sum(np.abs(self.goal - position)) + count + 1
        rand = random.randint(0, 10000)
        heapq.heappush(self.queue, (distance, rand, count+1, position, prev_pos))


    def pop(self):
        v = heapq.heappop(self.queue)
        return v[3], v[4], v[2]
