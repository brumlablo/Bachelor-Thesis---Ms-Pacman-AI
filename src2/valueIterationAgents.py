# valueIterationAgents.py
# -----------------------
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


#------------------------------------------------------------------------------------------------#
# BP: implemented Value Iteration agent

# AGENTS MANUAL
# VALUE ITERATION + BASIC Q-LEARNING AGENTS
# basic usage examples:
# (more in help: python gridworld.py -h)
    # -g TypeOfGrid: BookGrid (default), BridgeGrid, DiscountGrid, ...
    # -a agentType: "value" for ValueIterationAgent, "q" for "QLearningAgent"
    # -i NumberOfIterations: similar to depth, default: 10
    # -k  NumberOfEpisodes: episodes of performing optimal policy, default = 10
    # --discount value: gamma, defualt 0.9
    # --noise value<1: non-deterministic probability
    # --livingReward value: default 0.0
    # --epsilon value:probability of actions
    # --learningRate value: aplha
#
# EXAMPLES
#
# VALUE ITERATION AGENT - USED WITH gridworld.py
# default map, 100 iterations, 10 episodes
# python gridworld.py -a value -i 100 -k 10
#
# type of grid: DiscountGrid , 5 iterations, default 10 episodes
# python gridworld.py -a value -i 5 -g DiscountGrid
#
# type of grid: BridgeGrid , 100 iterations, gamma = 0.9, noise =  0.2
# python gridworld.py -a value -i 100 -g BridgeGrid --discount 0.9 --noise 0.2
#
# Q-LEARNING AGENT EXAMPLES n qlearningAgents.py
#------------------------------------------------------------------------------------------------#

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        A ValueIterationAgent takes a Markov decision process
        (mdp.py) on initialization, (gets initial values of
        transition function and reward) and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp # model
        self.discount = discount # gamma
        self.iterations = iterations
        self.values = util.Counter() # dict with default 0 (used for TERMINAL_STATE type)
        # values structure is dict with (x,y) grid position: value of the position
        # e.g. [(0,1):-10.0,(5,3):0.0]

        for k in range(iterations): # iterations + 1 for V0 layer
            futureValues = self.values.copy() # V_{k+1} <- V_k
            for state in self.mdp.getStates():
                actions = self.mdp.getPossibleActions(state) # possible actions for state
                # terminal node test
                if mdp.isTerminal(state) or len(actions) == 0:
                    futureValues[state] = 0
                    continue

                # maximalize = gain best possible VALUE based on chance Q-VALUES
                value = float("-inf") # V_{k+1}
                for action in actions:
                    #print "         action:",action
                    expectedQValue = 0.0 # suma of q-values for resulting state s'
                    expectedQValue = self.getQValue(state, action)
                    if expectedQValue > value: # best value possible of expected rewards
                        value = expectedQValue
                #print "             newstatevalue: ",value
                futureValues[state] = value
                #st += 1
            self.values = futureValues # update values for each state V_{k+1}

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    # ------------------------------------------------------------------------------------------------#
    # return expected future utility of Q(state,action) (chance node) from V(state)
    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        qval = 0.0
        # state,probability = model.transitionFunction(state,action,nextState)
        for nextState,probability in self.mdp.getTransitionStatesAndProbs(state, action):
            # averaging all nextStates
            # Q_k(state,action) = suma(probability * (Reward(state, action, nextState) + discountFactor * Value_k(nextState)
            qval += probability * ( self.mdp.getReward(state,action,nextState) + self.discount * self.getValue(nextState))
        return qval

    # ------------------------------------------------------------------------------------------------#
    # return state policy (max node)

    # called by environment (gridwrold.py) AFTER Value Iteration evaluation (after exploration)
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    # called by environment (gridwrold.py), returns directly the policy at the state (no exploration)
    def getAction(self, state):
        return self.computeActionFromValues(state)

    def computeActionFromValues(self, state):
        """
          RETURNS BEST POLICY BASED ON Q-VALUES OF STATE
          (policy = the best action in the given state based on current self.values)

          Choosing optimal policy (similar to max node in Expectimax)
          policy* = max action of Q-Value*(state) (state,action,nextState)
        """
        # tuple (action,value)
        #print "GETTING BEST POLICY"
        bestPolicy = ["", float("-inf")]

        actions = self.mdp.getPossibleActions(state)
        # terminal node
        if len(actions) == 0:
            return None

        for action in actions:
            tmp = self.getQValue(state,action) # expected value
            if tmp > bestPolicy[1]:
                bestPolicy = [action,tmp]
        #print "policy - best action returned: ",bestPolicy[0]
        return bestPolicy[0]
