from env.sim import Simulation
from gymnasium import spaces

import os
import numpy as np

class SoccerEnvironment(Simulation):
	def __new__(cls, *args):
		if not hasattr(cls, 'instance'):
			cls.instance = super(SoccerEnvironment, cls).__new__(cls)
		return cls.instance

	def __init__(self, num_players_team_A, num_players_team_B, render = True):
		dirname = os.path.dirname(__file__)
		env_path = os.path.join(dirname, 'assets', 'arena_division_b.xml')

		super().__init__(render, env_path)

		# action_space: [speed, rotation]
		self.action_space = spaces.Box(
			low  = np.array([0, -np.pi], dtype=np.float32),
			high = np.array([1, np.pi], dtype=np.float32),
		)

		# player information (x_pos, y_pos, x_vel, y_vel, orientation)
		player_information_low 	= np.array([-48, -33, 0, 0, -np.pi], dtype=np.float32)
		player_information_high =	np.array([ 48,  33, 1, 1,  np.pi], dtype=np.float32)

		# ball information (x_pos, y_pos, x_vel, y_vel)
		ball_information_low 	= np.array([-48, -33, 0, 0], dtype=np.float32)
		ball_information_high = np.array([ 48,  33, 1, 1], dtype=np.float32)

		# goal positions (A_goal_top_x, A_goal_top_y, A_goal_bottom_x, A_goal_bottom_y, \
		# 	B_goal_top_x, B_goal_top_y, B_goal_bottom_x, B_goal_bottom_y)
		goal_positions_low 	= np.array([-45, -5, -45, -5, -45, -5, -45, -5], dtype=np.float32)
		goal_positions_high = np.array([ 45,  5,  45,  5,  45,  5,  45,  5], dtype=np.float32)

		# corner positions (top_left_x, top_left_y, top_right_x, top_right_y, \
		# 	bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y)
		corner_positions_low 	= np.array([-45, -30, -45, -30, -45, -30, -45, -30], dtype=np.float32)
		corner_positions_high = np.array([ 45,  30,  45,  30,  45,  30,  45,  30], dtype=np.float32)

		# observation_space: [player_information, ball_information, goal_positions, corner_positions, \
		# 	(num_players_team_A + num_players_team_B - 1) * player_information] => teammates and opponents information
		observation_space_low = np.concatenate((
			player_information_low,
			ball_information_low,
			goal_positions_low,
			corner_positions_low,
			np.tile(player_information_low, num_players_team_A + num_players_team_B - 1),
		))

		observation_space_high = np.concatenate((
			player_information_high,
			ball_information_high,
			goal_positions_high,
			corner_positions_high,
			np.tile(player_information_high, num_players_team_A + num_players_team_B - 1),
		))

		self.observation_space = spaces.Box(
			low  = observation_space_low,
			high = observation_space_high,
			dtype = np.float32
		)