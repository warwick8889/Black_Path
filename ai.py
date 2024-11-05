import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import board

ACTIONS = ['T', 'S', 'Z']  #The possible moves

class AI:
    def __init__(self, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.99):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.q_table = {}  #Q-table for storing learned action values

    def get_state(self):
        board_state = board.get_board()
        return tuple(np.array(board_state).flatten())  #2D array into a tuple

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate: #Exploration: Choose a random action
            return random.choice(ACTIONS)
        else: #Exploitation: Choose the action with the highest Q-value for the current state
            return self.get_best_action(state)

    def get_best_action(self, state):
        if state not in self.q_table:
            return random.choice(ACTIONS)  #If state is new, return a random action
        return max(self.q_table[state], key=self.q_table[state].get)

    def update_q_value(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in ACTIONS}
        
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0 for a in ACTIONS}
        
        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state].values())

        #Q-learning formula
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q

    def take_step(self):
        #Get the current state of the board
        state = self.get_state()

        #Choose an action (T, S, or Z)
        action = self.choose_action(state)

        #Apply the action to the board
        board.apply_action(action)

        #Get the reward and the new state after the action
        reward = self.get_reward()  #TBA
        next_state = self.get_state()
        
        #Update the Q-value based on the reward
        self.update_q_value(state, action, reward, next_state)

        #Reduce exploration over time
        self.exploration_rate *= self.exploration_decay

    def get_reward(self):
        """
        Reward logic here
        """

