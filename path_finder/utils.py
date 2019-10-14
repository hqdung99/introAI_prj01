from . import NEGATIVE_INF, POSITIVE_INF
import numpy as np

def check_position(position, matrix_graph):
    ''' Check if player can move to position or not
    Input: 
        position: Position need to check
        matrix_graph: State of matrix
    
    Output:
        return True if cannot move to that position
    '''
    if (position < 0).any():
        return True

    if (position >= matrix_graph.shape).any():
        return True 

    if matrix_graph[tuple(position)] > 0:
        return True
    
    return False



def manhattan(state, agent_coor, goal, move, path):
    new_position = agent_coor + move
    is_invalid = check_position(new_position, state)
    
    if is_invalid:
        return NEGATIVE_INF
    
    for p in path:
        if (new_position == p).all():
            return NEGATIVE_INF

    return np.sum(np.abs(goal - new_position))


