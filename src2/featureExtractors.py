# featureExtractors.py
# --------------------
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


"Feature extractors for Pacman game states"

#------------------------------------------------------------------------------------------------#
# BP: implemented BetterExtractor for ApproximateQAgent

from game import Directions, Actions
import util
from util import *

class FeatureExtractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()

class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[(state,action)] = 1.0
        return feats

class CoordinateExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[state] = 1.0
        feats['x=%d' % state[0]] = 1.0
        feats['y=%d' % state[0]] = 1.0
        feats['action=%s' % action] = 1.0
        return feats

def closestFood(pos, food, walls):
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        if food[pos_x][pos_y]:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no food found
    return None

# Simple feature extractor
class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist) / (walls.width * walls.height)
        features.divideAll(10.0)
        return features

# Improved feature extractor for Ms. Pacman
class BetterExtractor(FeatureExtractor):
    """
    - if food will be eaten (in next state)
    - if capsule will be eaten and there is an active ghost
    - distance of next closest food
    - if a ghost collision is imminent
    - if a SCARED ghost is one step away
    - if an ACTIVE ghost is one step away
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        numGhosts = state.getNumAgents() - 1
        powerups = state.getCapsules()

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        for i in range(0,numGhosts):
            gPos = state.getGhostPosition(i+1%(numGhosts+1))
            g = state.getGhostState(i+1%(numGhosts+1))
            # ghostD = manhattanDistance(gPos,(next_x, next_y))
            if (next_x, next_y) in Actions.getLegalNeighbors(gPos, walls):
                if g.scaredTimer < 1: # count the number of active ghosts 1-step away
                    features["active-ghosts-1-step-away"] += 1
                else: # count the number of scared ghosts 1-step away
                    features["scared-ghosts-1-step-away"] += 1

        # if there is no danger of ghosts then add the food feature
        if not features["active-ghosts-1-step-away"] and not features["scared-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        foodD = closestFood((next_x, next_y), food, walls)

        # if there is powerup and active ghost
        if((next_x, next_y) in powerups and not features["active-ghosts-1-step-away"]):
            features["powerup"] = 1.0

        if foodD is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(foodD) / (walls.width * walls.height)

        features.divideAll(10.0) # to prevent divergetion
        return features

