from abc import ABC, abstractmethod

class BaseAgent(ABC):
	@abstractmethod
	def __init__(self):
		pass

	@abstractmethod
	def choose_action(self):
		pass

	@abstractmethod
	def remember(self):
		pass

	@abstractmethod
	def learn(self):
		pass

	@abstractmethod
	def save_models(self):
		pass
	
	@abstractmethod
	def load_models(self):
		pass

