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