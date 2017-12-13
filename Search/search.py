# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

####* FOLLOWING CODE HAD BEEN ADDED TO COMPLETE ASSIGNMENTS Q1 - Q4: ####

class Node:
    def __init__(self, successor, parentNode=None):
      self.state = successor[0]
      self.action = successor[1]
      self.parentNode = parentNode
      self.pathCost = successor[2]
      if parentNode is not None and parentNode.pathCost is not None:
          self.pathCost += parentNode.pathCost

def getPath(node):
      path = list()
      currentNode = node
      while currentNode.action != None:
          path.insert(0, currentNode.action)
          currentNode = currentNode.parentNode
      return path
####* END OF ADDED CODE

####* FOLLOWING CODE HAD BEEN CHANGED TO COMPLETE ASSIGNMENTS Q1 - Q4: ####

def genericSearch(problem, openList, heuristic=nullHeuristic):
    closedList = []
    openList.push(Node((problem.getStartState(), None, 0), None), 0)

    while not openList.isEmpty():
        current = openList.pop()
        if current.state not in closedList:
            if problem.isGoalState(current.state):
                return getPath(current)
            else:
                closedList.append(current.state)
                for successor in problem.getSuccessors(current.state):
                    if successor[0] not in closedList:
                        nextNode = Node(successor, current)
                        openList.push(nextNode, nextNode.pathCost + heuristic(nextNode.state, problem))

def depthFirstSearch(problem):
    return genericSearch(problem, util.Stack())

def breadthFirstSearch(problem):
    return genericSearch(problem, util.Queue())

def uniformCostSearch(problem):
    return genericSearch(problem, util.PriorityQueue())

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    return genericSearch(problem, util.PriorityQueue(), heuristic)

####* END OF ADAPTED CODE ####

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
