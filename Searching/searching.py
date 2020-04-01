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
    return a_star(graph, start, goal, lambda G, s, g : 0)

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
                newDist = newPath[0]+heuristic(graph, node, goal)
                queue.append((newDist, newPath))

    raise Error('No path from {} to {}').format(start, goal)

def bidirectional_ucs(graph, start, goal):
    """
    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """
    return bidirectional_a_star(graph, start, goal, lambda G, s, g : 0)

def bidirectional_a_star(graph, start, goal, heuristic=euclidean_dist_heuristic):
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

    queue_s = PriorityQueue()
    queue_s.append((0, 0, start, ''))
    is_visited_s = {}
    queue_g = PriorityQueue()
    queue_g.append((0, 0, goal, ''))
    is_visited_g = {}
    small = [float('inf'),'']

    p = lambda g, s, t, n : (heuristic(g, n, t)-heuristic(g, n, s)+heuristic(g, t, s))/2

    while queue_s.size()+queue_g.size() > 0:
        est_s, dist_s, node_s, pa_s = queue_s.pop()
        est_g, dist_g, node_g, pa_g = queue_g.pop()

        # not really sure about the ending criteria for a*
        if est_s+est_g >= small[0]+2*p(graph, start, goal, start):
            node = small[1]
            ret = [node]
            ptr = node
            while is_visited_s[ptr][1] != '':
                ret.append(is_visited_s[ptr][1])
                ptr = is_visited_s[ptr][1]
            ret.reverse()

            ptr = node
            while is_visited_g[ptr][1] != '':
                ret.append(is_visited_g[ptr][1])
                ptr = is_visited_g[ptr][1]

            return ret

        """
            forward/backward search
        """
        for queue, is_visited, is_visited_other, node, dist, pa, t, s in \
            [[queue_s, is_visited_s, is_visited_g, node_s, dist_s, pa_s, goal, start], \
             [queue_g, is_visited_g, is_visited_s, node_g, dist_g, pa_g, start, goal]]:
            if is_visited.get(node) is not None:
                continue
            is_visited[node] = [dist, pa]
            if is_visited_other.get(node) is not None:
                dist_cache, _ = is_visited_other[node]
                if dist_cache+dist < small[0]:
                    small = [dist_cache+dist, node]
            else:
                for dest in graph[node]:
                    new_dist = dist+graph[node][dest]['weight']
                    new_heuristic = p(graph,s,t,dest)
                    queue.append((new_dist+new_heuristic, new_dist, dest, node))

    raise Error('No path from {} to {}').format(start, goal)
