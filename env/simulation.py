from mujoco.glfw import glfw
import mujoco as mj

import os
import numpy as np
import time

class Simulation:
	def __init__(self, render, env_path):
		self.render = render

		self.model = mj.MjModel.from_xml_path(env_path)
		self.data = mj.MjData(self.model)
		self.cam = mj.MjvCamera()
		self.opt = mj.MjvOption()

		self.button_left = False
		self.button_middle = False
		self.button_right = False
		self.lastx = 0
		self.lasty = 0

		if self.render is True:
			glfw.init()
			self.window = glfw.create_window(1200, 900, "RoboCup SSL Simulator", None, None)
			glfw.make_context_current(self.window)
			glfw.swap_interval(1)

			mj.mjv_defaultCamera(self.cam)
			mj.mjv_defaultOption(self.opt)

			glfw.set_key_callback(self.window, self.keyboard)
			glfw.set_cursor_pos_callback(self.window, self.mouse_move)
			glfw.set_mouse_button_callback(self.window, self.mouse_button)
			glfw.set_scroll_callback(self.window, self.mouse_scroll)

			self.context = mj.MjrContext(self.model, mj.mjtFontScale.mjFONTSCALE_150.value)

		self.scene = mj.MjvScene(self.model, maxgeom=10000)

	def keyboard(self, window, key, scancode, act, mods):
		if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
			mj.mj_resetData(self.model, self.data)
			mj.mj_forward(self.model, self.data)

	def mouse_button(self, window, button, act, mods):
		self.button_left = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS)
		self.button_middle = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_MIDDLE) == glfw.PRESS)
		self.button_right = (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS)
		glfw.get_cursor_pos(window)

	def mouse_move(self, window, xpos, ypos):
		dx = xpos - self.lastx
		dy = ypos - self.lasty
		self.lastx = xpos
		self.lasty = ypos

		if (
			(not self.button_left)
			and (not self.button_middle)
			and (not self.button_right)
		):
			return

		width, height = glfw.get_window_size(window)

		PRESS_LEFT_SHIFT = glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
		PRESS_RIGHT_SHIFT = glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
		mod_shift = PRESS_LEFT_SHIFT or PRESS_RIGHT_SHIFT

		if self.button_right:
			if mod_shift:
				action = mj.mjtMouse.mjMOUSE_MOVE_H
			else:
				action = mj.mjtMouse.mjMOUSE_MOVE_V
		elif self.button_left:
			if mod_shift:
				action = mj.mjtMouse.mjMOUSE_ROTATE_H
			else:
				action = mj.mjtMouse.mjMOUSE_ROTATE_V
		else:
				action = mj.mjtMouse.mjMOUSE_ZOOM

		mj.mjv_moveCamera(self.model, action, dx / height, dy / height, self.scene, self.cam)

	def mouse_scroll(self, window, xoffset, yoffset):
		action = mj.mjtMouse.mjMOUSE_ZOOM
		mj.mjv_moveCamera(self.model, action, 0.0, -0.05 * yoffset, self.scene, self.cam)

	def reset(self):
		mj.mj_resetData(self.model, self.data)
		mj.mj_kinematics(self.model, self.data)
		mj.mj_forward(self.model, self.data)

	def controller(self, model, data):
		pass

	def run(self):
		self.reset()
		mj.set_mjcb_control(self.controller)

		while True:
			for i in range(10):
				mj.mj_step(self.model, self.data)
			
			mj.mjv_updateScene(self.model, self.data, self.opt, None, self.cam, mj.mjtCatBit.mjCAT_ALL.value, self.scene)

			if self.render is True:
				viewport_width, viewport_height = glfw.get_framebuffer_size(self.window)
				viewport = mj.MjrRect(0, 0, viewport_width, viewport_height)

				mj.mjr_render(viewport, self.scene, self.context)

				glfw.swap_buffers(self.window)
				glfw.poll_events()
	
	def stop(self):
		glfw.terminate()