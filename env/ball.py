import mujoco as mj
import numpy as np

class Ball:
	def __init__(self, model):
		self.name = 'ball'

		self.body_id 	= mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY.value, self.name)
		self.geom_id 	= mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM.value, self.name)
		self.joint_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_JOINT.value, self.name)

	def get_xy_position(self, data):
		return data.qpos[self.joint_id * 7 : self.joint_id * 7 + 2]

	def set_position(self, data, position):
		data.qpos[self.joint_id * 7 : self.joint_id * 7 + 3] = position
	
	def get_xy_velocity(self, data):
		return data.qvel[self.joint_id * 6 : self.joint_id * 6 + 2]
	
	def get_observation(self, data):
		# (x_pos, y_pos, x_vel, y_vel)
		return np.concatenate((self.get_xy_position(data), self.get_xy_velocity(data)))

	