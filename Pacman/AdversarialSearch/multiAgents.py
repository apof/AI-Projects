# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newCapsules = successorGameState.getCapsules()
        newScaredTimes = []
        for ghostState in newGhostStates:
          newScaredTimes.append(ghostState.scaredTimer)

        evaluation = 0

        # den theloume kapoio fantasma to opoio einai energo dhl den mporoume na fame 
        # na plhsiasei se apostash mikroterh tou 3, arketa konta mas dhladh
        distance = 0
        if newScaredTimes[0] == 0:
          for ghostState in newGhostStates:
            distance = abs(ghostState.getPosition()[0] - newPos[0]) + abs(ghostState.getPosition()[1] - newPos[1])
            if (distance <= 3):
              evaluation -= 10000

        # theloume h  thesh sthn opoia vriskomaste na exei faghto
        if currentGameState.hasFood(newPos[0], newPos[1]):
          evaluation += 1000

        # den theloume na stamatame
        if action == Directions.STOP:
          evaluation -= 20
          
        # oso pio konta einai to kontinotero faghto toso to kalytero
        minDistToFood = float("inf")
        for food in newFood:
          currDist = abs(food[0] - newPos[0]) + abs(food[1] - newPos[1])
          if(currDist < minDistToFood):
            minDistToFood = currDist
        evaluation += 10/minDistToFood


        # oso pio konta einai h kontinoterh capsule toso to kalytero
        minDistToCaps= float("inf")
        for capsule in newCapsules:
          currDist = abs(capsule[0] - newPos[0]) + abs(capsule[1] - newPos[1])
          if(currDist < minDistToCaps):
            minDistCaps = currDist
        evaluation += 10/minDistToCaps

        return evaluation

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        (value,action) = self.minimax(gameState,0, 0)
        return action

    def minimax(self, state, agent, depth):


        # h synartsh minimax kalei analoga to agent orisma me to opoio kaleitai ton katallhlo agent kyklika
        # dhladh prwta ton pacman meta osa fantasmata exoume
        # molis klhthei kai to teleytaio fntasma 3anakalei ton pacman kai synexizei paromoiws
        # to depth ay3anetai ston max kathws 1 depth anaparistatai apo mia kinhsh gia kathe agent
        # 1 gia ton pacman kai mia gia ola ta fantasmata dhladh


        if ((depth == self.depth and agent % state.getNumAgents() == 0) or state.isWin() or state.isLose()):
            return self.evaluationFunction(state), None

        agent_index = agent % state.getNumAgents()
        if agent_index == 0:
            return self.max(state, 0, depth)
        return self.min(state, agent_index, depth)

    def min(self, state, agent, depth):
        
        ghost_actions = state.getLegalActions(agent)

        if not ghost_actions:
            return self.evaluationFunction(state), None

        value = float("inf")

        for action in ghost_actions:
            succ = state.generateSuccessor(agent,action)
            new_value, new_action = self.minimax(succ, agent + 1, depth)
            if new_value < value:
                value = new_value

        return value, None

    def max(self, state, agent, depth):

        pacman_actions = state.getLegalActions(agent)

        if not pacman_actions:
            return self.evaluationFunction(state), None

        value = -float("inf")

        for action in pacman_actions:
            succ = state.generateSuccessor(agent,action)
            new_value, new_action = self.minimax(succ, agent + 1, depth + 1)
            if new_value > value:
                value = new_value
                value_action = action

        return value, value_action



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        (max_value,action) = self.minimax(gameState,0, 0,-float("inf"),float("inf"))
        return action

    def minimax(self, state, agent, depth,alpha,beta):


        if ((depth == self.depth and agent % state.getNumAgents() == 0) or state.isWin() or state.isLose()):
            return self.evaluationFunction(state), None

        agent_index = agent % state.getNumAgents()
        if agent_index == 0:
            return self.max(state, 0, depth,alpha,beta)
        return self.min(state, agent_index,depth,alpha,beta)

    def min(self, state, agent, depth,alpha,beta):
        
        ghost_actions = state.getLegalActions(agent)

        if not ghost_actions:
            return self.evaluationFunction(state), None

        value = float("inf")

        for action in ghost_actions:
            succ = state.generateSuccessor(agent,action)
            new_value, new_action = self.minimax(succ, agent + 1, depth,alpha,beta)
            if new_value < alpha:
              value = new_value
              return value, None
            if new_value < value:
              value = new_value

            beta = min(beta,new_value)
    
        return value, None

    def max(self, state, agent, depth,alpha,beta):

        pacman_actions = state.getLegalActions(agent)

        if not pacman_actions:
            return self.evaluationFunction(state), None

        value = -float("inf")

        for action in pacman_actions:
            succ = state.generateSuccessor(agent,action)
            new_value, new_action = self.minimax(succ, agent + 1, depth + 1,alpha,beta)
            if new_value > beta:
              value = new_value
              value_action = action
              return value, value_action
            if new_value > value:
              value = new_value
              value_action = action

            alpha = max(alpha,new_value)
    
        return value, value_action

    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        (value,action) = self.minimax(gameState,0, 0)
        return action

    def minimax(self, state, agent, depth):

        
        if ((depth == self.depth and agent % state.getNumAgents() == 0) or state.isWin() or state.isLose()):
            return self.evaluationFunction(state), None

        agent_index = agent % state.getNumAgents()
        if agent_index == 0:
            return self.max(state, 0, depth)
        return self.chance(state, agent_index, depth)

    def chance(self, state, agent, depth):
        
        ghost_actions = state.getLegalActions(agent)

        if not ghost_actions:
            return self.evaluationFunction(state), None

        value = float("inf")

        prob = 1.0/float(len(ghost_actions))
        expectvalue = 0.0

        for action in ghost_actions:
            succ = state.generateSuccessor(agent,action)
            new_value, next_action = self.minimax(succ, agent + 1, depth)
            expectvalue += new_value*prob

        return expectvalue, None

    def max(self, state, agent, depth):

        pacman_actions = state.getLegalActions(agent)

        if not pacman_actions:
            return self.evaluationFunction(state), None

        value = -float("inf")

        for action in pacman_actions:
            succ = state.generateSuccessor(agent,action)
            new_value, new_action = self.minimax(succ, agent + 1, depth + 1)
            if new_value > value:
                value = new_value
                value_action = action

        return value, value_action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    newGhostStates = currentGameState.getGhostStates()
    newCapsules = currentGameState.getCapsules()
    newScaredTimes = []
    for ghostState in newGhostStates:
        newScaredTimes.append(ghostState.scaredTimer)

    # xreishmopoiw to get score gia na exw thn poinh analoga me tis kinhseis pou kanw
    evaluation = currentGameState.getScore()

    # apostash apo fantasmata
    # koitaw thn apostash apo ta fantasmata
    # 1) ama kapoio mporw na to faw ayto einai kati pou to thelw
    # 2) den theloume kapoio fantasma pou einai energo na einai poly konta mas
    # ara afairoume poly ama afto apexei apostash 1 apo ton pacman kai analoga ligotero oso makrytera
    # apo ton pacman einai

    
    
    # oso pio konta einai h kontinoterh capsule toso to kalytero
    minDistToCaps= float("inf")
    for capsule in newCapsules:
        currDist = abs(capsule[0] - newPos[0]) + abs(capsule[1] - newPos[1])
        if(currDist < minDistToCaps):
            minDistCaps = currDist
    evaluation += 10/minDistToCaps

    ghostVal = 0
    for ghostState in newGhostStates:
        distance = abs(newPos[0] - ghostState.getPosition()[0]) + abs(newPos[1]- ghostState.getPosition()[1])
        if distance > 0:
            if ghostState.scaredTimer > 0:
                ghostVal += 100 / distance
            else:
                if minDistToCaps < distance:
                    ghostVal += 10 / distance
                else:
                    if(distance == 1):
                        ghostVal -= 30 / distance
                    else:
                        ghostVal -= 10 / distance
    evaluation += ghostVal



    # oso pio konta einai to kontinotero faghto toso to kalytero
    minDistToFood = float("inf")
    for food in newFood:
        currDist = abs(food[0] - newPos[0]) + abs(food[1] - newPos[1])
        if(currDist < minDistToFood):
            minDistToFood = currDist
    evaluation += 10/minDistToFood

    return evaluation



    
# Abbreviation
better = betterEvaluationFunction

