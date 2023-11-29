from env.player import Player
from env.ball import Ball

import env
import os
import time

os.environ['RSS_FIELD_SIZE'] = 'M' # [XS, S, M, R]
os.environ['RSS_N_MAX_PLAYERS'] = '3'
num_players_team_A = 3
num_players_team_B = 3

size = os.environ['RSS_FIELD_SIZE']
n_max_players = int(os.environ['RSS_N_MAX_PLAYERS'])

env = env.make(size = size, num_players_team_A = num_players_team_A, num_players_team_B = num_players_team_B, render = True)

team_a = [Player('A', 'A_{i}'.format(i = i), env) for i in range(n_max_players)]
team_a_active_players = [player for player in team_a[:num_players_team_A]]
team_b = [Player('B', 'B_{i}'.format(i = i), env) for i in range(n_max_players)]
team_b_active_players = [player for player in team_b[:num_players_team_B]]
ball = Ball(env.model)

env.set_game_elements(team_a, team_b, ball)
[team_a[i].set_ai('ddpg') for i in range(num_players_team_A)]
[team_b[i].set_ai('ddpg') for i in range(num_players_team_B)]
players = team_a + team_b

max_episodes = 10000
for i in range(max_episodes):
	episode_start_time = time.time()
	observations = env.reset_game(randomize = True)
	while True:
		actions = [player.ai.choose_action(observations[i]) for i, player in enumerate(players)]
		new_observations, rewards, dones, infos = env.step(players_actions = zip(players, actions))
		[player.ai.remember([observations[i], actions[i], rewards[i], new_observations[i], dones[i]]) for i, player in enumerate(players)]
		observations = new_observations

		[player.ai.learn() for player in players]

		if any(dones) or (time.time() - episode_start_time > 135):
			break

	if i % 10 == 0:
		[player.ai.save_models() for player in team_a_active_players]
	
	



