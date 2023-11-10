from env.sim import Simulation
from gymnasium import spaces
from env.arena import Arena

import os
import numpy as np

class SoccerEnvironment(Simulation):
	def __new__(cls, *args):
		if not hasattr(cls, 'instance'):
			cls.instance = super(SoccerEnvironment, cls).__new__(cls)
		return cls.instance

	def __init__(self, num_players_team_A, num_players_team_B, render = True):
		self.num_players_team_A = num_players_team_A
		self.num_players_team_B = num_players_team_B

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
			np.tile(player_information_low, 11),
		))

		observation_space_high = np.concatenate((
			player_information_high,
			ball_information_high,
			goal_positions_high,
			corner_positions_high,
			np.tile(player_information_high, 11),
		))

		self.observation_space = spaces.Box(
			low  = observation_space_low,
			high = observation_space_high,
			dtype = np.float32
		)

	def set_game_elements(self, team_A, team_B, ball):
		self.team_A = team_A
		self.team_B = team_B
		self.ball = ball

	def get_observation_space(self):
		pass

	def reset(self, randomize = True):
		current_arena_props = Arena(os.environ['FIELD_SIZE']).current_arena_props
		spawn_pos_limits_division_B = [current_arena_props['boundary_line_length'] - 1, current_arena_props['boundary_line_width'] - 1]

		if randomize is True:
			for i in range(self.num_players_team_A):
				random_position = (
					np.random.uniform(-spawn_pos_limits_division_B[0], spawn_pos_limits_division_B[0]),
					np.random.uniform(-spawn_pos_limits_division_B[1], spawn_pos_limits_division_B[1]),
					0.365
				)
				self.team_A[i].set_position(self.data, random_position)

			for i in range(self.num_players_team_B):
				random_position = (
					np.random.uniform(-spawn_pos_limits_division_B[0], spawn_pos_limits_division_B[0]),
					np.random.uniform(-spawn_pos_limits_division_B[1], spawn_pos_limits_division_B[1]),
					0.365
				)
				self.team_B[i].set_position(self.data, random_position)

			random_position = (
				np.random.uniform(-spawn_pos_limits_division_B[0], spawn_pos_limits_division_B[0]),
				np.random.uniform(-spawn_pos_limits_division_B[1], spawn_pos_limits_division_B[1]),
				0.215
			)
			self.ball.set_position(self.data, random_position)

	def step(self):
		pass