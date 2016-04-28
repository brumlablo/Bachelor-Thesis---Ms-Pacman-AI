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
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # dict with default 0 (used for TERMINAL_STATE type)
        # values structure is dict with (x,y) grid position: value of the position
        # e.g. [(0,1):-10.0,(5,3):0.0]

        st = 0
        for k in range(iterations): # iterations + 1 for V0 layer
            futureValues = self.values.copy() # current values V_k
            #print "----------------------------",k,"---------------------------"
            for state in self.mdp.getStates():
                #print "state: ",st,"...",state
                # legal actions for state
                actions = self.mdp.getPossibleActions(state)
                # terminal node test
                if mdp.isTerminal(state) or len(actions) == 0:
                    futureValues[state] = 0
                    continue

                # maximalize = gain best possible VALUE based on chance Q-VALUES
                value = float("-inf") # V_{k+1}
                for action in actions:
                    #print "         action:",action
                    expectedQValue = 0.0 # suma of q-values = resulting states s'
                    expectedQValue = self.getQValue(state, action)
                    if expectedQValue > value: # best value possible of expected rewards
                        value = expectedQValue
                #print "             newstatevalue: ",value
                futureValues[state] = value
                st += 1
            self.values = futureValues # update values for each state V_{k+1}

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    # expected future utility from a chance node = q-state
    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

    def computeQValueFromValues(self, state, action): #chance node
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        qval = 0.0
        # probability = transitionFunction(state,action,nextState)
        for nextState,probability in self.mdp.getTransitionStatesAndProbs(state, action):
            # averaging all nextStates
            # Q_k(state) = suma(probability * (Reward(state, action, nextState) + discountFactor * Value_k(nextState)
            qval += probability * ( self.mdp.getReward(state,action,nextState) + self.discount * self.getValue(nextState))
        return qval

    # choose best possible action = max node
    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns directly the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def computeActionFromValues(self, state): # max node
        """
          FINAL POLICY COMPUTING
          (policy = the best action in the given state
          according to the values currently stored in self.values)

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
                bestPolicy = (action,tmp)
        #print "policy - best action returned: ",bestPolicy[0]
        return bestPolicy[0]
