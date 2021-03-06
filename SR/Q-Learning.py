from gridworld import GridworldEnv
import gym
import numpy as np
from collections import defaultdict
import plotting
import gym_minigrid

#env_id = 'MiniGrid-Empty-6x6-v0'

env = GridworldEnv()
#env = gym.make(env_id)

EPSILON = 0.3
GAMMA = 0.99
LEARNING_RATE = 0.3
NUM_EPISODES = 500

# initialize Q
Q = defaultdict(lambda: np.zeros(env.action_space.n))

stats = plotting.EpisodeStats(
        episode_lengths=np.zeros(NUM_EPISODES),
        episode_rewards=np.zeros(NUM_EPISODES))

def convert(state):

    ct = 0
    for i in range(4):
        for j in range(4):

            if state == (i+1,j+1):
                print(True)
                obs = ct
            ct += 1

    return obs

for i in range(NUM_EPISODES):

    state = env.reset()
    #state = convert(env.agentPos)
    steps = 0

    while True:

        if np.random.sample() < EPSILON:
            action = np.random.choice(env.action_space.n)
        else:
            action = np.argmax(Q[state])

        next_state, reward, done, _ = env.step(action)

        #next_state = convert(env.agentPos)
        #if done and reward > 0:
        #    next_state = 15
        #env.render()

        stats.episode_rewards[i] += reward
        stats.episode_lengths[i] = steps

        Q_target = reward + GAMMA * Q[next_state][np.argmax(Q[next_state])]
        Q_error = Q_target - Q[state][action]

        Q[state][action] += LEARNING_RATE * Q_error
        state = next_state
        steps += 1

        EPSILON -= 0.00005

        if done:
            break


plotting.plot_episode_stats(stats)
