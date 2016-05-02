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

#------------------------------------------------------------------------------------------------#
# BP: imlemented:
# Q-Learning agents for
    # gridworld (QLearningAgent)
    # Ms. Pacman (PacmanQAgent)
# Approximate Q-Learning Agent (ApproximateQAgent)
#------------------------------------------------------------------------------------------------#

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

#------------------------------------------------------------------------------------------------#
# Q-Learning Agent for gridworld
class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent
      Parent instance variables
        - self.epsilon (exploration probability)
        - self.alpha (learning rate)
        - self.discount (discount rate = gamma)
    """
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)

        # init Q-Values = current estimates for each Q(state,action)
        self.qValues = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        # default - returning 0.0
        return self.qValues[(state,action)]

    # ------------------------------------------------------------------------------------------------#
    # best action of Q(state,action)
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
          Compute the best action to take in a state.
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
          take the best policy action otherwise.
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
          The parent class calls this to observe a (state,action,nextState) and reward transition...
          Q-Value update:
          used here: Q(state,action) = Q(state,action) + alpha(reward+ discount * bestAction' Q(s',a') - Q(s,a))
          ==
          alternative:Q(state,action) =  (1-alpha) Q(state,action) + alpha(reward + discount * bestAction' Q(state',action')).
        """
        self.qValues[(state,action)] = self.getQValue(state,action) + self.alpha * ((reward +
        self.discount * self.getValue(nextState)) - self.qValues[(state,action)])

#------------------------------------------------------------------------------------------------#
# Q-Learning Agent for Ms. Pacman
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
        informs parent of action for Pacman.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action

#------------------------------------------------------------------------------------------------#
# Aproximate Q-Learning Agent for Ms. Pacman
class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent
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
        qvalue = 0.0
        # features
        features = self.featExtractor.getFeatures(state, action)
        for i in features: # concrete feature fi in features
            qvalue += self.getWeights()[i] * features[i]
        return qvalue

    def update(self, state, action, nextState, reward):
        """
           Updating features weights based on on transition
        """
        difference = (reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action)
        # features
        features = self.featExtractor.getFeatures(state, action)
        for i in features:
            self.getWeights()[i] += self.alpha * difference * features[i]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # print weights for debugging
            #print self.getWeights()
            pass
