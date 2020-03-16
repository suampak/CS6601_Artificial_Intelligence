"""Testing pbnt. Run this before anything else to get pbnt to work!"""
import sys

if('pbnt/lib' not in sys.path):
    sys.path.append('pbnt/lib')
if('pbnt/examples' not in sys.path):
    sys.path.append('pbnt/examples')
from exampleinference import inferenceExample

inferenceExample()
# Should output:
# ('The marginal probability of sprinkler=false:', 0.80102921)
#('The marginal probability of wetgrass=false | cloudy=False, rain=True:', 0.055)

'''
WRITE YOUR CODE BELOW.
'''

from random import randint, random
from pbnt.Node import BayesNode
from pbnt.Graph import BayesNet
from numpy import zeros, float32
import pbnt.Distribution as Distribution
from pbnt.Distribution import DiscreteDistribution, ConditionalDiscreteDistribution
from pbnt.Inference import JunctionTreeEngine, EnumerationEngine


def make_power_plant_net():
    """Create a Bayes Net representation of the above power plant problem.
    Use the following as the name attribute: "alarm","faulty alarm", "gauge","faulty gauge", "temperature". (for the tests to work.)
    """
    nodes = []
    # TODO: finish this function
    # raise NotImplementedError
    # create five variables
    

    return BayesNet(nodes)
