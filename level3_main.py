from path_finder import BFS, DFS, GreedySearch
from path_finder import AStarSearch
from path_finder import AllPointSearch
from graph_generator import read_input_file
from graph_generator import read_multi_point_input
from PIL import Image
import imageio
import pylab as pl

import time
import argparse
import warnings
from matplotlib import pyplot as plt
from IPython.display import display

warnings.filterwarnings("ignore")

SEARCH_MAP = {
    "BFS": BFS,
    "DFS": DFS,
    "Greedy": GreedySearch,
    "A*": AStarSearch,
    "AllPointSearch": AllPointSearch
}

def parse_args():
    parser = argparse.ArgumentParser("Benchmark script for search function")
    parser.add_argument("--search_name", help="Search function name, support DFS, BFS, A*, Greedy, AllPointSearch", default="BFS")
    parser.add_argument("--input_file", help="Input file path with teacher format", default="sample_input.txt")
    parser.add_argument("--allpoint_type", help="which algorithm you want to use for AllPointSearch: DP, BruteForce, Greedy", default="DP")
    
    args = parser.parse_args()
    return args

def show_result(matrix, final_path, start, goal, list_point = None):
    if list_point:
        for point in list_point:
            matrix[point] = -5
    
    matrix[start] = 4
    matrix[goal] = 4
    fig = plt.figure()
    fig.canvas.draw()
    PATH_VALUE = 9
    for pos in final_path:
        if matrix[pos] == 0 or matrix[pos]==-5:
            matrix[pos] = PATH_VALUE
        else:
            matrix[pos] += 1
        pl.imshow(matrix)
        pl.pause(1e-2)
        pl.draw()

if __name__ == '__main__':
    args = parse_args()
    input_path = args.input_file
    
    if args.search_name not in SEARCH_MAP:
        print(f"[WARN] {args.search_name} not supported")
        print("We will use BFS instead")
        args.search_name = "BFS"
    
    # Handle AllPointSearch command
    if args.search_name == 'AllPointSearch':
        matrix, start, goal, list_point = read_multi_point_input(input_path)
        # check list of points to reach is exist or not
        if len(list_point) == 0:
            print('input file invalid')
            print('we will use 50x50.txt test')
            matrix, start, goal, list_point = read_multi_point_input('50x50.txt')
        # check algorithm type
        if args.allpoint_type != 'Greedy' and args.allpoint_type != 'DP' and args.allpoint_type != 'BruteForce':
            print('wrong algorithm name')
            print('we will use DP algorithm')
            args.allpoint_type = 'DP'

        if args.allpoint_type  == 'Greedy':
            use_heapq = True
        else:
            use_heapq = False
        all_point_finder = AllPointSearch(start, goal, list_point, args.allpoint_type, use_heapq=use_heapq, algo_to_find_shortest_point=BFS)
        start_time = time.clock()
        total_dist, final_path = all_point_finder.search(matrix)
        end_time = time.clock()
        if final_path:
            print("Found path")
            print("Length path:", total_dist)
            print("Exec time:", end_time - start_time)
            show_result(matrix, final_path, start, goal, list_point = list_point)
        else:
            print("Not found path")
        
    else:
        matrix, start, goal = read_input_file(input_path)
        method = SEARCH_MAP[args.search_name]

        path_finder = method(start, goal)
        start_time = time.clock()
        path = path_finder.search(matrix)
        end_time = time.clock()
        if path:
            print("Found path")
            print("Length path:", len(path))
            print("Exec time:", end_time - start_time)
            show_result(matrix, path, start, goal)
        else:
            print("Not found path")
