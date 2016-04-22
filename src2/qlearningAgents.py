# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)

        # init Q-Values = current estimates for each Q*(state,action)
        self.qValues = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        # default - returning 0.0
        return self.qValues[(state,action)]

    def getValue(self, state):
        return self.computeValueFromQValues(state)

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        actions = self.getLegalActions(state)
        # terminal node
        if len(actions) == 0:
            return 0.0

        actionValue = float("-inf")

        for action in actions:
            tmp = self.getQValue(state, action)  # expected value
            if tmp > actionValue:
                actionValue = tmp
        #print "policy - best action value returned: ", actionValue
        return actionValue

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        actions = self.getLegalActions(state)
        # terminal state
        if len(actions) == 0:
            return None

        bestPolicy = [("", float("-inf"))]
        for action in actions:
            tmp = self.getQValue(state, action)  # expected value
            if tmp > bestPolicy[0][1]:
                bestPolicy = [(action,tmp)]
            elif tmp == bestPolicy[0][1]: # randomness of same valued actions - optimizing
                bestPolicy.append((action,tmp))
        # bestPolicy.sort()
        #print "policyPairs: ", bestPolicy
        return (random.choice(bestPolicy)[0])

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
        """
        actions = self.getLegalActions(state)
        # terminal state
        if len(actions) == 0:
            return None

        # probability
        if flipCoin(self.epsilon):
            return random.choice(actions) # random action
        else:
            return self.getPolicy(state) # best possible action

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a state = action => nextState and reward transition...
          Q-Value update:
          used here: Q(state,action) = Q(state,action) + alpha(reward+ discount * bestAction' Q(s',a') - Q(s,a))
          ==
          alternstive:Q(state,action) =  (1-alpha) Q(state,action) + alpha(reward + discount * bestAction' Q(state',action')).
        """
        self.qValues[(state,action)] = self.getQValue(state,action) + self.alpha * ((reward +
        self.discount * self.getValue(nextState)) - self.qValues[(state,action)])


class PacmanQAgent(QLearningAgent):
    "same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # Ms. Pacman index
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
