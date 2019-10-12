from path_finder import BFS, DFS, GreedySearch
from path_finder import AStarSearch
from graph_generator import read_input_file
import time
import argparse


SEARCH_MAP = {
    "BFS": BFS,
    "DFS": DFS,
    "Greedy": GreedySearch,
    "A*": AStarSearch
}

def parse_args():
    parser = argparse.ArgumentParser("Benchmark script for search function")
    parser.add_argument("--search_name", help="Search function name, support DFS, BFS, A*, Greedy", default="BFS")
    parser.add_argument("--input_file", help="Input file path with teacher format", default="sample_input.txt")
    
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    input_path = args.input_file
    matrix, start, goal = read_input_file(input_path)
    
    if args.search_name not in SEARCH_MAP:
        print(f"[WARN] {args.search_name} not supported")
        print("We will use BFS instead")
        args.search_name = "BFS"

    method = SEARCH_MAP[args.search_name]
    
    path_finder = method(start, goal)
    start_time = time.clock()
    path = path_finder.search(matrix)
    end_time = time.clock()
    if path:
        print("Found path")
        print(path)
        print("Length path:", len(path))
        print("Exec time:", end_time - start_time)
        
    else:
        print("Not found path")