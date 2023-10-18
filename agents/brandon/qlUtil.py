from collections import defaultdict
from game import Directions
import game
import random
from game import Configuration

MAX_CAPACITY = 3
class QTable():
    def __init__(self, default=0.0):
        self.default = default
        self.qtable = defaultdict(float)  # Initialize with float, not lambda
        # Populate qtable with default values if necessary

    def update(self, state, action, delta):
        self.qtable[(state, action)] = self.get_q_value(state, action) + delta


    def get_q_value(self, state, action):
        print(f"Q value for : state {state} with actions {action} = {self.qtable.get((state, action), self.default)}.")
        return self.qtable.get((state, action), self.default)

    def get_max_q(self, state, actions):
        max_q_value = float(0)
        best_action = None

        for action in actions:
            q_value = self.get_q_value(state, action)
            if q_value > max_q_value:
                max_q_value = q_value
                best_action = action

        return best_action, max_q_value

class ModelFreeReinforcementLearner:
    def __init__(self, mdp, bandit, qfunction, agent, alpha=0.1):
        self.mdp = mdp
        self.bandit = bandit
        self.alpha = alpha
        self.qfunction = qfunction
        self.agent = agent

    def execute(self, state, episodes=100):
        for i in range(episodes):
            actions = self.mdp.get_actions(state)
            action = self.bandit.select(state, actions, self.qfunction)
            while not self.mdp.is_terminal(state, self.agent):
                (next_state, reward) = self.mdp.execute(state, action)
                actions = self.mdp.get_actions(next_state)
                next_action = self.bandit.select(next_state, actions, self.qfunction)
                q_value = self.qfunction.get_q_value(state, action)

                delta = self.get_delta(reward, q_value, state, next_state, next_action)
                self.qfunction.update(state, action, delta)
                state = next_state
                action = next_action

    def get_delta(self, reward, q_value, state, next_state, next_action):
        next_state_value = self.state_value(next_state, next_action)
        delta = reward + self.mdp.discount_factor * next_state_value - q_value
        return self.alpha * delta

    def state_value(self, state, action):
        actions = self.mdp.get_actions(state)
        return max([self.qfunction.get_q_value(state, action) for action in actions])

class QLearning(ModelFreeReinforcementLearner):
    def state_value(self, state, action):
        # (_, max_q_value) = self.qfunction.get_max_q(state, self.mdp.get_actions(state))
        # return max_q_value
        actions = self.mdp.get_actions(state)
        return max([self.qfunction.get_q_value(state, action) for action in actions])

class MDP:
    def __init__(self, gameState, agent, agentIndex):
        # Initialization similar to PositionSearchProblem
        self.gameState = gameState
        self.walls = gameState.getWalls()
        x, y = gameState.getAgentState(agentIndex).getPosition()
        self.startState = int(x), int(y)
        self.agent = agent
        self.discount_factor = 0.9


    def getStartState(self):
        return self.startState

    def get_actions(self, state):
        return state.getLegalActions(1)

    def is_terminal(self, state, agent):
        notPacman = not state.getAgentState(agent.index).isPacman
        if len(agent.getFood(state).asList()) <= 2 and notPacman:
            return True

    def execute(self, state, action):
        x, y = state.getAgentState(1).getPosition()
        dx, dy = game.Actions.directionToVector(action)
        nextx, nexty = int(x + dx), int(y + dy)
        next_state = (nextx, nexty)
        reward = self.calculate_reward(next_state, state)
        if not self.walls[nextx][nexty]:
            return next_state, reward
        return state, reward

    def calculate_reward(self, next_state, gameState):
        STEP_REWARD = -1
        FOOD_REWARD = 0
        WALL_REWARD = -999999
        # GHOST_REWARD = -100


        x, y = next_state
        foodgrid = self.agent.getFood(gameState)

        if foodgrid[x][y]:
            return FOOD_REWARD

        if self.walls[x][y]:
            return WALL_REWARD

        # ghosts = []
        #
        # for i in self.agent.getOpponents(self.gameState):
        #     opponentState = self.gameState.getAgentState(i)
        #     ghostForm = not opponentState.isPacman
        #     if ghostForm:
        #         ghosts.append(opponentState)
        #
        # ghost_positions = [ghost.getPosition() for ghost in ghosts if ghost.getPosition() is not None
        #                    and ghost.scaredTimer == 0]
        #
        # if next_state in ghost_positions:
        #     return GHOST_REWARD

        return STEP_REWARD

class EpsilonGreedy():
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon

    def reset(self):
        pass

    def select(self, state, actions, qfunction):
        # Select a random action with epsilon probability
        if random.random() < self.epsilon:
            return random.choice(actions)
        (arg_max_q, _) = qfunction.get_max_q(state, actions)
        # if arg_max_q is None:
        #     print(f"Warning: arg_max_q is None for state {state} with actions {actions}.")
        if arg_max_q is None:
            return random.choice(actions)

        return arg_max_q