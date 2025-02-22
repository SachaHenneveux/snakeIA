import random
import torch
import torch.nn as nn
import torch.optim as optim
from environnement import NUM_ACTIONS

class QNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(QNetwork, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.LeakyReLU(),
            nn.Linear(64, 128),
            nn.LeakyReLU(),
            nn.Linear(128, 256),
            nn.LeakyReLU(),
            nn.Linear(256, 32),
            nn.LeakyReLU(),
            nn.Linear(32, output_dim)
        )
        
    def forward(self, x):
        return self.model(x)

class DQNAgent:
    def __init__(self, lr=0.0001, gamma=0.99, epsilon=1.0, epsilon_decay=0.99):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = QNetwork(input_dim=7, output_dim=NUM_ACTIONS).to(self.device)
        self.optimizer = optim.AdamW(self.model.parameters(), lr=lr)
        self.criteria = nn.MSELoss()
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
    
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, NUM_ACTIONS - 1)
        else:
            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            with torch.no_grad():
                q_values = self.model(state_tensor)
            return torch.argmax(q_values).item()
    
    def update(self, state, action, reward, next_state, done):
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0).to(self.device)
        q_values = self.model(state_tensor)
        q_value = q_values[0, action]
        
        with torch.no_grad():
            next_q_values = self.model(next_state_tensor)
            max_next_q = torch.max(next_q_values)
            target = reward + (self.gamma * max_next_q * (1 - int(done)))
        
        loss = self.criteria(q_value, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
    def decay_epsilon(self):
        self.epsilon *= self.epsilon_decay
