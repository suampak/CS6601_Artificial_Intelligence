import Queue
import sets
import copy

def breadth_first_search(graph, start, goal):
    """
    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.
    Returns:
        The best path as a list from the start and goal nodes (including both).
    """
    if start == goal:
        return []

    queue = Queue.Queue()
    queue.put([start])
    isVisited = sets.Set()
    isVisited.add(start)

    while not queue.empty():
        nodes = queue.get()
        for node in graph[nodes[-1]]:
            if node == goal:
                nodes.append(goal)
                return nodes
            if node not in isVisited:
                newPath = copy.deepcopy(nodes)
                newPath.append(node)
                queue.put(newPath)
                isVisited.add(node)

    raise Error('No path from {} to {}').format(start, goal)
