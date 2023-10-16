from direction import Direction
from direction import ComplexDirection
from random import randint
from random import choices
import math
from typing import Dict
import numpy as np

class StateAction:
    def __init__(self, state, action):
        self.state = state
        self.action = action

    def __str__(self):
        s = ""
        s += str(self.state) + "\n"
        s += str(self.action) + "\n"
        return s

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
        
            

        
class State:
    def __init__(self, sheep_direction: ComplexDirection, facing_queue):
        self.sheep_direction = sheep_direction
        self.facing_queue = facing_queue


    def as_attack(self):
        return State(self.sheep_direction, set())
    
    def as_defense(self):
        return State(ComplexDirection.LEFT, self.facing_queue)
    
    def __eq__(self, other):
        return self.sheep_direction == other.sheep_direction and self.facing_queue == other.facing_queue
    
    def __hash__(self):
        return hash((self.sheep_direction, tuple(self.facing_queue)))
        
    def __str__(self):
        str_facing_queue = ""
        for direction in self.facing_queue:
            str_facing_queue += str(direction) + " "
        s = ""
        s += "Sheep on: " + str(self.sheep_direction) + "\n"
        s += "Facing queue: " + str_facing_queue + "\n"
        return s
    
        
class Policy:
    def __init__(self):
        self.policy: Dict[State, Direction] = {}
        self.exploration = 0.3
        self.improvements = 0
        
    def get_action(self, state: State, current_direction: Direction):
        available = current_direction.get_available()
        if (not state in self.policy):
            return choices(available)[0]
        weights = [self.exploration / 2, self.exploration / 2, self.exploration / 2]
        try:
            weights[available.index(self.policy[state])] = 1 - self.exploration
            return choices(available, weights=weights)[0]
        except:
            return choices(available)[0]
        
    
        
    
    def improve(self, rewards):
        for state in rewards.keys():
            isUniformDistribution = True

            actions = list(rewards[state].keys())

            best_reward = rewards[state][actions[0]]["reward"]
            best_action = actions[0]

            for i in range(1, len(actions)):
                average_reward = rewards[state][actions[i]]["reward"]
                if (average_reward > best_reward):
                    best_reward = average_reward
                    best_action = actions[i]
                    isUniformDistribution = False
                elif (average_reward < best_reward):
                    isUniformDistribution = False

            if (not isUniformDistribution):
                self.policy[state] = best_action
        if (self.exploration > 0):
            self.exploration -= 0.001
        if (self.exploration < 0):
            self.exploration = 0
        print(self.exploration)

    def __str__(self):
        s = "--------------------------\n"

        for state in self.policy.keys():
            s += str(state) + "\n"
            s += str(self.policy[state]) + "\n\n"

        s += "---------------------------\n"
            
        return s

            


    
        
        