import mujoco as mj

class Ball:
	def __init__(self, model):
		self.name = 'ball'

		self.body_id 	= mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY.value, self.name)
		self.geom_id 	= mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM.value, self.name)
		self.joint_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_JOINT.value, self.name)

	def get_xy_position(self, data):
		return data.qpos[self.joint_id * 7 : self.joint_id * 7 + 2]