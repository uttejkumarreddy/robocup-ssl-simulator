from env.player import Player
from env.ball import Ball

import env
import os

os.environ['RSS_FIELD_SIZE'] = 'R' # [XS, S, M, R]
os.environ['RSS_N_MAX_PLAYERS'] = '6'
num_players_team_A = 3
num_players_team_B = 4

size = os.environ['RSS_FIELD_SIZE']
n_max_players = int(os.environ['RSS_N_MAX_PLAYERS'])

env = env.make(size = size, num_players_team_A = num_players_team_A, num_players_team_B = num_players_team_B, render = True)

team_a = [Player('A', 'A_{i}'.format(i = i), env) for i in range(n_max_players)]
team_b = [Player('B', 'B_{i}'.format(i = i), env) for i in range(n_max_players)]
ball = Ball(env.model)

env.set_game_elements(team_a, team_b, ball)
[team_a[i].set_ai('ddpg') for i in range(num_players_team_A)]
[team_b[i].set_ai('ddpg') for i in range(num_players_team_B)]
players = team_a + team_b

max_episodes = 10000
for i in range(max_episodes):
	observations = env.reset_game(randomize = True)
	while True:
		actions = [player.ai.choose_action(observations[i]) for i, player in enumerate(players)]
		env.step(players_actions = zip(players, actions))
	
	



