import random
import unittest
import pickle
import networkx
import matplotlib.pyplot as plt

from explorable_graph import ExplorableGraph
from priority_queue import PriorityQueue
from searching import breadth_first_search, uniform_cost_search, \
                      euclidean_dist_heuristic, a_star, bidirectional_ucs, \
                      bidirectional_a_star

class TestPriorityQueue(unittest.TestCase):
    def test_append_and_pop(self):
        """Test the append and pop functions"""
        queue = PriorityQueue()
        temp_list = []

        for _ in xrange(10):
            a = random.randint(0, 10000)
            queue.append((a, 'a'))
            temp_list.append(a)

        temp_list = sorted(temp_list)

        for item in temp_list:
            popped = queue.pop()
            self.assertEqual(item, popped[0])

class TestBasicSearch(unittest.TestCase):
    """Test the simple search algorithms: BFS, UCS, A*"""

    def setUp(self):
        """Romania map data from Russell and Norvig, Chapter 3."""
        romania = pickle.load(open('romania_graph.pickle', 'rb'))
        self.romania = ExplorableGraph(romania)
        self.romania.reset_search()

    def test_bfs(self):
        """Test and visualize breadth-first search"""
        start = 'a'
        goal = 'u'

        node_positions = {n: self.romania.node[n]['pos'] for n in
                          self.romania.node.keys()}

        self.romania.reset_search()
        path = breadth_first_search(self.romania, start, goal)

        self.draw_graph(self.romania, node_positions=node_positions,
                        start=start, goal=goal, path=path)

    def test_ucs(self):
        """Test and visualize uniform-cost search"""
        start = 'a'
        goal = 'u'

        node_positions = {n: self.romania.node[n]['pos'] for n in
                          self.romania.node.keys()}

        self.romania.reset_search()
        path = uniform_cost_search(self.romania, start, goal)

        self.draw_graph(self.romania, node_positions=node_positions,
                        start=start, goal=goal, path=path)

    def test_a_star(self):
        """Test and visualize A* search"""
        start = 'a'
        goal = 'u'

        node_positions = {n: self.romania.node[n]['pos'] for n in
                          self.romania.node.keys()}

        self.romania.reset_search()
        path = a_star(self.romania, start, goal)

        self.draw_graph(self.romania, node_positions=node_positions,
                        start=start, goal=goal, path=path)

    def test_bidirectional_ucs(self):
        """Test and visualize bidirectional UCS search"""
        start = 'a'
        goal = 'u'

        node_positions = {n: self.romania.node[n]['pos'] for n in
                          self.romania.node.keys()}

        self.romania.reset_search()
        path = bidirectional_ucs(self.romania, start, goal)

        self.draw_graph(self.romania, node_positions=node_positions,
                        start=start, goal=goal, path=path)

    def test_bidirectional_a_star(self):
        """Test and visualize bidirectional A* search"""
        start = 'a'
        goal = 'u'

        node_positions = {n: self.romania.node[n]['pos'] for n in
                          self.romania.node.keys()}

        self.romania.reset_search()
        path = bidirectional_a_star(self.romania, start, goal)

        self.draw_graph(self.romania, node_positions=node_positions,
                        start=start, goal=goal, path=path)

    @staticmethod
    def draw_graph(graph, node_positions=None, start=None, goal=None,
                   path=None):
        """Visualize results of graph search"""
        explored = list(graph.explored_nodes)

        labels = {}
        for node in graph:
            labels[node] = node

        if node_positions is None:
            node_positions = networkx.spring_layout(graph)

        networkx.draw_networkx_nodes(graph, node_positions)
        networkx.draw_networkx_edges(graph, node_positions, style='dashed')
        networkx.draw_networkx_labels(graph, node_positions, labels)

        networkx.draw_networkx_nodes(graph, node_positions, nodelist=explored,
                                     node_color='g')

        if path is not None:
            edges = [(path[i], path[i + 1]) for i in range(0, len(path) - 1)]
            networkx.draw_networkx_edges(graph, node_positions, edgelist=edges,
                                         edge_color='b')

        if start:
            networkx.draw_networkx_nodes(graph, node_positions,
                                         nodelist=[start], node_color='b')

        if goal:
            networkx.draw_networkx_nodes(graph, node_positions,
                                         nodelist=[goal], node_color='y')

        plt.plot()
        plt.show()

if __name__ == '__main__':
    unittest.main()
