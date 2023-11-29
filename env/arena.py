import numpy as np

class Arena:
	def __new__(cls, *args):
		if not hasattr(cls, 'instance'):
			cls.instance = super(Arena, cls).__new__(cls)
		return cls.instance

	def __init__(self, size):
		# All values are halved from original, since mujoco uses radius
		self.arena_props = {
			'boundary_wall_length': 48,
			'boundary_wall_width': 33,
			'goal_back_length': 5,
			'goal_arm_length': 0.9,
			'goal_width': 0.2,
			'goal_height': 1.6,
			'goal_pos_x': 46.8,
			'goal_pos_y': 45.9,
			'boundary_line_length': 45,
			'boundary_line_width': 30,
			'partial_goal_line_length': 12,
			'partial_goal_line_pos': 18,
			'defence_box_length': 5,
			'defence_box_width': 10,
			'defence_box_arm_x_pos': 40,
			'defence_box_arm_y_pos': 10,
			'defence_box_main_x_pos': 35,
		}

		self.size = size
		self.current_arena_props = self.calculate_arena_props_to_size(self.size)
		self.goal_positions = self.get_goal_positions()
		self.corner_positions = self.get_corner_positions()

		self.xml_arena_division_b = \
			'''
			<mujoco>
				<default>
					<geom contype="1" conaffinity="1" condim="3" friction=".5 .02 .02" />
				</default>

				<worldbody>
					<body name="arena">

						<geom name="field" type="plane" size="52 34 0.1" pos="0 0 0" rgba="0 1 0 1" />

						<geom name="boundary_S" type="box" size="{boundary_wall_length} 0.1 1" pos="0 {boundary_wall_width} 0" rgba="0 0 0 1" mass="1000" />
						<geom name="boundary_N" type="box" size="{boundary_wall_length} 0.1 1" pos="0 -{boundary_wall_width} 0" rgba="0 0 0 1" mass="1000" />
						<geom name="boundary_W" type="box" size="{boundary_wall_width} 0.1 1" pos="{boundary_wall_length} 0 0" rgba="0 0 0 1" euler="0 0 90" mass="1000" />
						<geom name="boundary_E" type="box" size="{boundary_wall_width} 0.1 1" pos="-{boundary_wall_length} 0 0" rgba="0 0 0 1" euler="0 0 90" mass="1000" />

						<geom name="goalE_E" type="box" size="{goal_back_length} {goal_width} {goal_height}" pos="{goal_pos_x} 0 0" rgba="1 0 0 1" euler="0 0 90" />
						<geom name="goalE_N" type="box" size="{goal_arm_length} {goal_width} {goal_height}" pos="{goal_pos_y} {goal_back_length} 0" rgba="1 0 0 1" />
						<geom name="goalE_S" type="box" size="{goal_arm_length} {goal_width} {goal_height}" pos="{goal_pos_y} -{goal_back_length} 0" rgba="1 0 0 1" />

						<geom name="goalW_W" type="box" size="{goal_back_length} {goal_width} {goal_height}" pos="-{goal_pos_x} 0 0" rgba="0 0 1 1" euler="0 0 90" />
						<geom name="goalW_N" type="box" size="{goal_arm_length} {goal_width} {goal_height}" pos="-{goal_pos_y} {goal_back_length} 0" rgba="0 0 1 1" />
						<geom name="goalW_S" type="box" size="{goal_arm_length} {goal_width} {goal_height}" pos="-{goal_pos_y} -{goal_back_length} 0" rgba="0 0 1 1" />

						<geom name="line_S" type="box" size="0.001 {boundary_line_length} 0.01" pos="0 {boundary_line_width} 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_N" type="box" size="0.001 {boundary_line_length} 0.01" pos="0 -{boundary_line_width} 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_goalE" type="box" size="0.001 {goal_back_length} 0.01" pos="-{boundary_line_length} 0 0" rgba="255 255 0 1" euler="0 90 0" />
						<geom name="line_goalE_N" type="box" size="0.001 {partial_goal_line_length} 0.01" pos="-{boundary_line_length} -{partial_goal_line_pos} 0" rgba="255 255 255 1" euler="0 90 0" />
						<geom name="line_goalE_S" type="box" size="0.001 {partial_goal_line_length} 0.01" pos="-{boundary_line_length} {partial_goal_line_pos} 0" rgba="255 255 255 1" euler="0 90 0" />
						<geom name="line_goalW" type="box" size="0.001 {goal_back_length} 0.01" pos="{boundary_line_length} 0 0" rgba="255 255 0 1" euler="0 90 0" />
						<geom name="line_goalW_N" type="box" size="0.001 {partial_goal_line_length} 0.01" pos="{boundary_line_length} -{partial_goal_line_pos} 0" rgba="255 255 255 1" euler="0 90 0" />
						<geom name="line_goalW_S" type="box" size="0.001 {partial_goal_line_length} 0.01" pos="{boundary_line_length} {partial_goal_line_pos} 0" rgba="255 255 255 1" euler="0 90 0" />

						<geom name="line_halfway" type="box" size="0.001 {boundary_line_width} 0.01" pos="0 0 0" rgba="255 255 255 1" euler="0 90 0" />
						<geom name="line_goal2goal" type="box" size="0.001 {boundary_line_length} 0.01" pos="0 0 0" rgba="255 255 255 1" euler="90 0 90" />

						<geom name="line_defenceW_S" type="box" size="0.001 {defence_box_length} 0.01" pos="{defence_box_arm_x_pos} {defence_box_arm_y_pos} 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_defenceW_N" type="box" size="0.001 {defence_box_length} 0.01" pos="{defence_box_arm_x_pos} -{defence_box_arm_y_pos} 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_defenceW_E" type="box" size="0.001 {defence_box_width} 0.01" pos="{defence_box_main_x_pos} 0 0" rgba="255 255 255 1" euler="0 90 0" />

						<geom name="line_defenceE_S" type="box" size="0.001 {defence_box_length} 0.01" pos="-{defence_box_arm_x_pos} {defence_box_arm_y_pos} 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_defenceE_N" type="box" size="0.001 {defence_box_length} 0.01" pos="-{defence_box_arm_x_pos} -{defence_box_arm_y_pos} 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_defenceE_W" type="box" size="0.001 {defence_box_width} 0.01" pos="-{defence_box_main_x_pos} 0 0" rgba="255 255 255 1" euler="0 90 0" />

					</body>

					<body name="ball" pos="0 0 0.215">
						<geom name="ball" type="sphere" size="0.215" rgba="1 0.647 0 1" mass="2.77" friction="1" />
						<joint name="ball" type="free" />
					</body>

					<body name="A_0" pos="50 0 0.365">
						<geom name="A_0" type="sphere" size="0.365" rgba="1 0 0 1" mass="200" density="100" />
						<joint name="A_0" type="free" />
					</body>

					<body name="A_1" pos="50 2 0.365">
						<geom name="A_1" type="sphere" size="0.365" rgba="1 0 0 1" mass="200" density="100" />
						<joint name="A_1" type="free" />
					</body>

					<body name="A_2" pos="50 4 0.365">
						<geom name="A_2" type="sphere" size="0.365" rgba="1 0 0 1" mass="200" density="100" />
						<joint name="A_2" type="free" />
					</body>

					<body name="B_0" pos="-50 0 0.365">
						<geom name="B_0" type="sphere" size="0.365" rgba="0 0 1 1" mass="200" density="100" />
						<joint name="B_0" type="free" />
					</body>

					<body name="B_1" pos="-50 2 0.365">
						<geom name="B_1" type="sphere" size="0.365" rgba="0 0 1 1" mass="200" density="100" />
						<joint name="B_1" type="free" />
					</body>

					<body name="B_2" pos="-50 4 0.365">
						<geom name="B_2" type="sphere" size="0.365" rgba="0 0 1 1" mass="200" density="100" />
						<joint name="B_2" type="free" />
					</body>

				</worldbody>
			</mujoco>
			'''

	def calculate_arena_props_to_size(self, size):
		''' Sizes 
		R: Regular: arena_props
		M: Medium: arena_props / 2
		S: Small:	arena_props / 4 
		XS: Extra Small: arena_props / 8
		'''
		arena_props_of_size = None
		match size:
			case 'R':
				arena_props_of_size = self.arena_props
			case 'M':
				arena_props_of_size = {k: v / 2 for k, v in self.arena_props.items()}
			case 'S':
				arena_props_of_size = {k: v / 4 for k, v in self.arena_props.items()}
			case 'XS':
				arena_props_of_size = {k: v / 8 for k, v in self.arena_props.items()}
			case _:
				raise Exception('Invalid size')
		
		arena_props_of_size['goal_height'] = self.arena_props['goal_height']
		return arena_props_of_size
	
	def get_goal_positions(self):
		'''
		goal positions (A_goal_top_x, A_goal_top_y, A_goal_bottom_x, A_goal_bottom_y, \
			B_goal_top_x, B_goal_top_y, B_goal_bottom_x, B_goal_bottom_y)
		'''
		return [
			self.current_arena_props['boundary_line_length'], # A_goal_top_x
			self.current_arena_props['goal_back_length'], # A_goal_top_y
			self.current_arena_props['boundary_line_length'], # A_goal_bottom_x
			-self.current_arena_props['goal_back_length'], # A_goal_bottom_y
			-self.current_arena_props['boundary_line_length'], # B_goal_top_x
			self.current_arena_props['goal_back_length'], # B_goal_top_y
			-self.current_arena_props['boundary_line_length'], # B_goal_bottom_x
			-self.current_arena_props['goal_back_length'], # B_goal_bottom_y
		]
	
	def get_corner_positions(self):
		'''
		corner positions (top_right_x, top_right_y, bottom_right_x, bottom_right_y, \
			top_left_x, top_left_y, bottom_left_x, bottom_left_y)
		'''
		return [
			self.current_arena_props['boundary_line_length'], # top_right_x
			self.current_arena_props['boundary_line_width'], # top_right_y
			self.current_arena_props['boundary_line_length'], # bottom_right_x
			-self.current_arena_props['boundary_line_width'], # bottom_right_y
			-self.current_arena_props['boundary_line_length'], # top_left_x
			self.current_arena_props['boundary_line_width'], # top_left_y
			-self.current_arena_props['boundary_line_length'], # bottom_left_x
			-self.current_arena_props['boundary_line_width'], # bottom_left_y
		]

	def construct(self):
		xml_arena_division_b = self.xml_arena_division_b.format(**self.current_arena_props)
		with open('env/assets/arena_division_b.xml', 'w') as f:
			f.write(xml_arena_division_b)