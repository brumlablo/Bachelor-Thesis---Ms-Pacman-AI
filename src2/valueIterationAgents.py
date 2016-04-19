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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
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
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        for k in range(0,iterations): # actual values = Value_k, counting new values Value_{k+1} = Value_k
            tmpValues = self.values.copy() # current values V_k
            for state in self.mdp.getStates():
                # legal actions for state
                actions = self.mdp.getPossibleActions(state)
                if mdp.isTerminal(state) or len(actions) == 0:
                    tmpValues[state] = 0
                    continue
                # maximalize = gain best possible action based on chance q-values
                value = float("-inf") # V_{k+1}
                for action in actions:
                    qvals = 0.0 # suma of q-values
                    qvals = self.getQValue(state, action)
                    # same as ...
                    # for nextState, probability in self.mdp.getTransitionStatesAndProbs(state, action):
                    #     tmp += probability * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))
                    if qvals > value: # best value possible
                        value = qvals
                tmpValues[state] = value
            self.values = tmpValues # update values for each state V_{k+1}

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action): #chance node
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.

          probability = transitionFunction(state,action,nextState)
          Q_k(state) = suma(probability * ( Reward(state,action,nextState) + discountFactor * Value_k(nextState)
        """
        qval = 0.0
        for nextState,probability in self.mdp.getTransitionStatesAndProbs(state, action):
            qval += probability * ( self.mdp.getReward(state,action,nextState) + self.discount * self.getValue(nextState))
        return qval

    def computeActionFromValues(self, state): # max node
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          Choosing optimal policy (similar to max node in Expectimax)
          Value*(state) = max action of Q-Value*(state) (state,action,nextState)
          = = PI*
        """
        # tuple (action,value)
        expectedValue = ["", float("-inf")]

        actions = self.mdp.getPossibleActions(state)
        # terminal node
        if len(actions) == 0:
            return None

        for action in actions:
            tmp = self.getQValue(state,action) # expected value
            if tmp > expectedValue[1]:
                expectedValue = (action,tmp)
        return expectedValue[0]

    # max node
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    # chance node
    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)
