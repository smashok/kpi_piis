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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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

        FAR_GHOST = 200
        NEAR_GHOST = 50

        score = successorGameState.getScore()

        #Ghost
        for ghost in newGhostStates:
          if ghost.scaredTimer <= 0:
            if util.manhattanDistance(newPos,successorGameState.getGhostPosition(newGhostStates.index(ghost) + 1)) == 1:
              score -= FAR_GHOST
            if util.manhattanDistance(newPos,successorGameState.getGhostPosition(newGhostStates.index(ghost) + 1)) == 2:
              score -= NEAR_GHOST
          else:
            score = score + 150

        def foodMinDist(point):
          min_distance, related_point = 100000, None
          for i in range(len(list(newFood))):
            for j in range(len(newFood[0])):
              if newFood[i][j] and manhattanDistance((i, j), point) < min_distance:
                  min_distance = manhattanDistance((i, j), point)
                  related_point = (i, j)
          return min_distance, related_point

        #Food
        if successorGameState.getNumFood() == 0 or currentGameState.getFood()[newPos[0]][newPos[1]]:
           return score
        min_distance, cloest_point = foodMinDist(newPos)
        if successorGameState.getNumFood() == 1:
          return score - min_distance
        else:
          distance, point = foodMinDist(cloest_point)
          return score - min_distance - distance

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        def cal_value(state, numsOfagent, depth, f, score):
            legal_moves = state.getLegalActions(numsOfagent)
            for action in legal_moves:
                next_state = state.generateSuccessor(numsOfagent, action)
                score = f(score, get_value(next_state, numsOfagent + 1, depth - 1))
            return score

        def get_value(state, numsOfagent, depth):
            numsOfagent = numsOfagent % state.getNumAgents()
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            elif numsOfagent == 0:
                return cal_value(state, numsOfagent, depth, max, -1000000)
            else:
                return cal_value(state, numsOfagent, depth, min, 1000000)

        scores = [get_value(gameState.generateSuccessor(0, action), 1, self.depth * gameState.getNumAgents() - 1) for
                  action in gameState.getLegalActions(0)]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        index = random.choice(best_indices)
        return gameState.getLegalActions(0)[index]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def cal_value(state, agent_num, depth, alpha, beta, f, score):
            legal_moves = state.getLegalActions(agent_num)
            for move in legal_moves:
                next_state = state.generateSuccessor(agent_num, move)
                score = f(score, get_value(next_state, agent_num + 1, depth - 1, alpha, beta))
                if f is max:
                    if score > beta:
                        return score
                    alpha = f(alpha, score)
                elif f is min:
                    if score < alpha:
                        return score
                    beta = min(beta, score)
            return score

        def get_value(state, agent_num, depth, alpha, beta):
            agent_num = agent_num % state.getNumAgents()
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            elif agent_num == 0:
                return cal_value(state, agent_num, depth, alpha, beta, max, -1000000)
            else:
                return cal_value(state, agent_num, depth, alpha, beta, min, 1000000)

        legal_moves = gameState.getLegalActions(0)
        alpha, beta = -100000, 100000
        best_move = None
        for move in legal_moves:
            score = get_value(gameState.generateSuccessor(0, move), 1, self.depth * gameState.getNumAgents() - 1, alpha,
                              beta)
            if score > alpha:
                alpha = score
                best_move = move
        return best_move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def cal_value(state, agent_num, depth, f, score):
            legal_moves = state.getLegalActions(agent_num)
            prob = 1.0 / float(len(legal_moves))
            for action in legal_moves:
                next_state = state.generateSuccessor(agent_num, action)
                if f is max:
                    score = max(score, get_value(next_state, agent_num + 1, depth - 1))
                elif f is min:
                    score = score + prob * get_value(next_state, agent_num + 1, depth - 1)
            return score

        def get_value(state, agent_num, depth):
            agent_num = agent_num % state.getNumAgents()
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            elif agent_num == 0:
                return cal_value(state, agent_num, depth, max, -1000000)
            else:
                return cal_value(state, agent_num, depth, min, 0)

        legal_moves = gameState.getLegalActions(0)
        scores = [get_value(gameState.generateSuccessor(0, action), 1, self.depth * gameState.getNumAgents() - 1) for
                  action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        index = random.choice(best_indices)
        return legal_moves[index]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
