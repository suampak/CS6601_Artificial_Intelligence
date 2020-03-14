import Queue
import sets
import copy

from priority_queue import PriorityQueue
from scipy.spatial import distance

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

def uniform_cost_search(graph, start, goal):
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

    queue = PriorityQueue()
    queue.append((0, [start]))
    isVisited = sets.Set()

    while queue.size() > 0:
        dist, nodes = queue.pop()
        if nodes[-1] not in isVisited:
            isVisited.add(nodes[-1])
            if nodes[-1] == goal:
                return nodes
            for node in graph[nodes[-1]]:
                newPath = copy.deepcopy(nodes)
                newPath.append(node)
                queue.append((dist+graph[nodes[-1]][node]['weight'], newPath))

    raise Error('No path from {} to {}').format(start, goal)

def euclidean_dist_heuristic(graph, v, goal):
    """
    Args:
        graph (ExplorableGraph): Undirected graph to search.
        v (str): Key for the node to calculate from.
        goal (str): Key for the end node to calculate to.
    Returns:
        Euclidean distance between `v` node and `goal` node
    """
    return distance.euclidean(graph.node[v]['pos'], graph.node[goal]['pos'])

def a_star(graph, start, goal, heuristic=euclidean_dist_heuristic):
    """
    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.
    Returns:
        The best path as a list from the start and goal nodes (including both).
    """
    if start == goal:
        return []

    queue = PriorityQueue()
    queue.append((0, [0, start]))
    isVisited = sets.Set()

    while queue.size() > 0:
        dist, nodes = queue.pop()
        if nodes[-1] not in isVisited:
            isVisited.add(nodes[-1])
            if nodes[-1] == goal:
                return nodes[1:]
            for node in graph[nodes[-1]]:
                newPath = copy.deepcopy(nodes)
                newPath.append(node)
                newPath[0] += graph[nodes[-1]][node]['weight']
                newDist = newPath[0]+heuristic(graph, nodes[-1], node)
                queue.append((newDist, newPath))

    raise Error('No path from {} to {}').format(start, goal)
