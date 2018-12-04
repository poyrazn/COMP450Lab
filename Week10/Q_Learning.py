
"""
COMP450 Artificial Intelligence Week-10 Fall 2018-19
A simple example for Reinforcement Learning using table lookup Q-learning method.
An agent "o" is on the left of a 1 dimensional world, the target is on the rightmost location.

TASK-1A: Please explain how this algorithm work to make the agent reach its target.
TASK-1B: Please give the necessary comments for the following piece of code.
"""

import numpy as np
import pandas as pd
import time

N_STATES = 6  # Number of states
ACTIONS = ['left', 'right']  # Possible actions
EPSILON = 0.9  # Ensures randomization
ALPHA = 0.1  # Learning Rate
GAMMA = 0.9  # Discount Factor
MAX_EPISODES = 100  # Maximum episodes allowed
FRESH_TIME = 0.0  # .........................


def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),  # q_table initial values
        columns=actions,  # actions's name
    )
    print(table)  # show table
    return table


def choose_action(state, q_table):
    # choose action from the q_table considering the state the agent is in
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or (state_actions.all() == 0):  # act non-greedy or state-action have no value
        action_name = np.random.choice(ACTIONS)
    else:  # act greedy
        action_name = state_actions.idxmax()
    return action_name


def get_env_feedback(S, A):
    # get the next state (S_) and the reward (R) upon the executing the action on the state S
    if A == 'right':  # Check if the action is right
        if S == N_STATES - 2:  # Check if the state is the
            S_ = 'terminal'
            R = 1
        else:
            S_ = S + 1
            R = 0
    else:  # Action is left
        R = 0
        if S == 0:
            S_ = S  # Stay in the same state
        else:
            S_ = S - 1
    return S_, R


def update_env(S, episode, step_counter):
    # This is how environment be updated
    env_list = ['-'] * (N_STATES - 1) + ['T']  # '---------T' our environment
    if S == 'terminal':
        interaction = 'Episode %s: total_steps = %s' % (episode + 1, step_counter)
        print('\r{}'.format(interaction))
        time.sleep(2)
        print('\r                                ')
    else:
        env_list[S] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction))
        time.sleep(FRESH_TIME)


def rl():
    # Reinforcement Learning (Q-Learning) simulation
    q_table = build_q_table(N_STATES, ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 0
        is_terminated = False
        update_env(S, episode, step_counter)
        while not is_terminated:

            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A)  # Returns next state and the expected reward upon executing the action
            q_predict = q_table.loc[S, A]
            if S_ != 'terminal':
                q_target = R + GAMMA * q_table.iloc[S_, :].max()  # Calculate the Reward using the discount factor
            else:
                q_target = R  # Reward is Reward
                is_terminated = True  # Terminated

            q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # Update Q-Table
            S = S_  # Next state

            update_env(S, episode, step_counter + 1)
            step_counter += 1
        print(q_table)
    return q_table

if __name__ == "__main__":
    q_table = rl()
    print('\r\nQ-table:\n')
    print(q_table)
