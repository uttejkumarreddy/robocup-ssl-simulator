import os
import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

from utils.logger import Logger

# Checkpoint Directories
DDPG_CHKPT_DIR = "checkpoints/ddpg/"

class ActorNetwork(nn.Module):
	def __init__(
		self,
		alpha,
		input_dims,
		fc1_dims,
		fc2_dims,
		n_actions,
		name,
		chkpt_dir = DDPG_CHKPT_DIR,
	):
		super(ActorNetwork, self).__init__()

		self.logger = Logger()

		self.input_dims = input_dims
		self.n_actions = n_actions
		self.fc1_dims = fc1_dims
		self.fc2_dims = fc2_dims
		self.checkpoint_file = os.path.join(chkpt_dir, name + "_ddpg")

		self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)
		f1 = 1.0 / np.sqrt(self.fc1.weight.data.size()[0])
		T.nn.init.uniform_(self.fc1.weight.data, -f1, f1)
		T.nn.init.uniform_(self.fc1.bias.data, -f1, f1)
		self.bn1 = nn.LayerNorm(self.fc1_dims)

		self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
		f2 = 1 / np.sqrt(self.fc2.weight.data.size()[0])
		T.nn.init.uniform_(self.fc2.weight.data, -f2, f2)
		T.nn.init.uniform_(self.fc2.bias.data, -f2, f2)
		self.bn2 = nn.LayerNorm(self.fc2_dims)

		f3 = 0.003
		self.mu = nn.Linear(self.fc2_dims, self.n_actions)
		T.nn.init.uniform_(self.mu.weight.data, -f3, f3)
		T.nn.init.uniform_(self.mu.bias.data, -f3, f3)

		self.optimizer = optim.Adam(self.parameters(), lr=alpha)

		self.device = T.device("cuda" if T.cuda.is_available() else "cpu")
		self.to(self.device)

	def forward(self, state):
		x = self.fc1(state)
		x = self.bn1(x)
		x = F.relu(x)

		x = self.fc2(x)
		x = self.bn2(x)
		x = F.relu(x)

		x = T.tanh(self.mu(x))

		return x

	def save_checkpoint(self):
		self.logger.write("Saving checkpoint to: " + self.checkpoint_file)
		T.save(self.state_dict(), self.checkpoint_file)

	def load_checkpoint(self):
		if os.path.isfile(self.checkpoint_file):
			self.logger.write("Loading checkpoint from: " + self.checkpoint_file)
			self.load_state_dict(T.load(self.checkpoint_file, map_location=self.device))

class CriticNetwork(nn.Module):
	def __init__(
		self,
		beta,
		input_dims,
		fc1_dims,
		fc2_dims,
		n_actions,
		name,
		chkpt_dir = DDPG_CHKPT_DIR,
	):
		super(CriticNetwork, self).__init__()

		self.logger = Logger()

		self.input_dims = input_dims
		self.fc1_dims = fc1_dims
		self.fc2_dims = fc2_dims
		self.n_actions = n_actions
		self.checkpoint_file = os.path.join(chkpt_dir, name + "_ddpg")

		self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)
		f1 = 1.0 / np.sqrt(self.fc1.weight.data.size()[0])
		T.nn.init.uniform_(self.fc1.weight.data, -f1, f1)
		T.nn.init.uniform_(self.fc1.bias.data, -f1, f1)
		self.bn1 = nn.LayerNorm(self.fc1_dims)

		self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
		f2 = 1.0 / np.sqrt(self.fc2.weight.data.size()[0])
		T.nn.init.uniform_(self.fc2.weight.data, -f2, f2)
		T.nn.init.uniform_(self.fc2.bias.data, -f2, f2)
		self.bn2 = nn.LayerNorm(self.fc2_dims)

		self.action_value = nn.Linear(self.n_actions, self.fc2_dims)
		f3 = 0.003
		self.q = nn.Linear(self.fc2_dims, 1)
		T.nn.init.uniform_(self.q.weight.data, -f3, f3)
		T.nn.init.uniform_(self.q.bias.data, -f3, f3)

		self.optimizer = optim.Adam(self.parameters(), lr=beta)

		self.device = T.device("cuda" if T.cuda.is_available() else "cpu")
		self.to(self.device)

	def forward(self, state, action):
		state_value = self.fc1(state)
		state_value = self.bn1(state_value)
		state_value = F.relu(state_value)
		state_value = self.fc2(state_value)
		state_value = self.bn2(state_value)

		action_value = F.relu(self.action_value(action))
		state_action_value = F.relu(T.add(state_value, action_value))
		state_action_value = self.q(state_action_value)

		return state_action_value

	def save_checkpoint(self):
		self.logger.write("Saving checkpoint to: " + self.checkpoint_file)
		T.save(self.state_dict(), self.checkpoint_file)

	def load_checkpoint(self):
		if os.path.isfile(self.checkpoint_file):
			self.logger.write("Loading checkpoint from: " + self.checkpoint_file)
			self.load_state_dict(T.load(self.checkpoint_file, map_location=self.device))