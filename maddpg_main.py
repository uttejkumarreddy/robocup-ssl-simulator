import numpy as np
import env
import time
import os

from ai.maddpg.maddpg import MADDPG
from ai.maddpg.replay_buffer import MultiAgentReplayBuffer
from env.player import Player
from env.ball import Ball

def obs_list_to_state_vector(observation):
	state = np.array([])
	for obs in observation:
		state = np.concatenate([state, obs])
	return state

if __name__ == '__main__':
	scenario = '3v3'

	size = 'R' # [XS, S, M, R]
	num_players_team_A = 3
	num_players_team_B = 3

	os.environ['RSS_FIELD_SIZE'] = 'R'
	os.environ['RSS_N_MAX_PLAYERS'] = '3'

	env = env.make(size = size, num_players_team_A = num_players_team_A, num_players_team_B = num_players_team_B, render = True)
	team_a = [Player('A', 'A_{i}'.format(i = i), env) for i in range(num_players_team_A)]
	team_b = [Player('B', 'B_{i}'.format(i = i), env) for i in range(num_players_team_B)]
	ball = Ball(env.model)
	env.set_game_elements(team_a, team_b, ball)
	
	n_actions = env.action_space.shape[0]

	maddpg_actor_dims = [env.observation_space.shape[0] for i in range(num_players_team_A + num_players_team_B)]
	maddpg_critic_dims = sum(maddpg_actor_dims)

	maddpg_agents = MADDPG(
		maddpg_actor_dims,
		maddpg_critic_dims,
		num_players_team_A + num_players_team_B,
		n_actions,
		scenario = scenario
	)
	memory = MultiAgentReplayBuffer(1000000, maddpg_critic_dims, maddpg_actor_dims, n_actions, num_players_team_A + num_players_team_B, 1024)
	
	# Simulation
	maddpg_agents.load_checkpoints()

	N_GAMES = 50000
	MAX_TIME = 45 # seconds
	total_steps = 0
	best_score = 0
	score_history = []
	PRINT_EVERY = 100

	for i in range(N_GAMES):
		episode_start_time = time.time()

		score = 0
		episode_step = 0
		
		obs = env.reset_game() # observations: A_0, A_1, A_2, B_0, B_1, B_2
		done = [False] * (num_players_team_A + num_players_team_B)

		while not any(done):
			if env.render is True:
				env.render_sim()

			actions = maddpg_agents.choose_actions(obs)
			obs_, rewards, dones, info = env.step(players_actions=zip(team_a + team_b, actions))

			state = obs_list_to_state_vector(obs)
			state_ = obs_list_to_state_vector(obs_)

			time_elapsed = time.time() - episode_start_time
			if time_elapsed > MAX_TIME:
				done = [True] * (num_players_team_A + num_players_team_B)

			memory.store_transition(obs, state, actions, rewards, obs_, state_, dones)

			if total_steps % 100 == 0:
				maddpg_agents.learn(memory)

			obs = obs_

			score += sum(rewards)
			total_steps += 1

		score_history.append(score)
		avg_score = np.mean(score_history[-100:])
		if avg_score > best_score:
			maddpg_agents.save_checkpoints()
			best_score = avg_score

		if i % PRINT_EVERY == 0 and i > 0:
			print('episode', i, 'average score {:.1f}'.format(avg_score))