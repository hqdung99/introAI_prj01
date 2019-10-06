


class BasePathFinder(object):
    """ Base class for all path finder logic
        Please implement search function

    """

    def __init__(self, *args, **kwargs):
        """
        Input:
            start: Tuple for start coordinate
            goal: Tuple for goal coordinate
            list_move: List valid move to update

        """
        pass



    def search(self, matrix_graph, *args ,**kwargs):
        raise NotImplementedError()
