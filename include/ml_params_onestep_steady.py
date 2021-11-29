import numpy as np
# One-step environment Q-learning parameters

# Action related constants
ACTION_STEP = 0.025 # (Logarithm step for Damkohler number)
CONTROL_STEP = 1 # (Take action for every step)
NUM_ACTIONS = 3 # (increase, stay or decrease by mass flow rate step)

# Bounds for temperature buckets
# Note these can be unequal
STATE_BOUNDS = np.array([300.,700.,750.,1200.,1300.])
NUM_BUCKETS = STATE_BOUNDS.size - 1

## Learning related constants
MIN_EXPLORE_RATE = 0.01
MIN_LEARNING_RATE = 0.2

## Reward constants
CORRECT_REWARD = 1
REDUCED_REWARD = 0.8
WRONG_REWARD = 0

# Defining the simulation related constants
NUM_EPISODES = 2000
DEBUG_MODE = True

# Render episode from the episode number
RENDER_FROM = 200
