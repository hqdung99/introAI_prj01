from .bfs_path import BFS

class DFS(BFS):
    def pop(self):
        return self.queue.pop()