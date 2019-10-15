from PIL import Image, ImageDraw
import numpy as np
from matplotlib import pyplot as plt
import random

class GraphGenerator(object):
    def __init__(self, size: tuple, mode:str="L", fill:bool=False,
        list_move=[(0, 1), (0, -1), (1, 0), (-1, 0)]) -> None:
        '''

        size: tuple of two interger.

        '''

        self.size = size

        self.__img = Image.new(mode, size)
        self.__draw = ImageDraw.ImageDraw(self.__img)
        self.polygon_list = []
        self.fill = fill
        self.list_move = list_move

    def add_polygon(self, polygon: list, 
                    polygon_ind: int = None) -> None:
        ''' Add polygon to image

        polygon: List of Tuple of two intergers represent coordinates
                for each vertex of polygon
        
        polygon_ind: Index for polygon in graph
        '''
        self.polygon_list.append(polygon)
        if polygon_ind is None:
            polygon_ind = len(self.polygon_list)
        
        if self.fill:
            fill = polygon_ind
        else:
            fill = None
        self.__draw.polygon(polygon, fill, polygon_ind)
    
    def generate_graph(self):
        return np.array(self.__img, dtype=int)

    def update(self, agent_coor, goal):
        prev_state = self.generate_graph()
        ind = random.randint(0, len(self.polygon_list) - 1)
        old_polygon = self.polygon_list[ind]
        
        self.__draw.polygon(old_polygon, 0, 0)

        pol_move = random.choice(self.list_move)
        new_polygon = []
        for point in old_polygon:
            point = np.array(point) + pol_move
            new_polygon.append(tuple(point))

        print(f"Polygon {ind} move {pol_move}")
        self.__draw.polygon(new_polygon, outline=ind + 1)
        self.polygon_list[ind] = new_polygon

    def plot_graph(self, cmap='tab20c'):
        plt.imshow(self.__img, cmap=cmap)
        plt.show()



def read_input_file(fpath:str, verbose:bool=False, fill:bool=False, return_graph_gen=False):
    """ Read input file with TA Format
    Input:
        fpath: Path to input txt file
        verbose: Print to screen to debug
        fill: Should we fill the polygon
    Output:
        graph: (Numpy array) Matrix to represent graph value
        start: (Tuple of int) Start point
        goal: (Tuple of int) Goal point


    """
    f = open(fpath)
    l = f.readline()
    w, h = [int(x) for x in l.strip().split(',')]

    if verbose:
        print("Read from file....")
        print(f"Width={w}, Height={h}")

    generator = GraphGenerator((h, w), fill=fill)
    
    l = f.readline()
    xStart, yStart, xGoal, yGoal = [int(x) for x in l.strip().split(',')]

    if verbose:
        print(f"Start: ({xStart}, {yStart})")
        print(f"Goal: ({xGoal}, {yGoal})")

    num_polygon = int(f.readline().strip())

    if verbose:
        print(f"Found {num_polygon} Polygons")
    for pInd in range(num_polygon):
        l = f.readline()
        point_list = [int(x) for x in l.strip().split(',')]
        polygon = list(zip(point_list[::2], point_list[1::2]))

        generator.add_polygon(polygon)

    f.close()

    if verbose:
        print("Done load input")
        generator.plot_graph()
    
    if return_graph_gen:
        return generator, (xStart, yStart), (xGoal, yGoal) 


    return generator.generate_graph(), (xStart, yStart), (xGoal, yGoal) 



if __name__ == '__main__':
    a, b, c = read_input_file('sample_input.txt', True)
    print(a)


    
