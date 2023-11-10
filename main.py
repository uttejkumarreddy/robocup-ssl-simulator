from env.player import Player
from env.ball import Ball

import env
import os

size = 'XS'
num_players_team_A = 6
num_players_team_B = 6

os.environ['FIELD_SIZE'] = size
env = env.make(size = size, num_players_team_A = num_players_team_A, num_players_team_B = num_players_team_B, render = True)

team_a = [Player('A', 'A_{i}'.format(i = i), env) for i in range(num_players_team_A)]
team_b = [Player('B', 'B_{i}'.format(i = i), env) for i in range(num_players_team_B)]
ball	 = Ball(env.model)

env.set_game_elements(team_a, team_b, ball)
env.run()

max_episodes = 10000
for i in range(max_episodes):
	observations, states, rewards = env.reset(randomize = True)

