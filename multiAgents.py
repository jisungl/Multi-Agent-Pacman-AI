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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        "***You can change what this function returns***"
        score = successorGameState.getScore()
        foods = newFood.asList()
        score += 1.0 / (min(manhattanDistance(newPos, food) for food in foods) + 1) if foods else 0
        
        return score

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
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        currScore = float('-inf')
        next = None # ?
        for action in gameState.getLegalActions(0):
            score = self.minimax(gameState.generateSuccessor(0, action), 1, 0)
            if score > currScore:
                currScore = score
                next = action
        return next
    
    def minimax(self, state, agent, depth):
        if depth == self.depth or state.isWin() or state.isLose(): # ?
            return self.evaluationFunction(state)
        
        allActions = state.getLegalActions(agent)
        if not allActions:
            return self.evaluationFunction(state)
        
        nextAgent = (agent + 1) % state.getNumAgents()
        newDepth = depth + 1 if nextAgent == 0 else depth
        
        if agent == 0:
            return max(self.minimax(state.generateSuccessor(agent, action), nextAgent, newDepth) for action in allActions)
        else :
            return min(self.minimax(state.generateSuccessor(agent, action), nextAgent, newDepth) for action in allActions)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a = float('-inf')
        b = float('inf')
        curr = float('-inf')
        next = None

        for action in gameState.getLegalActions(0):
            hold = self.alphabeta(gameState.generateSuccessor(0, action), 1, 0, a, b)
            if hold > curr:
                curr = hold
                next = action
            a = max(a, curr)

        return next
    
    def alphabeta(self, state, agent, depth, a, b):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)      
        allActions = state.getLegalActions(agent)
        if not allActions:
            return self.evaluationFunction(state)

        nextAgent = (agent + 1) % state.getNumAgents()
        newDepth = depth + 1 if nextAgent == 0 else depth

        if agent == 0:
            hold = float('-inf')
            for action in allActions:
                hold = max(hold, self.alphabeta(state.generateSuccessor(agent, action), nextAgent, newDepth, a, b))
                if hold > b:
                    return hold
                a = max(a, hold) # ?
            return hold
        else:
            hold = float('inf')
            for action in allActions:
                hold = min(hold, self.alphabeta(state.generateSuccessor(agent, action), nextAgent, newDepth, a, b))
                if hold < a:
                    return hold
                b = min(b, hold) # ?
            return hold

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
        curr = float('-inf')
        next = None
        for action in gameState.getLegalActions(0):
            hold = self.expectimax(gameState.generateSuccessor(0, action), 1, 0)
            if hold > curr:
                curr = hold
                next = action
        return next

    def expectimax(self, state, agent, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        allActions = state.getLegalActions(agent)
        if not allActions:
            return self.evaluationFunction(state)

        nextAgent = (agent + 1) % state.getNumAgents()
        newDepth = depth + 1 if nextAgent == 0 else depth

        if agent == 0:
            return max(self.expectimax(state.generateSuccessor(agent, action), nextAgent, newDepth) for action in allActions) # ?
        else:
            total = 0
            for action in allActions:
                total += self.expectimax(state.generateSuccessor(agent, action), nextAgent, newDepth) # ?
            return total / len(allActions)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: gives rewards when pacman is closer to food, gives penalties
    for states with more capsules untouched.
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    pac = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()

    closest = float('inf')
    for food in foods:
        dist = util.manhattanDistance(pac, food)
        if dist < closest:
            closest = dist
    if closest == float('inf'):
        closest = 1
    score += 1.0 / closest
    score -= len(currentGameState.getCapsules()) # ?

    return score

# Abbreviation
better = betterEvaluationFunction
