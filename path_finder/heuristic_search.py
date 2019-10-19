from . import NEGATIVE_INF, POSITIVE_INF
from .BasePathFinder import BasePathFinder
from .utils import check_position
from matplotlib import pyplot as plt
import numpy as np

# Heuristic Function template: 
def hfunc_template(state, agent_coor, goal, move, path):
    """ Heuristics function
    Input:
        state: Current state of matrix
        agent_coor: current coordinate of agent
        goal:
        move: Move to apply
        path:
    Output:
        score: float, higher better. 
    """
    pass


class HeuristicSearch(object):
    ALLOW_LOWER = 1

    def __init__(self, start, goal, 
                heuristic_function, 
                list_move=[(0, 1), (0, -1), (1, 0), (-1, 0)],
                flag_list=[], 
                min_best=True):
        self.start = np.array(start)
        self.goal = np.array(goal)
        self.list_move = list_move
        self.heuristic_function = heuristic_function
        self.min_best = min_best

        if HeuristicSearch.ALLOW_LOWER in flag_list:
            self.allow_lower = True
        else:
            self.allow_lower = False


        if self.min_best:
            self.invalid_move = POSITIVE_INF
        else:
            self.invalid_move = NEGATIVE_INF

    def search(self, graph, visualize=False):
        # init variable
        agent_coor = self.start
        next_move_point = np.zeros(len(self.list_move), dtype=np.float)
        path = []
        prev_score = self.invalid_move

        while (agent_coor != self.goal).any():
            for i, move in enumerate(self.list_move):
                score = self.heuristic_function(graph.generate_graph(), agent_coor, self.goal, move, path)
                next_move_point[i] = score
            
            if self.min_best:
                best_move_ind = next_move_point.argmin()
            else:
                best_move_ind = next_move_point.argmax()
            
            
            best_move = self.list_move[best_move_ind]
            best_score = next_move_point[best_move_ind]

            if not self.allow_lower:
                if best_score < prev_score:
                    print("No better score than previous found.")
                    return path

            if best_score == self.invalid_move:
                print("No valid move found")
                return path

            agent_coor = self.apply_move(agent_coor, best_move,
                        graph=graph)
            path.append(agent_coor)
            print(agent_coor, best_score)
            
            if visualize:
                matrix = graph.generate_graph()
                matrix[agent_coor[0], agent_coor[1]] = 10
                matrix[self.goal[0], self.goal[1]] = 11
                plt.imshow(matrix)
                plt.show()
        
        return path            

    def apply_move(self, agent_coor, move, **kwargs):
        # For later implementation of level 4 problem
        graph = kwargs['graph']
        print("Updating graph")
        graph.update(agent_coor + move, self.goal)
        return agent_coor + move


