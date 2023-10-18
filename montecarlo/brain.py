from .policy import Policy
from .state import StateAction
from .game.direction import Direction

class Brain:
    def __init__(self, gamma):
        self.current_policy = Policy()
        self.values = {}
        self.rewards = {}
        self.history = []
        self.gamma = gamma

    def choose_direction(self, state, current_direction) -> Direction:
        direction = self.current_policy.get_action(state, current_direction)
        self.history.append([StateAction(state, direction), 0])
        return direction
    
    def choose_weights(self, state, available):
       return self.current_policy.get_weights(state, available)


    def add_history(self, state_action):
        self.history.append([state_action, 0])
    
    def add_reward(self, reward):
        self.history[-1][1] = reward
        

    def evaluate(self):
        for i in range(0, len(self.history)):
            reward = 0
            counter = 0
            for j in range(i, len(self.history)):
                reward += self.history[j][1] * (self.gamma ** counter)
                counter += 1

            state_action = self.history[i][0]
            
            if (not state_action.state in self.rewards.keys()):
                self.rewards[state_action.state] = {}
            if (not state_action.action in self.rewards[state_action.state].keys()):
                self.rewards[state_action.state][state_action.action] = {}
                self.rewards[state_action.state][state_action.action]["reward"] = 0
                self.rewards[state_action.state][state_action.action]["count"] = 0

            old_reward = self.rewards[state_action.state][state_action.action]["reward"]

            count = self.rewards[state_action.state][state_action.action]["count"] + 1

            self.rewards[state_action.state][state_action.action]["count"] = count

            self.rewards[state_action.state][state_action.action]["reward"] = old_reward + (reward - old_reward) / count

        self.history = []
        self.current_policy.improve(self.rewards)