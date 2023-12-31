from env.sim import Simulation
from gymnasium import spaces
from env.arena import Arena
from config import sphero as sphero_config
from ai import rewards as rewards_fn

import os
import numpy as np
import mujoco as mj

class SoccerEnvironment(Simulation):
	def __new__(cls, *args):
		if not hasattr(cls, 'instance'):
			cls.instance = super(SoccerEnvironment, cls).__new__(cls)
		return cls.instance

	def __init__(self, num_players_team_A, num_players_team_B, render = True):
		self.num_players_team_A = num_players_team_A
		self.num_players_team_B = num_players_team_B
		self.render = render

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

		# Arena
		self.current_arena = Arena(os.environ['RSS_FIELD_SIZE'])

		self.team_A_goal = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, 'line_goalE')
		self.team_B_goal = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, 'line_goalW')

	def set_game_elements(self, team_A, team_B, ball):
		self.team_A = team_A
		self.team_B = team_B
		self.ball = ball

	def get_observation_space(self):
		'''
			Always returns observations of all 12 players on the field regardless of whether they're in the game
			proprioception: player information (x_pos, y_pos, x_vel, y_vel, orientation)
			ball information (x_pos, y_pos, x_vel, y_vel)
			goal positions (A_goal_top_x, A_goal_top_y, A_goal_bottom_x, A_goal_bottom_y, \
				B_goal_top_x, B_goal_top_y, B_goal_bottom_x, B_goal_bottom_y)
			corner positions (top_right_x, top_right_y, bottom_right_x, bottom_right_y, \
				top_left_x, top_left_y, bottom_left_x, bottom_left_y)
			teammates and opponents information (x_pos, y_pos, x_vel, y_vel, orientation)
		'''
		n_max_players = int(os.environ['RSS_N_MAX_PLAYERS'])

		team_a_obs = np.array([self.team_A[i].get_observation(self.data) for i in range(n_max_players)])
		team_b_obs = np.array([self.team_B[i].get_observation(self.data) for i in range(n_max_players)])
		ball_obs = self.ball.get_observation(self.data)
		goals_pos = self.current_arena.goal_positions
		corners_pos = self.current_arena.corner_positions

		players_obs_spaces = []

		for i in range(n_max_players):
			team_a_player_i_obs_space = np.concatenate((team_a_obs[i], ball_obs, goals_pos, corners_pos,
				np.concatenate((team_a_obs[:i].flatten(), team_a_obs[i+1:].flatten(), team_b_obs.flatten()))))
			players_obs_spaces.append(team_a_player_i_obs_space)

		for i in range(n_max_players):
			team_b_player_i_obs_space = np.concatenate((team_b_obs[i], ball_obs, goals_pos, corners_pos,
				np.concatenate((team_a_obs.flatten(), team_b_obs[:i].flatten(), team_b_obs[i+1:].flatten())))).flatten()
			players_obs_spaces.append(team_b_player_i_obs_space)

		return players_obs_spaces
		
	def randomize_elements_spawn(self, spawn_pos_limits_division_B):
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

	def reset_game(self, randomize = True):
		super().reset()

		current_arena_props = self.current_arena.current_arena_props

		spawn_pos_limits_division_B = [current_arena_props['boundary_line_length'] - 1, current_arena_props['boundary_line_width'] - 1]
		self.randomize_elements_spawn(spawn_pos_limits_division_B) if randomize is True else None

		observations = self.get_observation_space()
		return observations
	
	# TODO: Move to utils
	def scale_linear(self, x, min, max):
		# Linear scaling: f(x) = 0.5 * (max - min) * x + 0.5 * (max + min)
		return (0.5 * (max - min) * x) + (0.5 * (max + min))

	# TODO: Move to utils
	def preprocess_tanh_actions(self, action):
		# Actions are in the range [-1, 1]
		action_speed, action_rotation = action
		player_speed = self.scale_linear(action_speed, sphero_config.ENV_BOLT_MIN_SPEED, sphero_config.ENV_BOLT_MAX_SPEED)
		player_rotation = self.scale_linear(action_rotation, sphero_config.ENV_BOLT_MIN_ROTATION, sphero_config.ENV_BOLT_MAX_ROTATION)
		return player_speed, player_rotation
	
	def step(self, players_actions):
		if self.render is True:
			self.render_sim()

		for player, action in players_actions:
			speed, rotation = self.preprocess_tanh_actions(action)
			player.set_heading_and_velocity(self.data, speed, rotation)

		new_observations = self.get_observation_space()

		rewards, dones = [], []
		for player in self.team_A + self.team_B:
			reward, done = rewards_fn.score_goal(self.data, player, self.ball, self.team_A_goal, self.team_B_goal, self.current_arena.current_arena_props['boundary_line_length'])
			rewards.append(reward)
			dones.append(done)

		info = {}

		return new_observations, rewards, dones, info




