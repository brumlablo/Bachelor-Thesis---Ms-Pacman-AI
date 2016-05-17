# learningAgents.py
# -----------------
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


from game import Directions, Agent, Actions

import random,util,time

#------------------------------------------------------------------------------------------------#
# BP: slightly edited and commented...
#------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------#
# abstract class for agents: ValueIterationAgent, ReinforcementAgent (and QLearningAgent,...)
# inherits from Agent in game.py
class ValueEstimationAgent(Agent):
    """
      Abstract agent which assigns values to (state,action)
      Q-Values for an environment. As well as a value to a
      state and a policy given respectively by,

      V(s) = max_{a in actions} Q(s,a)
      policy(s) = arg_max_{a in actions} Q(s,a)

      parent of:
        ValueIterationAgent - needs model of the environment from MarkovDecisionProcess (mdp.py),
                              used to estimate Q-Values before acting
        QLearningAgent      - estimates Q-Values while acting in the environment
    """

    def __init__(self, alpha=1.0, epsilon=0.05, gamma=0.8, numTraining = 10):
        """
        Sets options, which can be passed in via the Pacman command line using -a alpha=0.5,...
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes >> no learning after these many episodes
        """
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.discount = float(gamma)
        self.numTraining = int(numTraining)

    ####################################
    #  these functions are overriden   #
    ####################################
    def getQValue(self, state, action):
        """
        returns Q(state,action)
        """
        util.raiseNotDefined()

    def getValue(self, state):
        """
        returns value of this state under the best action
        Value(state) = max_{action in legal actions} Q(state,action)
        """
        util.raiseNotDefined()

    def getPolicy(self, state):
        """
        returns the best action to take in the state
        (or random action based on epsilon-greedy)

        policy(state) = arg_max_{action in legal actions} Q(state,action)
        """
        util.raiseNotDefined()

    def getAction(self, state):
        """
        return chosen action
        """
        util.raiseNotDefined()

class ReinforcementAgent(ValueEstimationAgent):
    """
      Abstract Reinforcement Agent: A ValueEstimationAgent
      which estimates Q-Values (as well as policies) from experience (no model).

      The environment will call
      observeTransition(state,action,nextState,deltaReward),
      which will call update(state, action, nextState, deltaReward) - to be overriden
    """
    ####################################
    #  these functions are overriden   #
    ####################################

    def update(self, state, action, nextState, reward):
        """
        called after observing a transition and reward
        """
        util.raiseNotDefined()

    ####################################
    #    other functions               #
    ####################################

    def getLegalActions(self,state):
        """
          actions available for a given state
        """
        return self.actionFn(state)

    # new transition
    def observeTransition(self, state,action,nextState,deltaReward):
        """
        Called by environment to inform agent that a transition has
        been observed. This will result in a call to self.update
        on the same arguments
        """
        self.episodeRewards += deltaReward
        self.update(state,action,nextState,deltaReward)

    def startEpisode(self):
        """
          Called by environment when new episode is starting
        """
        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0

    def stopEpisode(self):
        """
          Called by environment when episode is done
        """
        if self.episodesSoFar < self.numTraining:
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards
        self.episodesSoFar += 1
        if self.episodesSoFar >= self.numTraining:
            # stop training
            self.epsilon = 0.0    # no exploration
            self.alpha = 0.0      # no learning

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return not self.isInTraining()

    def __init__(self, actionFn = None, alpha=0.5, epsilon=0.5, gamma=1, numTraining=100):
        """
        actionFn: Function which takes a state and returns the list of legal actions

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        if actionFn == None:
            actionFn = lambda state: state.getLegalActions()
        self.actionFn = actionFn
        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setLearningRate(self, alpha):
        self.alpha = alpha

    def setDiscount(self, discount):
        self.discount = discount

    def doAction(self,state,action):
        """
        Called by inherited class when
        an action is taken in a state
        """
        self.lastState = state
        self.lastAction = action

    #######################
    # Ms. Pacman Specific #
    #######################

    # connecting agent's behaviour with Ms. Pacman Game
    def observationFunction(self, state):
        """
        Successor state after last action. Called by environment...
        """
        if not self.lastState is None:
            reward = state.getScore() - self.lastState.getScore()
            self.observeTransition(self.lastState, self.lastAction, state, reward) # start update of Q-values
        return state

    def registerInitialState(self, state):
        self.startEpisode()
        if self.episodesSoFar == 0:
            print 'Beginning %d episodes of Training' % (self.numTraining)

    def final(self, state):
        """
          called by Ms. Pacman game at the terminal state
        """
        deltaReward = state.getScore() - self.lastState.getScore()
        self.observeTransition(self.lastState, self.lastAction, state, deltaReward)
        self.stopEpisode()

        # mandatory variables for output
        if not 'episodeStartTime' in self.__dict__:
            self.episodeStartTime = time.time()
        if not 'lastWindowAccumRewards' in self.__dict__:
            self.lastWindowAccumRewards = 0.0
        self.lastWindowAccumRewards += state.getScore()

        NUM_EPS_UPDATE = 100
        if self.episodesSoFar % NUM_EPS_UPDATE == 0:
            print 'Reinforcement Learning Status:'
            windowAvg = self.lastWindowAccumRewards / float(NUM_EPS_UPDATE)
            if self.episodesSoFar <= self.numTraining:
                trainAvg = self.accumTrainRewards / float(self.episodesSoFar)
                print '\tCompleted %d out of %d training episodes' % (
                       self.episodesSoFar,self.numTraining)
                print '\tAverage Rewards over all training: %.2f' % (
                        trainAvg)
            else:
                testAvg = float(self.accumTestRewards) / (self.episodesSoFar - self.numTraining)
                print '\tCompleted %d test episodes' % (self.episodesSoFar - self.numTraining)
                print '\tAverage Rewards over testing: %.2f' % testAvg
            print '\tAverage Rewards for last %d episodes: %.2f'  % (
                    NUM_EPS_UPDATE,windowAvg)
            print '\tEpisode took %.2f seconds' % (time.time() - self.episodeStartTime)
            self.lastWindowAccumRewards = 0.0
            self.episodeStartTime = time.time()

        if self.episodesSoFar == self.numTraining:
            msg = 'Training Done (turning off epsilon and alpha)'
            print '%s\n%s' % (msg,'-' * len(msg))
