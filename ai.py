import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier

def make_decision(board, previous_point, current_point):
    """
    Make a decision based on the board state and moves.
    :param board: 2D array representing the board.
    :param previous_point: Tuple (x, y) for the previous move.
    :param current_point: Tuple (x, y) for the current move.
    :param next_point: Tuple (x, y) for the possible next move.
    :return: One of 'T', 'S', or 'Z'
    """
    # Placeholder AI logic - replace with actual learning logic
    return random.choice(['T', 'S', 'Z'])