import heapq
import numpy as np
import random
from path_finder import BasePathFinder
from path_finder import BFS
import json

REACHED_POINT_FLAG = 88

class AllPointSearch():
    def __init__(self, start, goal, list_point, list_move=[(0, 1), (0, -1), (1, 0), (-1, 0)]):
        self.list_point = list_point
        self.start = start
        self.goal = goal
        self.list_move = list_move
        self.list_point = list_point

        ## this att is used for find path between two points:
        ## path_lookup[start][goal] = ['A', 'B', 'C', ...]
        self.path_lookup = {}
        self.visited = np.zeros((len(list_point), len(list_point)))
#         self.edges = []
#         self._init_edges()
    
    def _find_shortest_path(self, start_point, end_point, matrix):
        shortest_path_finder = BFS(start_point, end_point)
        return shortest_path_finder.search(matrix)
    
    def _init_path_lookup(self, matrix):
        matrix[goal] += 1
        for i, start_point in enumerate(list_point):
            shortest_path = self._find_shortest_path(self.start, start_point, matrix)
            self._update_path_lookup(self.start, start_point, shortest_path)
            
            for j in range(i+1, len(list_point)):
                end_point = list_point[j]
                if j == i or self.visited[i, j] == 1 or self.visited[j, i] == 1:
                    continue
                
                shortest_path = self._find_shortest_path(start_point, end_point, matrix)
                self._update_path_lookup(start_point, end_point, shortest_path)
                
                reverse_shortest_path = shortest_path.copy()
                if shortest_path != False:
                    reverse_shortest_path.reverse()
                    
                self._update_path_lookup(end_point, start_point, reverse_shortest_path)
                                
                self.visited[i, j] = 1
                self.visited[j, i] = 1
        
        matrix[goal] -= 1
        
    def _update_path_lookup(self, head, tail, path):
        if head not in self.path_lookup:
            self.path_lookup[head] = []
        
        dist = 1e9
        if path != False:
            dist = len(path)
        #heapq.heappush(self.path_lookup[head], (dist, tail, path))
        self.path_lookup[head].append((dist, tail, path))
    
    def _lookup_path_of_point(self, start_point):
        return heapq.heappop(self.path_lookup[start_point])
    
    def show_path_lookup(self):
        print(f'path_lookup type: {type(self.path_lookup)}')
        print(f'path_lookup key: {list(self.path_lookup.keys())}')
        print(f'path_lookup: {self.path_lookup}')
    
    def search(self, matrix):
        self._init_path_lookup(matrix)
        #self.show_path_lookup()
        #pretty(self.path_lookup, indent=2)
        
        final_path = [] # list of points that leads to goal
        reaching_order = [] # order of points we will reach - dtype: list of points
        total_distance = 0
        
        start_point = self.start
        num_of_list_point = len(list_point)
        
        while num_of_list_point > 0:
            distance, next_point, path = self._lookup_path_of_point(start_point)
            
            if matrix[next_point] != REACHED_POINT_FLAG:
                total_distance += distance
                final_path += path
                reaching_order+= [next_point]
                
                matrix[next_point] = REACHED_POINT_FLAG
                start_point = next_point
                num_of_list_point-=1

        
        ## find shortest path from the final point to goal
        shortest_path_to_goal = self._find_shortest_path(reaching_order[-1], goal, matrix)

        total_distance += len(shortest_path_to_goal)
        reaching_order.append(goal)
        final_path.extend(shortest_path_to_goal)
        
        return final_path, reaching_order, total_distance