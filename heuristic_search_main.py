from path_finder import HeuristicSearch, manhattan
from graph_generator import read_input_file



if __name__ == '__main__':
    input_path = 'sample_input.txt'
    graph_gen, start, goal = read_input_file(input_path, return_graph_gen=True, verbose=True)
    flag_list = [1]
    path_finder = HeuristicSearch(start, goal, manhattan, flag_list=flag_list)



    path = path_finder.search(graph_gen, True)
    
    if path:
        print("Found path")
        print(path)
    else:
        print("Not found path")