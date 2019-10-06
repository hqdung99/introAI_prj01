from path_finder import BFS
from graph_generator import read_input_file


if __name__ == '__main__':
    input_path = 'sample_input.txt'
    matrix, start, goal = read_input_file(input_path)
    
    path_finder = BFS(start, goal)
    path = path_finder.search(matrix)
    
    if path:
        print("Found path")
        print(path)
    else:
        print("Not found path")