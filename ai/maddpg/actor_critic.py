import os
import numpy as np
import torch as T
import torch.nn.functional as F
import torch.optim as optim
import torch.nn as nn

class ActorNetwork(nn.Module):
	def __init__(self, alpha, input_dims, fc1_dims, fc2_dims, n_actions, name, chkpt_dir):
		super(ActorNetwork, self).__init__()

		self.fc1_dims, self.fc2_dims = fc1_dims, fc2_dims
		self.chkpt_dir = chkpt_dir
		self.chkpt_file = os.path.join(chkpt_dir, name)

		self.fc1 = nn.Linear(input_dims, fc1_dims)
		self.fc2 = nn.Linear(fc1_dims, fc2_dims)
		self.mu = nn.Linear(fc2_dims, n_actions)

		self.optimizer = optim.Adam(self.parameters(), lr = alpha)
		self.device = T.device('cuda' if T.cuda.is_available() else 'cpu')
		self.to(self.device)

	def forward(self, state):
		x = F.relu(self.fc1(state))
		x = F.relu(self.fc2(x))
		mu = T.tanh(self.mu(x))

		return mu

	def save_checkpoint(self):
		os.makedirs(self.chkpt_dir, exist_ok=True)
		T.save(self.state_dict(), self.chkpt_file)

	def load_checkpoint(self):
		if os.path.exists(self.chkpt_file):
			self.load_state_dict(T.load(self.chkpt_file, map_location = self.device))

class CriticNetwork(nn.Module):
	def __init__(self, beta, input_dims, fc1_dims, fc2_dims, n_agents, n_actions, name, chkpt_dir):
		super(CriticNetwork, self).__init__()

		self.fc1_dims, self.fc2_dims = fc1_dims, fc2_dims
		self.chkpt_dir = chkpt_dir
		self.chkpt_file = os.path.join(chkpt_dir, name)

		self.fc1 = nn.Linear(input_dims + (n_actions * n_agents), fc1_dims)
		self.fc2 = nn.Linear(fc1_dims, fc2_dims)
		self.q = nn.Linear(self.fc2_dims, 1)

		self.optimizer = optim.Adam(self.parameters(), lr = beta)
		self.device = T.device('cuda' if T.cuda.is_available() else 'cpu')
		self.to(self.device)

	def forward(self, state, action):
		x = F.relu(self.fc1(T.cat([state, action], dim = 1)))
		x = F.relu(self.fc2(x))
		q = self.q(x)

		return q

	def save_checkpoint(self):
		os.makedirs(self.chkpt_dir, exist_ok=True)
		T.save(self.state_dict(), self.chkpt_file)

	def load_checkpoint(self):
		if os.path.exists(self.chkpt_file):
			self.load_state_dict(T.load(self.chkpt_file, map_location = self.device))