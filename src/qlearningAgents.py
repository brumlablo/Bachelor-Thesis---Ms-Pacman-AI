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
# BP: implemented:
# Q-Learning agents for
    # gridworld (QLearningAgent)
    # Ms. Pacman (PacmanQAgent)
# Approximate Q-Learning Agent (ApproximateQAgent)

# AGENTS MANUAL USAGE EXAMPLES
# QLearningAgent (used with gridworld.py, basic usage examples - see valueiterationsAgents.py)
#
# 5 episodes of training, manually
# python gridworld.py -a q -k 5 -m
#
# 20 episodes of training on DiscountGrid, alpha=0.8, epsilon-greedy=0.5
# python gridworld.py -a q -k 20 -g DiscountGrid --learningRate 0.8 --epsilon 0.5

# MS. PACMAN DEMO - pacman,py basic usage:
# basic usage examples:
# more in help: python pacman.py -h
# basic arguments examples:
    # no animation: --frameTime 0
    # quiet = no GUI (only stdout output): -q
    # -n  or --numGames NumberOfGames
    # -x  or --numTraining NumberOfTrainingEpisodes
    # fixed randomSeed: -f
    # ! alpha, gamma, epsilon set for each agent
# PacmanQAgent (Ms. Pacman Q-Learning agent, used with pacman.py)
#
# 2000 episodes of training, 10 episodes of performing optimal (no epsilon-greedy, from training), smallGrid layout
# python pacman.py -p PacmanQAgent -x 2000 -n 2010 -l smallGrid
#
# only 10 episodes of training on smallGrid
# python pacman.py -p PacmanQAgent -n 10 -l smallGrid -a numTraining=10
#
# ApproximateQAgent (Ms. Pacman Approximate Q-Learning agent, used with pacman.py)
#
# 2000 episodes of training, 10 episodes of performing optimal (no epsilon-greedy, from training), smallGrid layout
# python pacman.py -p ApproximateQAgent -x 2000 -n 2010 -l smallGrid
#
# 60 games from which 50 episodes of training
# python pacman.py -p ApproximateQAgent -a extractor=BetterExtractor ---numGames 60 --numTraining 50 -l mediumGrid
#
# python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic
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
      NOTE:
      parent instance variables:
        epsilon (exploration probability)
        alpha (learning rate)
        discount (discount rate = gamma)
    """
    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)

        # init Q-Values = current estimates for each Q(state,action)
        self.qValues = util.Counter()

    def getQValue(self, state, action):
        #  returns Q(state,action); default = 0.0 for unseen state/Q-value
        return self.qValues[(state,action)]

    # ------------------------------------------------------------------------------------------------#
    # return best action of Q(state,action) from state legal actions
    def getValue(self, state):
        return self.computeValueFromQValues(state)

    def computeValueFromQValues(self, state):
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

    # ------------------------------------------------------------------------------------------------#
    # EXECUTING POLICIES = STRATEGIES: return MAX action for state
    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    # compute the best action to take in a state
    def computeActionFromQValues(self, state):

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

    # ------------------------------------------------------------------------------------------------#
    # TRAINING: return action for state chosen based on epsilon-greedy (random or best possible)
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

    # update Q-values - called by parent to observe new transition (state,action,nextState) and its reward
    def update(self, state, action, nextState, reward):
        """
          Q-Value update:
          used here: Q(state,action) = Q(state,action) + alpha(reward+ discount * bestAction' Q(s',a') - Q(s,a))
          ==
          alternative:Q(state,action) =  (1-alpha) Q(state,action) + alpha(reward + discount * bestAction' Q(state',action')).
        """
        self.qValues[(state,action)] = self.getQValue(state,action) + self.alpha * ((reward +
        self.discount * self.getValue(nextState)) - self.qValues[(state,action)])

#------------------------------------------------------------------------------------------------#
# Q-Learning Agent for Ms. Pacman ( == QLearningAgent, different default parameters)
class PacmanQAgent(QLearningAgent):

    def __init__(self, alpha=0.2, epsilon=0.05, gamma=0.8, numTraining=0, **args):
        """
        NOTE:
        defualt params can be changed from the pacman.py CLI e.g.:
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

    # calls the getAction method of QLearningAgent and informs parent of action for Pacman
    def getAction(self, state):
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action

#------------------------------------------------------------------------------------------------#
# Aproximate Q-Learning Agent for Ms. Pacman
class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent
    """

    # init featureExtractor, weights and agent
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    # return Q(state,action) = w * featureVector
    def getQValue(self, state, action):

        qvalue = 0.0
        # features
        features = self.featExtractor.getFeatures(state, action)
        for i in features: # concrete feature f_i in features
            qvalue += self.getWeights()[i] * features[i]
        return qvalue

    # weights update based on transition
    def update(self, state, action, nextState, reward):

        difference = (reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action)
        # features
        features = self.featExtractor.getFeatures(state, action)
        for i in features:
            self.getWeights()[i] += self.alpha * difference * features[i]

    # final print
    def final(self, state):
        # call the super-class final method at the end of each game
        PacmanQAgent.final(self, state)

        # is training finished ?
        if self.episodesSoFar == self.numTraining:
            # print weights for debugging
            print self.getWeights()
            pass
