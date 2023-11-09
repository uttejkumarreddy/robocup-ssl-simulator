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

					<body name="A_3" pos="50 -2 0.365">
						<geom name="A_3" type="sphere" size="0.365" rgba="1 0 0 1" mass="200" density="100" />
						<joint name="A_3" type="free" />
					</body>

					<body name="A_4" pos="50 -4 0.365">
						<geom name="A_4" type="sphere" size="0.365" rgba="1 0 0 1" mass="200" density="100" />
						<joint name="A_4" type="free" />
					</body>

					<body name="A_5" pos="50 -6 0.365">
						<geom name="A_5" type="sphere" size="0.365" rgba="1 0 0 1" mass="200" density="100" />
						<joint name="A_5" type="free" />
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

					<body name="B_3" pos="-50 -2 0.365">
						<geom name="B_3" type="sphere" size="0.365" rgba="0 0 1 1" mass="200" density="100" />
						<joint name="B_3" type="free" />
					</body>

					<body name="B_4" pos="-50 -4 0.365">
						<geom name="B_4" type="sphere" size="0.365" rgba="0 0 1 1" mass="200" density="100" />
						<joint name="B_4" type="free" />
					</body>

					<body name="B_5" pos="-50 -6 0.365">
						<geom name="B_5" type="sphere" size="0.365" rgba="0 0 1 1" mass="200" density="100" />
						<joint name="B_5" type="free" />
					</body>

				</worldbody>

			</mujoco>
			'''

	def construct(self):	
		with open('env/assets/arena_division_b.xml', 'w') as f:
			f.write(self.xml_arena_division_b)