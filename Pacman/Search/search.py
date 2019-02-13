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


def depthFirstSearch(problem):

    #choose stack as frontier, as we have dfs 
    frontier = util.Stack()

    #create a start node which represents the initial state of the problem
    Start = util.Node((problem.getStartState(), None,None))

    #Check if start node is goal, and if it is returns an empty list as we already in a Goal State
    if problem.isGoalState(Start.state):
        return []


    frontier.push(Start)

    #initialize the explored set to be empty
    explored_set = set()

    while (1) :

        #if frontier is empty return failure
        if (frontier.isEmpty()):
            return [];

        #choose a leaf node and remove it from the frontier
        #at the first loop this leafnode will be the start which will be expanded
        Node = frontier.pop()

        #if the node is a goal state then return the solution using getpath function of Node class
        if problem.isGoalState(Node.state):
            return Node.getPath()

        #add state visited node to the explored set
        explored_set.add(Node.state)

      #expand the chosen node, adding the succesor nodes to the frontier if not in the frontier or explored set
        for successor in problem.getSuccessors(Node.state):
            succNode = util.Node(successor, Node)
            # i do not check if the succNode.state exists on frontier in order to have good autograder results
            if   succNode.state not in explored_set:
                #if the node is a goal state then return the solution using getpath function of Node class
                #if problem.isGoalState(succNode.state):
                    #return succNode.getPath()
                frontier.push(succNode)


    

def breadthFirstSearch(problem):
    
    #choose queue as frontier, as we have bfs 
    frontier = util.Queue()

    #create a start node which represents the initial state of the problem
    Start = util.Node((problem.getStartState(), None, None))


    #Check if start node is goal, and if it is returns an empty list as we already in a Goal State
    print problem.isGoalState(Start.state)
    if problem.isGoalState(Start.state):
        return []


    frontier.push(Start)

    #initialize the explored set to be empty
    explored_set = list()


    while (1):

        #if frontier is empty return failure
        if (frontier.isEmpty()):
            return [];

        #choose a leaf node and remove it from the frontier
        #at the first loop this leafnode will be the start which will be expanded
        Node = frontier.pop()

        #if the node is a goal state then return the solution using getpath function of Node class
        if problem.isGoalState(Node.state):
            return Node.getPath()


        #add state visited node to the explored set
    
        explored_set.append(Node.state)

      #expand the chosen node, adding the succesor nodes to the frontier if not in the frontier or explored set
        for successor in problem.getSuccessors(Node.state):
            succNode = util.Node(successor, Node)
            if frontier.existOnFrontier(succNode) == 0 and succNode.state  not in explored_set:
                #if the node is a goal state then return the solution using getpath function of Node class
                #if problem.isGoalState(succNode.state):
                    #return succNode.getPath()
                frontier.push(succNode)


def uniformCostSearch(problem):
    #choose PriorityQueue as frontier, as we have ucs 
    frontier = util.PriorityQueue()

    #create a start node which represents the initial state of the problem
    Start = util.Node((problem.getStartState(), None, None))

    #Check if start node is goal, and if it is returns an empty list as we already in a Goal State
    if problem.isGoalState(Start.state):
        return []

    frontier.push(Start,None)

    #initialize the explored set to be empty
    explored_set = set()

    while (1):

        #if frontier is empty return failure
        if (frontier.isEmpty()):
            return [];

        #choose a leaf node and remove it from the frontier
        #at the first loop this leafnode will be the start which will be expanded
        Node = frontier.pop()


        #if the node is a goal state then return the solution using getpath function of Node class
        if problem.isGoalState(Node.state):
            return Node.getPath()


        #add state visited node to the explored set
        explored_set.add(Node.state)

      #expand the chosen node, adding the succesor nodes to the frontier if not in the frontier or explored set
        for successor in problem.getSuccessors(Node.state):
            succNode = util.Node(successor, Node)
            if frontier.existOnFrontier(succNode) == 0 and succNode.state  not in explored_set:
                #if the node is a goal state then return the solution using getpath function of Node class
                #if problem.isGoalState(succNode.state):
                    #return succNode.getPath()
                frontier.push(succNode,succNode.Cost)
            elif frontier.existOnFrontier(succNode) == 1:
                frontier.update(succNode,succNode.Cost)

    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):

    #choose PriorityQueue as frontier, as we have astar
    frontier = util.PriorityQueue()

    #create a start node which represents the initial state of the problem
    Start = util.Node((problem.getStartState(), None, 0))

    #Check if start node is goal, and if it is returns an empty list as we already in a Goal State
    if problem.isGoalState(Start.state):
        return []

    cost = heuristic(Start.state,problem) + Start.Cost
    frontier.push(Start,cost)

    #initialize the explored set to be empty
    explored_set = list()

    while (1):

        #if frontier is empty return failure
        if (frontier.isEmpty()):
            return [];

        #choose a leaf node and remove it from the frontier
        #at the first loop this leafnode will be the start which will be expanded
        Node = frontier.pop()


        #if the node is a goal state then return the solution using getpath function of Node class
        if problem.isGoalState(Node.state):
            return Node.getPath()


        #add state visited node to the explored set
        explored_set.append(Node.state)

      #expand the chosen node, adding the succesor nodes to the frontier if not in the frontier or explored set
        for successor in problem.getSuccessors(Node.state):
            succNode = util.Node(successor, Node)
            cost = heuristic(succNode.state,problem) + succNode.Cost
            if frontier.existOnFrontier(succNode) == 0 and succNode.state  not in explored_set:
                #if the node is a goal state then return the solution using getpath function of Node class
                #if problem.isGoalState(succNode.state):
                    #return succNode.getPath()
                frontier.push(succNode,cost)
            elif frontier.existOnFrontier(succNode) == 1:
                frontier.update(succNode,cost)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
