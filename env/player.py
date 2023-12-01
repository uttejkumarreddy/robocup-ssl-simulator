import mujoco as mj
import numpy as np
import math

from ai.dummy_ai import DummyAgent
from utils.logger import Logger

class Player:
	def __init__(self, team, name, env):
		self.team = team
		self.name = name
		self.env = env

		model = self.env.model

		self.body_id 	= mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY.value, self.name)
		self.geom_id 	= mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM.value, self.name)
		self.joint_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_JOINT.value, self.name)

		self.heading = np.random.uniform(-np.pi, np.pi)

		self.ai_name = None
		self.ai = DummyAgent()

		logger = Logger()
		logger.write("Player {0} initialized. body_id {1} geom_id {2} joint_id {3}".format(self.name, self.body_id, self.geom_id, self.joint_id))

	def get_position(self, data):
		return data.qpos[self.joint_id * 7 : self.joint_id * 7 + 3]
	
	def get_xy_position(self, data):
		return data.qpos[self.joint_id * 7 : self.joint_id * 7 + 2]
	
	def set_position(self, data, position):
		data.qpos[self.joint_id * 7 : self.joint_id * 7 + 3] = position

	def get_velocity(self, data):
		return data.qvel[self.joint_id * 6 : self.joint_id * 6 + 6]
	
	def get_xy_velocity(self, data):
		return data.qvel[self.joint_id * 6 : self.joint_id * 6 + 2]
	
	def set_velocity(self, data, velocity):
		data.qvel[self.joint_id * 6 : self.joint_id * 6 + 3] = velocity

	def get_orientation(self):
		return [self.heading]
	
	def set_heading_and_velocity(self, data, speed, rotation):
		# TODO: When applying this to the API, calculate the rotation from the current heading and the desired heading
		self.heading = rotation # Sphero bolt heading is relative to the user and not the robot 
		direction = np.array([math.cos(self.heading), math.sin(self.heading), 0])
		velocity = speed * direction
		self.set_velocity(data, velocity)

	def get_observation(self, data):
		# (x_pos, y_pos, x_vel, y_vel, orientation)
		return np.concatenate((self.get_xy_position(data), self.get_xy_velocity(data), [self.heading]))