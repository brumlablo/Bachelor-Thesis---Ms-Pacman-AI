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
    """

    def getAction(self, gameState):
        """
        getAction chooses among the best options according to the evaluation function.

        getAction takes a GameState and returns some Directions.X for some X in the
        set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]

        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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

        """
        # Getting successor GameSate and all needed info
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFoodGrid = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # evaluation function value
        value = 0

        # STOP ACTION
        #if(action == Directions.STOP):
        #    value -= 1

        # FOOD distances
        foodDists = []
        for food in newFoodGrid:
            foodDists.append(manhattanDistance(food,newPos))
        foodDists.sort()

        if(len(foodDists) > 0):
            value += foodDists[0] * (-1) # further the closest food is, lower the value is

        # lesser the food, significantly smaller the value
        value -= (successorGameState.getNumFood() * 20)
        # ACTIVE GHOSTS distances
        ghostDists = []
        for ghost in newGhostStates:
            ghostD = manhattanDistance(ghost.getPosition(),newPos)
            if ghost.scaredTimer > ghostD:
                value +=  ghost.scaredTimer * 1.5 + ghostD * (-1)
            else:
                ghostDists.append(ghostD)
        if(len(ghostDists) > 0):
            value += ghostDists[0] # closer the closest ghost is, lower the value is

        return value

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

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.pacmanIndex = 0
        self.agentsNum = 0

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Minimax agent
    """

    def Minimax(self, state, agentIndex, depth):

        # new layer
        if agentIndex >= self.agentsNum:
            agentIndex = 0
            depth += 1

        # last layer or terminal node
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        # ms. pacman
        if agentIndex == self.index:
            return self.maximize(state, agentIndex, depth)
        # ghosts
        else:
            return self.minimize(state, agentIndex, depth)

    def minimize(self, state, agentIndex, depth):

        # tuple (action,value)
        value = ("", float("inf"))
        for action in state.getLegalActions(agentIndex):
            #if action == Directions.STOP:
            #    continue

            tmp = self.Minimax(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth)

            # getting value
            if type(tmp) is tuple:
                tmp = tmp[1]
            # returning tuple with action
            if tmp < value[1]:
                value = (action,tmp)
        print "min: ", value, " agent: ", agentIndex
        return value

    def maximize(self, state, agentIndex, depth):

        # tuple (action,value)
        value = ("", float("-inf"))
        for action in state.getLegalActions(agentIndex):
            #if action == Directions.STOP:
            #    continue

            tmp = self.Minimax(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth)
            # getting value
            if type(tmp) is tuple:
                tmp = tmp[1]
            # returning tuple with action
            if tmp > value[1]:
                value = (action, tmp)
        print "max: ",value," agent: " ,agentIndex
        return value

    def getAction(self, gameState):
        """
          returns minimax action from the current gameState

          FRAMEWORK IMPLEMENTATION NOTES
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        self.agentsNum = gameState.getNumAgents()
        value = self.Minimax(gameState, self.index, 0)
        print "FINAL VALUE: ",value[0]
        return value[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      minimax agent with alpha-beta pruning
    """

    def AlphaBeta(self, state, agentIndex, depth, alpha, beta):

        # new layer
        if agentIndex >= self.agentsNum:
            agentIndex = 0
            depth += 1

        # last layer or terminal node
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        # ms. pacman
        if agentIndex == self.index:
            return self.maximize(state, agentIndex, depth, alpha, beta)
        # ghosts
        else:
            return self.minimize(state, agentIndex, depth, alpha, beta)

    def maximize(self, state, agentIndex, depth, alpha, beta):

        # tuple (action,value)
        value = ("", float("-inf"))
        for action in state.getLegalActions(agentIndex):
            if action == Directions.STOP:
                continue

            tmp = self.AlphaBeta(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth,alpha, beta)
            # returning tuple with action
            if type(tmp) is tuple:
                tmp = tmp[1]

            if tmp > value[1]:
                value = (action, tmp)

            if value[1] >= beta:
                print "MAX PRUNE: ", value, " agent: ", agentIndex, "beta: ", beta
                return value

            alpha = max(alpha, value[1])
            print "alpha: ", alpha

            print "MAX FINAL ", value, " agent: ", agentIndex
        return value


    def minimize(self, state, agentIndex, depth, alpha, beta):

        # tuple (action,value)
        value = ("", float("inf"))
        for action in state.getLegalActions(agentIndex):
            if action == Directions.STOP:
                continue

            tmp = self.AlphaBeta(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth, alpha, beta)
            # getting value
            if type(tmp) is tuple:
                tmp = tmp[1]
            # returning tuple with action
            if tmp < value[1]:
                value = (action, tmp)
            # pruning
            if value[1] <= alpha:
                print "MIN PRUNE: ", value, " agent: ", agentIndex, "alpha: ", alpha
                return value

            beta = min(beta, value[1])
            print "beta: ", beta

            print "MIN FINAL ", value, " agent: ", agentIndex
        return value

    def getAction(self, gameState):
        """
          Returns alphabeta action
        """
        self.agentsNum = gameState.getNumAgents()
        value = self.AlphaBeta(gameState, self.index, 0, float("-inf"), float("inf"))
        print "FINAL VALUE: ",value[0]
        return value[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

