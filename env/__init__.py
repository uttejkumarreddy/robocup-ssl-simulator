from env.arena import Arena
from env.simulation import Simulation

def make(num_players_team_A, num_players_team_B, render = True):
	arena = Arena().construct(num_players_team_A, num_players_team_B)
	sim = Simulation().run()