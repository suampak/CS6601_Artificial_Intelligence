from __future__ import division
import numpy as np
import math

class DecisionTree(object):
    class Node(object):
        def __init__(self, attr, value):
            self.attr_id = attr
            self.value = {v:None for v in value}

    def __init__(self, values, outcome):
        self.root = None
        self.__build_tree(values, outcome)

    def predict(self, value):
        ptr = self.root
        while len(ptr.value) > 0:
            v = value[ptr.attr_id]
            ptr = ptr.value[v]
        return ptr.attr_id

    def __build_tree(self, values, outcome):
        is_visited = [False]*len(values[0])
        chosen_attr_id = DecisionTree.__attr_selection(values, outcome, is_visited)
        unique_v = np.unique(values[:,chosen_attr_id], return_counts=False)
        self.root = DecisionTree.Node(chosen_attr_id, unique_v)
        is_visited[chosen_attr_id] = True
        for subv in unique_v:
            sub_values = values[np.where(values[:,chosen_attr_id]==subv)]
            sub_outcome = outcome[np.where(values[:,chosen_attr_id]==subv)]
            DecisionTree.__build_tree_impl(self.root,subv,sub_values,sub_outcome,is_visited)

    @staticmethod
    def __build_tree_impl(node, v, values, outcome, is_visited):
        # choose attr with highest information gain
        chosen_attr_id = DecisionTree.__attr_selection(values, outcome, is_visited)

        # base case: no remaining attr or information gain == 0
        if chosen_attr_id == -1:
            counts = np.bincount(outcome)
            node.value[v] = DecisionTree.Node(np.argmax(counts),[])
            return

        unique_v = np.unique(values[:,chosen_attr_id], return_counts=False)
        node.value[v] = DecisionTree.Node(chosen_attr_id, unique_v)
        is_visited[chosen_attr_id] = True
        for subv in unique_v:
            sub_values = values[np.where(values[:,chosen_attr_id]==subv)]
            sub_outcome = outcome[np.where(values[:,chosen_attr_id]==subv)]
            DecisionTree.__build_tree_impl(node.value[v],subv,sub_values,sub_outcome,is_visited)
        is_visited[chosen_attr_id] = False

    @staticmethod
    def __attr_selection(values, outcome, is_visited):
        # choose attr with highest information gain
        entropy = DecisionTree.__entropy(outcome)
        information_gain = 0
        chosen_attr_id = -1
        for attr_id in range(len(values[0])):
            if not is_visited[attr_id]:
                avg_info_entropy = DecisionTree.__average_info_entropy(values[:,attr_id],outcome)
                if information_gain < entropy - avg_info_entropy:
                    information_gain = entropy - avg_info_entropy
                    chosen_attr_id = attr_id

        return chosen_attr_id

    @staticmethod
    def __average_info_entropy(value, outcome):
        unique_values = np.unique(value, return_counts=False)
        avg_entropy = 0
        for uv in unique_values:
            sub_outcome = outcome[np.where(value==uv)]
            avg_entropy += (len(sub_outcome)/len(outcome))*DecisionTree.__entropy(sub_outcome)

        return avg_entropy

    @staticmethod
    def __entropy(outcome):
        neg = (outcome==0).sum()
        pos = (outcome==1).sum()
        total = neg+pos
        return -((neg/total)*math.log(neg/total,2) if neg > 0 else 0) - \
                ((pos/total)*math.log(pos/total,2) if pos > 0 else 0)

# outlook, temp, humidity, windy
values = np.array([['sunny','hot','high','weak'], \
                   ['sunny','hot','high','strong'], \
                   ['overcast','hot','high','weak'], \
                   ['rainy','mild','high','weak'], \
                   ['rainy','cool','normal','weak'], \
                   ['rainy','cool','normal','strong'], \
                   ['overcast','cool','normal','strong'], \
                   ['sunny','mild','high','weak'], \
                   ['sunny','cool','normal','weak'], \
                   ['rainy','mild','normal','weak'], \
                   ['sunny','mild','normal','strong'], \
                   ['overcast','mild','high','strong'], \
                   ['overcast','hot','normal','weak'], \
                   ['rainy','mild','high','strong']])
outcome = np.array([0,0,1,1,1,0,1,0,1,1,1,1,1,0])
dt = DecisionTree(values,outcome)
for v in values:
    print dt.predict(v)
