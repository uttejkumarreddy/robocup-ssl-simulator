from env.arena import Arena
from env.env import SoccerEnvironment

def make(size = 'L', num_players_team_A = '6', num_players_team_B = '6', render = True):
	arena = Arena().construct(size)
	return SoccerEnvironment(num_players_team_A, num_players_team_B, render)