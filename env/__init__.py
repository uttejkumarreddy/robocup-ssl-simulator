from env.arena import Arena
from env.env import SoccerEnvironment

def make(num_players_team_A, num_players_team_B, render = True):
	arena = Arena().construct(num_players_team_A, num_players_team_B)
	return SoccerEnvironment(num_players_team_A, num_players_team_B, render)