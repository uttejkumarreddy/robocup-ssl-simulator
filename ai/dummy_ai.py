from ai.base_ai import BaseAgent

class DummyAgent(BaseAgent):
	def __init__(self):
		pass
	
	def choose_action(self, observation):
		return [-1, 0] # [speed, rotation] for tanh actions translates to [0, 0]
	
	def remember(self, memory_unit):
		pass

	def learn(self):
		pass

	def save_models(self):
		pass

	def load_models(self):
		pass