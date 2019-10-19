from path_finder import BFS
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.gca(projection='3d')


matrix = np.zeros([9, 9, 9], dtype=np.uint8)

matrix[5:9, 3:9, 5:8] = 1

start = [0, 0, 0]
goal = [8, 8, 8]
list_move = [
    [1, 0, 0], [-1, 0, 0],
    [0, 1, 0], [0, -1, 0],
    [0, 0, 1], [0, 0, -1]
]
def visualize_3d(volume):
    x = np.arange(volume.shape[0])[:, None, None]
    y = np.arange(volume.shape[1])[None, :, None]
    z = np.arange(volume.shape[2])[None, None, :]
    x, y, z = np.broadcast_arrays(x, y, z)

    # Turn the volumetric data into an RGB array that's
    # just grayscale.  There might be better ways to make
    # ax.scatter happy.
    # c = np.tile(volume.ravel()[:, None], [1, 3])

    # Do the plotting in a single call.
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(x.ravel(),
            y.ravel(),
            z.ravel(),
            c=volume.ravel())
    fig.show()
    plt.show()
visualize_3d(matrix)

path = BFS(start, goal, list_move).search(matrix)
if path:
    print(path)
    for p in path:
        matrix[tuple(p)] = 2
        visualize_3d(matrix)