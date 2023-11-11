import mujoco as mj
import numpy as np
from ai import ddpg
from utils.logger import Logger

class Player:
	def __init__(self, team, name, env):
		self.team = team
		self.name = name

		model = env.model

		self.body_id 	= mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY.value, self.name)
		self.geom_id 	= mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM.value, self.name)
		self.joint_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_JOINT.value, self.name)

		self.ai = ddpg.Agent(
			name = self.name,
			alpha = ddpg.ALPHA,
			beta = ddpg.BETA,
			input_dims =	[env.observation_space.shape[0]],
			tau = ddpg.TAU,
			gamma = ddpg.GAMMA,
			n_actions = env.action_space.shape[0],
			max_size = ddpg.BUFFER_SIZE,
			layer1_size = ddpg.LAYER_1_SIZE,
			layer2_size = ddpg.LAYER_2_SIZE,
			batch_size = ddpg.BATCH_SIZE,
		)

		self.heading = np.random.uniform(-np.pi, np.pi)

		logger = Logger()
		logger.write("Player {0} initialized. body_id {1} geom_id {2} joint_id {3}".format(self.name, self.body_id, self.geom_id, self.joint_id))

	def set_position(self, data, position):
		data.qpos[self.joint_id * 7 : self.joint_id * 7 + 3] = position