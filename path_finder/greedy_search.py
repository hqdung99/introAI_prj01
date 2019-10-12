from .bfs_path import BFS
import heapq
import numpy as np
import random



class GreedySearch(BFS):
    def __init__(self, start, goal, 
                list_move=[(0, 1), (0, -1), (1, 0), (-1, 0)],
                ):
        super().__init__(start, goal, list_move)
        self.queue = []
        

    def push(self, position, prev_pos):
        distance = np.sum(np.abs(self.goal - position))
        rand = random.randint(0, 10000)
        heapq.heappush(self.queue, (distance, rand, position, prev_pos))


    def pop(self):
        v = heapq.heappop(self.queue)
        return v[2], v[3]