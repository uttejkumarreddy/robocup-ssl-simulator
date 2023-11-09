from env.arena import Arena
from env.env import SoccerEnvironment

def make(render = True):
	arena = Arena().construct()
	return SoccerEnvironment(render)