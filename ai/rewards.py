import numpy as np

def move_to_ball(data, player, ball):
	''' Reward the player for moving closer to the ball proportional to its speed '''
	player_position = player.get_xy_position(data)
	player_velocity = player.get_xy_velocity(data)

	ball_position = ball.get_xy_position(data)

	# vel-to-ball: player's linear velocity projected onto its unit direction vector towards the ball, thresholded at zero
	player_to_ball_unit_vector = (ball_position - player_position) / np.linalg.norm(ball_position - player_position)
	reward_vel_to_ball = np.dot(player_velocity, player_to_ball_unit_vector)

	return 0.05 * reward_vel_to_ball

def score_goal(data, player, ball, geom_team_A_goal, geom_team_B_goal, goal_pos_x):
	''' Reward player for moving closer to ball and pushing ball into goal '''
	player_position = player.get_xy_position(data)
	player_velocity = player.get_xy_velocity(data)

	ball_position = ball.get_xy_position(data)
	ball_velocity = ball.get_xy_velocity(data)

	# vel-player-to-ball: player's linear velocity projected onto its unit direction vector towards the ball, thresholded at zero
	player_to_ball_unit_vector = (ball_position - player_position) / np.linalg.norm(ball_position - player_position)
	reward_vel_to_ball = np.dot(player_velocity, player_to_ball_unit_vector)

	# vel-ball-to-goal: ball's linear velocity projected onto its unit direction vector towards the goal, thresholded at zero
	goal_position = [-goal_pos_x, 0] if player.team == 'A' else [goal_pos_x, 0]
	ball_to_goal_unit_vector = (goal_position - ball_position) / np.linalg.norm(goal_position - ball_position)
	reward_vel_ball_to_goal = np.dot(ball_velocity, ball_to_goal_unit_vector)

	# +1 reward if goal is scored. If scored in opponent goal, -1
	reward_goal = 0
	contacts = data.contact
	for c in contacts:
		if c.geom1 == ball.geom_id and c.geom2 == geom_team_A_goal \
			or c.geom1 == geom_team_A_goal and c.geom2 == ball.geom_id:
			reward_goal = 1 if player.team == 'A' else -1
		elif c.geom1 == ball.geom_id and c.geom2 == geom_team_B_goal \
			or c.geom1 == geom_team_B_goal and c.geom2 == ball.geom_id:
			reward_goal = -1 if player.team == 'A' else 1

	done = True if reward_goal != 0 else False

	return reward_goal + (0.05 * reward_vel_to_ball) + (0.1 * reward_vel_ball_to_goal), done