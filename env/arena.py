import numpy as np

class Arena:
	def __init__(self):
		self.xml_arena_division_b = \
			'''
			<mujoco>

				<default>
					<geom contype="1" conaffinity="1" condim="3" friction=".5 .02 .02" />
				</default>

				<worldbody>

					<body name="arena">

						<geom name="field" type="plane" size="52 37 0.1" pos="0 0 0" rgba="0 1 0 1" />

						<geom name="boundary_S" type="box" size="48 0.1 1" pos="0 33 0" rgba="0 0 0 1" mass="1000" />
						<geom name="boundary_N" type="box" size="48 0.1 1" pos="0 -33 0" rgba="0 0 0 1" mass="1000" />
						<geom name="boundary_W" type="box" size="33 0.1 1" pos="48 0 0" rgba="0 0 0 1" euler="0 0 90" mass="1000" />
						<geom name="boundary_E" type="box" size="33 0.1 1" pos="-48 0 0" rgba="0 0 0 1" euler="0 0 90" mass="1000" />

						<geom name="goalE_W" type="box" size="5 0.2 1.6" pos="46.8 0 0" rgba="1 0 0 1" euler="0 0 90" />
						<geom name="goalE_S" type="box" size="0.9 0.2 1.6" pos="45.9 5 0" rgba="1 0 0 1" />
						<geom name="goalE_N" type="box" size="0.9 0.2 1.6" pos="45.9 -5 0" rgba="1 0 0 1" />

						<geom name="goalW_E" type="box" size="5 0.2 1.6" pos="-46.8 0 0" rgba="0 0 1 1" euler="0 0 90" />
						<geom name="goalW_S" type="box" size="0.9 0.2 1.6" pos="-45.9 5 0" rgba="0 0 1 1" />
						<geom name="goalW_N" type="box" size="0.9 0.2 1.6" pos="-45.9 -5 0" rgba="0 0 1 1" />

						<geom name="line_S" type="box" size="0.001 45 0.01" pos="0 30 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_N" type="box" size="0.001 45 0.01" pos="0 -30 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_goalE" type="box" size="0.001 5 0.01" pos="-45 0 0" rgba="255 255 0 1" euler="0 90 0" />
						<geom name="line_goalE_N" type="box" size="0.001 12 0.01" pos="-45 -18 0" rgba="255 255 255 1" euler="0 90 0" />
						<geom name="line_goalE_S" type="box" size="0.001 12 0.01" pos="-45 18 0" rgba="255 255 255 1" euler="0 90 0" />
						<geom name="line_goalW" type="box" size="0.001 5 0.01" pos="45 0 0" rgba="255 255 0 1" euler="0 90 0" />
						<geom name="line_goalW_N" type="box" size="0.001 12 0.01" pos="45 -18 0" rgba="255 255 255 1" euler="0 90 0" />
						<geom name="line_goalW_S" type="box" size="0.001 12 0.01" pos="45 18 0" rgba="255 255 255 1" euler="0 90 0" />

						<geom name="line_halfway" type="box" size="0.001 30 0.01" pos="0 0 0" rgba="255 255 255 1" euler="0 90 0" />
						<geom name="line_goal2goal" type="box" size="0.001 45 0.01" pos="0 0 0" rgba="255 255 255 1" euler="90 0 90" />

						<geom name="line_defenceW_S" type="box" size="0.001 5 0.01" pos="40 10 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_defenceW_N" type="box" size="0.001 5 0.01" pos="40 -10 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_defenceW_E" type="box" size="0.001 10 0.01" pos="35 0 0" rgba="255 255 255 1" euler="0 90 0" />

						<geom name="line_defenceE_S" type="box" size="0.001 5 0.01" pos="-40 10 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_defenceE_N" type="box" size="0.001 5 0.01" pos="-40 -10 0" rgba="255 255 255 1" euler="90 0 90" />
						<geom name="line_defenceE_W" type="box" size="0.001 10 0.01" pos="-35 0 0" rgba="255 255 255 1" euler="0 90 0" />

					</body>

					<body name="ball" pos="0 0 0.215">
						<geom name="ball" type="sphere" size="0.215" rgba="1 0.647 0 1" mass="2.77" friction="1" />
						<joint name="ball" type="free" />
					</body>

					{TEAM_A_PLAYERS}

					{TEAM_B_PLAYERS}

				</worldbody>
			</mujoco>
			'''

		self.xml_player_team_A = \
			'''
			<body name="{name}" pos="{pos_x} {pos_y} 0.365">
				<geom name="{name}" type="sphere" size="0.365" rgba="0 0 1 1" mass="200" density="100" />
				<joint name="{name}" type="free" />
			</body>
			'''

		self.xml_player_team_B = \
			'''
			<body name="{name}" pos="{pos_x} {pos_y} 0.365">
				<geom name="{name}" type="sphere" size="0.365" rgba="1 0 0 1" mass="200" density="100" />
				<joint name="{name}" type="free" />
			</body>
			'''

		self.spawn_pos_limits_division_B = [40, 25]
	
	def constuct_players_team_A(self, num_players):
		xml_team = ''
		for i in range(num_players):
			name = 'A_{i}'.format(i = i)
			pos_x = np.random.uniform(-self.spawn_pos_limits_division_B[0], self.spawn_pos_limits_division_B[0])
			pos_y = np.random.uniform(-self.spawn_pos_limits_division_B[1], self.spawn_pos_limits_division_B[1])
			xml_team += self.xml_player_team_A.format(name = name, pos_x = pos_x, pos_y = pos_y)
			xml_team += '\n'
		return xml_team

	def constuct_players_team_B(self, num_players):
		xml_team = ''
		for i in range(num_players):
			name = 'B_{i}'.format(i = i)
			pos_x = np.random.uniform(-self.spawn_pos_limits_division_B[0], self.spawn_pos_limits_division_B[0])
			pos_y = np.random.uniform(-self.spawn_pos_limits_division_B[1], self.spawn_pos_limits_division_B[1])
			xml_team += self.xml_player_team_B.format(name = name, pos_x = pos_x, pos_y = pos_y)
			xml_team += '\n'
		return xml_team

	def construct(self, num_players_team_A, num_players_team_B):
		xml_team_A_players = self.constuct_players_team_A(num_players_team_A)
		xml_team_B_players = self.constuct_players_team_B(num_players_team_B)
		xml_arena_division_b = self.xml_arena_division_b.format(TEAM_A_PLAYERS = xml_team_A_players, TEAM_B_PLAYERS = xml_team_B_players)
		
		with open('env/assets/arena_division_b.xml', 'w') as f:
			f.write(xml_arena_division_b)