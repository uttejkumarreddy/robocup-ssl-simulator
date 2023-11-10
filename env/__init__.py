from env.arena import Arena
from env.env import SoccerEnvironment

def make(size, num_players_team_A, num_players_team_B, render = True):
	arena = Arena(size).construct()
	return SoccerEnvironment(num_players_team_A, num_players_team_B, render)