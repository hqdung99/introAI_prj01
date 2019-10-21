from .bfs_path import BFS
import heapq
import numpy as np
import random
from itertools import count



tiebreaker = count(step=-11)


class GreedySearch(BFS):
    def __init__(self, start, goal, 
                list_move=[(0, 1), (0, -1), (1, 0), (-1, 0)],
                ):
        super().__init__(start, goal, list_move)
        self.queue = []
        

    def push(self, position, prev_pos):
        distance = sum(abs(self.goal - position))
        # Try generating random number to ensure no value equal
        heapq.heappush(self.queue, (distance, next(tiebreaker), position, prev_pos))

    def check_queue(self, position):
        '''Check if position is in open set'''
        for x in self.queue:
            if (x[2] == position).all():
                return True

    def pop(self):
        v = heapq.heappop(self.queue)

        return v[2], v[3]
