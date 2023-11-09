from env.player import Player
from env.ball import Ball

import env

num_players_team_A = 1
num_players_team_B = 0

env = env.make(render = True)

team_a = [Player('A', 'A_{i}'.format(i = i), env) for i in range(num_players_team_A)]
team_b = [Player('B', 'B_{i}'.format(i = i), env) for i in range(num_players_team_B)]
ball	 = Ball(env.model)

env.run()
