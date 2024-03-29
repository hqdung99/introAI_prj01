import heapq
import numpy as np
import random
from path_finder import BasePathFinder
from path_finder import BFS
import json
import itertools

REACHED_POINT_FLAG = 88

class AllPointSearch():
    def __init__(self, start, goal, list_point, search_algorithm = 'dp' , use_heapq = True, algo_to_find_shortest_point = BFS, list_move=[(0, 1), (0, -1), (1, 0), (-1, 0)]):
        '''
            - start: start point
            - goal: goal point
            - list_point: list of points that we have to reach
            - use_heapq:
                True: if want to use lookup table as a priority queue.
                False: otherwise
            - algo_to_find_shortest_point: algorithm to find shortest path between given pair of points
            - list_move: list of actions
        '''
        
        self.list_point = list_point
        self.start = start
        self.goal = goal
        self.search_algorithm = search_algorithm
        
        self.list_move = list_move
        self.list_point = list_point
        self.algo_to_find_shortest_point = algo_to_find_shortest_point
        self.use_heapq = use_heapq
        
        ## this att is used for find path between two points:
        ## path_lookup[start][goal] = (distance, ['A', 'B', 'C', ...])
        self.path_lookup = {}
        self.visited = np.zeros((len(list_point), len(list_point)))
    


    # --------------------------------------------------------------------------------
    # CREATE PATH_LOOKUP DICTIONARY

    ### helper function 1
    def _find_shortest_path(self, start_point, end_point, matrix):
        '''
            find shortest path between a pair of points

            input: source, target
            output: result pattern of the correspondent algorithm used for this task
        '''
        shortest_path_finder = self.algo_to_find_shortest_point(start_point, end_point)
        return shortest_path_finder.search(matrix)
    
    ### helper function 2
    def _update_path_lookup(self, head, tail, path):
        if head not in self.path_lookup:
            if self.use_heapq:
                self.path_lookup[head] = []
            else:
                self.path_lookup[head] = {}
        
        dist = 1e9
        if path != False:
            dist = len(path)
        
        if self.use_heapq:
            self.path_lookup[head].append((dist, tail, path))
        else:
            self.path_lookup[head][tail] = (dist, path)

    ### helper function 3
    #def _calculate_and_update_shortet_root(self, start_point, end_point, matrix):
        

    ### main function
    def _init_path_lookup(self, matrix):
        '''
            Initiate lookup dictionary
            *path_lookup is dictionary:
                key: point1
                value: dictionary{ 
                    key: point2, 
                    values: tuple(distance: between point1 & point2, path: list of points that lead point1 to point2
                    }
        '''
        matrix[self.goal] += 1 #mark matrix[goal] != 0: prohibit searching some ways that go through goal point
        
        # start init path_lookup
        for i, start_point in enumerate(self.list_point):
            shortest_path = self._find_shortest_path(self.start, start_point, matrix)
            self._update_path_lookup(self.start, start_point, shortest_path)
            
            ## 
            if self.use_heapq == False:
                matrix[self.goal] -= 1
                shortest_path = self._find_shortest_path(start_point, self.goal, matrix)
                self._update_path_lookup(start_point, self.goal, shortest_path)
                matrix[self.goal] += 1

            ## find shortest path between each pair of points
            for j in range(i+1, len(self.list_point)):
                end_point = self.list_point[j]
                if j == i or self.visited[i, j] == 1 or self.visited[j, i] == 1:
                    continue
                
                ## update path_lookup[start][end]
                shortest_path = self._find_shortest_path(start_point, end_point, matrix)
                self._update_path_lookup(start_point, end_point, shortest_path)

                ## update path_lookup[end][start]
                if shortest_path != False:
                    reverse_shortest_path = shortest_path.copy()
                    reverse_shortest_path.reverse()
                else:
                    print(f'cannot find path between {start_point} - {end_point}')
                    continue
                self._update_path_lookup(end_point, start_point, reverse_shortest_path)
                                
                self.visited[i, j] = 1
                self.visited[j, i] = 1

        matrix[self.goal] -= 1
        
    # ----------------------------------------------------------------------------------
    # SEARCH ORDER OF POINTS TO REACH
    def _lookup_path_of_point(self, start_point):
        '''
            get information about how to reach to other points of a given point
            path_lookup data structure is a priority queue
            
            input: point1
            output: tupple of closest point compare to point1
        '''
        return heapq.heappop(self.path_lookup[start_point])

    # ------------------------------------------------------------------------------------------
    # ALGORITHM 1: GREEDY, TIME COMPLEXITY: O(N.logN)
    def search_always_choose_nearest_point(self, matrix):
        '''
            start searching: at each point, just choose the closest one

            output:
                - total_distance: total distance of final_path. dtype: int
                - final_path: final path from start_point to goal_point. dtype: list of points
        '''
        self._init_path_lookup(matrix)
        
        final_path = [] # list of points that leads to goal
        reaching_order = [] # order of points we will reach - dtype: list of points
        total_distance = 0
        
        start_point = self.start
        num_of_list_point = len(self.list_point)
        
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
        shortest_path_to_goal = self._find_shortest_path(reaching_order[-1], self.goal, matrix)
        
        total_distance += len(shortest_path_to_goal)
        reaching_order.append(self.goal)
        final_path.extend(shortest_path_to_goal)
        
        #return total cost, and list of points to reach this cost
        return total_distance, final_path

    

# --------------------------------------------------------------------
# ALGORITHM 2: BRUTE FORCE, TIME COMPLEXITY: O(N!)
    def _get_full_path_from_reaching_order(self, reaching_order):
        final_dist = 0
        final_path = []
        for i in range(len(reaching_order)-1):
            dist = self._get_path_info_between_two_points(reaching_order[i], reaching_order[i+1])
            final_dist += dist[0]
            final_path.extend(dist[1])
            
        return final_path, final_dist                                      
        
    def _get_path_info_between_two_points(self, start, end):
        try:
            return self.path_lookup[start][end]
        except Exception as e:
            print(f'get path fail with error: {str(e)}')
            
    '''
        brute force - O(n!)
    '''
    def search_shortest_with_all_possible_way(self, matrix):
        
        self._init_path_lookup(matrix)
        all_point_coor = [self.start] + self.list_point + [self.goal]
        
        numberPoint = 2 + len(self.list_point);
        arr = self.permutationPath(numberPoint);
        
        distanceStartToPoint = [];
        detailRoad = []

        for i in range(len(arr)):
            path = arr[i];
            dis = 0;
            subRoad = []
            for j in range(len(path) - 1):
                dis_info = self._get_path_info_between_two_points(all_point_coor[arr[i][j]], all_point_coor[arr[i][j+1]])
                dis += dis_info[0]
                
            distanceStartToPoint.append(dis);

        indexMin = distanceStartToPoint.index(min(distanceStartToPoint));

        ## traceback
        final_path = []
        
        mostOptimalPath = arr[indexMin]
        for point_ind in range(len(mostOptimalPath)-1):
            final_path += self.path_lookup[all_point_coor[mostOptimalPath[point_ind]]][all_point_coor[mostOptimalPath[point_ind+1]]][1]
        
        #return total cost to reach the mostOptimalPath, and list of points to reach the most optimal cost
        return distanceStartToPoint[indexMin], final_path
        
        
    def permutationPath(self, numberPoint):
        listA = list(range(1, numberPoint - 1));
        perm = itertools.permutations(listA);
        number = 0;
        arr = [];

        for i in list(perm):
            temp = [];
            temp.append(0);
            temp += list(i);
            temp.append(numberPoint - 1);
            arr.append(temp);

        return arr;
    
# ---------------------------------------------------------------------------------------
# ALGORITHM 3: DYNAMIC PROGRAMMING, TIME COMPLEXITY: O(2^N * N^2)
    def find_shortest_hamilton_path(self, matrix):
        self._init_path_lookup(matrix) 
        
        n = len(self.list_point)
        
        dp = []
        INF = 1e9
        
        for i in range(1<<n):
            dp.append([])
            for j in range(n):
                dp[i].append(INF)
        
        point_id = range(n)
        
        #init adj_matrix
        #adj_matrix[a][b]: distance between a and b
        adj_matrix=np.zeros((n, n))
        for i in range(n):
            dp[(1<<i)][i] = self._get_path_info_between_two_points(self.start, self.list_point[i])[0]
            for j in range(n):
                if i == j:
                    adj_matrix[i, j] = 0
                else:
                    dist_i_j = self._get_path_info_between_two_points(self.list_point[i], self.list_point[j])[0]
                    adj_matrix[i, j] = dist_i_j
        
        
        # find min_path
        for i in range(1<<n):
            for j in range(n):
                if (i & (1<<j)):
                    for k in range(n):
                        if (i & (1<<k)) and j!=k and adj_matrix[k, j] > 0:
                            dp[i][j] = min(dp[i][j], dp[i^(1<<j)][k] + adj_matrix[k, j])
        
        #find min last point
        min_point_id = -1
        min_cost = INF
        for i in range(n):
            dist = dp[(1<<n) -1][i] + self._get_path_info_between_two_points(self.list_point[i], self.goal)[0]
            if min_cost > dist:
                min_cost = dist
                min_point_id = i
        
        print(self.list_point[min_point_id])
        #----------------------------------------------------
        ## trace back for the path that end at min_point_id

        list_trace_id = [min_point_id]
        path = (1<<n) - 1
        res_visit = []
        for i in range(n):
            if (i!=min_point_id):
                res_visit.append(i)

        cur_id = min_point_id
        
        while(len(res_visit)):
            for i in res_visit:
                if dp[path^(1<<cur_id)][i] + adj_matrix[i, cur_id] == dp[path][cur_id]:
                    list_trace_id.append(i)
                    path = path^(1<<cur_id)
                    cur_id = i
                    res_visit.remove(i)
                    break
        
        final_path = [self.start]
        for i in list_trace_id[::-1]:
            final_path.append(self.list_point[i])
        final_path.append(self.goal)
        
        final_path, total_distance = self._get_full_path_from_reaching_order(final_path)
        return total_distance, final_path
# ---------------------------------------------------------------------------------------
# CHOOSE ALGORITHM
    def search(self, matrix):
        if self.search_algorithm == 'DP':
            return self.find_shortest_hamilton_path(matrix)
        if self.search_algorithm == 'BruteForce':
            return self.search_shortest_with_all_possible_way(matrix)
        if self.search_algorithm == 'Greedy':
            return self.search_always_choose_nearest_point(matrix)
        print(f'wrong search type')
        return None, None
        
        
        
        