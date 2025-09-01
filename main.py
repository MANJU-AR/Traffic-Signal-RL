# -------------------------
# Step 1: Add modules
# -------------------------
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import threading

# -------------------------
# Step 2: SUMO path
# -------------------------
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# -------------------------
# Step 3: Traci
# -------------------------
import traci

# -------------------------
# Step 4: SUMO config
# -------------------------
Sumo_config = [
    'sumo-gui',
    '-c', 'RL.sumocfg',
    '--step-length', '1',
    '--start',                  
    '--delay', '0'           
]
# -------------------------
# Step 5: Start SUMO
# -------------------------
traci.start(Sumo_config)
traci.gui.setSchema("View #0", "real world")

# -------------------------
# Step 6: Variables
# -------------------------
q_EB_0 = q_EB_1 = q_EB_2 = 0
q_SB_0 = q_SB_1 = q_SB_2 = 0
current_phase = 0

TOTAL_STEPS = 10000
ALPHA = 0.001
GAMMA = 0.9
EPSILON = 0.1
ACTIONS = [0, 1]
MIN_GREEN_STEPS = 100
last_switch_step = -MIN_GREEN_STEPS
cumulative_reward = 0.0

# -------------------------
# Step 7: Functions
# -------------------------
def get_queue_length(detector_id):
    return traci.lanearea.getLastStepVehicleNumber(detector_id)

def get_current_phase(tls_id):
    return traci.trafficlight.getPhase(tls_id)

def get_state():
    global q_EB_0, q_EB_1, q_EB_2, q_SB_0, q_SB_1, q_SB_2, current_phase

    detector_Node1_2_EB_0 = "Node1_2_EB_0"
    detector_Node1_2_EB_1 = "Node1_2_EB_1"
    detector_Node1_2_EB_2 = "Node1_2_EB_2"
    detector_Node2_7_SB_0 = "Node2_7_SB_0"
    detector_Node2_7_SB_1 = "Node2_7_SB_1"
    detector_Node2_7_SB_2 = "Node2_7_SB_2"
    traffic_light_id = "Node2"

    q_EB_0 = get_queue_length(detector_Node1_2_EB_0)
    q_EB_1 = get_queue_length(detector_Node1_2_EB_1)
    q_EB_2 = get_queue_length(detector_Node1_2_EB_2)
    q_SB_0 = get_queue_length(detector_Node2_7_SB_0)
    q_SB_1 = get_queue_length(detector_Node2_7_SB_1)
    q_SB_2 = get_queue_length(detector_Node2_7_SB_2)
    current_phase = get_current_phase(traffic_light_id)

    return (q_EB_0, q_EB_1, q_EB_2, q_SB_0, q_SB_1, q_SB_2, current_phase)

def get_reward(state):
    total_queue = sum(state[:-1])
    return -float(total_queue)

def apply_action(action, tls_id="Node2"):
    global last_switch_step
    if action == 0:
        return
    elif action == 1:
        if current_simulation_step - last_switch_step >= MIN_GREEN_STEPS:
            program = traci.trafficlight.getAllProgramLogics(tls_id)[0]
            num_phases = len(program.phases)
            next_phase = (get_current_phase(tls_id) + 1) % num_phases
            traci.trafficlight.setPhase(tls_id, next_phase)
            last_switch_step = current_simulation_step

# -------------------------
# Step 7a: DQN Agent
# -------------------------
class DQNAgent:
    def __init__(self, state_size, action_size, alpha=ALPHA, gamma=GAMMA, epsilon=EPSILON):
        self.state_size = state_size
        self.action_size = action_size
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.alpha))
        return model

    def get_action_from_policy(self, state):
        if random.random() < self.epsilon:
            return random.choice(ACTIONS)
        q_values = self.model.predict(np.array([state]), verbose=0)
        return int(np.argmax(q_values[0]))

    def train(self, state, action, reward, next_state):
        target = reward + self.gamma * np.max(self.model.predict(np.array([next_state]), verbose=0)[0])
        target_f = self.model.predict(np.array([state]), verbose=0)
        target_f[0][action] = target
        self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

# -------------------------
# Step 11: FastAPI with CORS
# -------------------------
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global live state variables
live_state = (0,0,0,0,0,0,0)
live_cumulative_reward = 0.0

@app.get("/status")
def get_status():
    return {
        "q_EB": live_state[:3],
        "q_SB": live_state[3:6],
        "current_phase": live_state[6],
        "total_queue": sum(live_state[:-1]),
        "cumulative_reward": live_cumulative_reward
        
    }

def run_api():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Start FastAPI in background
threading.Thread(target=run_api, daemon=True).start()

# -------------------------
# Step 8: Simulation + DQN loop
# -------------------------
state_size = 7
agent = DQNAgent(state_size, len(ACTIONS))

step_history = []
reward_history = []
queue_history = []

print("\n=== Starting DQN Online Learning ===")
for step in range(TOTAL_STEPS):
    current_simulation_step = step

    state = get_state()
    action = agent.get_action_from_policy(state)
    apply_action(action)
    traci.simulationStep()

    new_state = get_state()
    reward = get_reward(new_state)
    cumulative_reward += reward

    agent.train(state, action, reward, new_state)

    # Update live variables for FastAPI
    live_state = new_state
    live_cumulative_reward = cumulative_reward

    if step % 1 == 0:
        print(f"Step {step}, State: {state}, Action: {action}, Reward: {reward:.2f}, Cumulative Reward: {cumulative_reward:.2f}")
        step_history.append(step)
        reward_history.append(cumulative_reward)
        queue_history.append(sum(new_state[:-1]))

# -------------------------
# Step 9: Close SUMO
# -------------------------
traci.close()
print("\nDQN Training completed.")

# -------------------------
# Step 10: Visualization
# -------------------------
plt.figure(figsize=(10, 6))
plt.plot(step_history, reward_history, marker='o', linestyle='-', label="Cumulative Reward")
plt.xlabel("Simulation Step")
plt.ylabel("Cumulative Reward")
plt.title("DQN Training: Cumulative Reward")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(step_history, queue_history, marker='o', linestyle='-', label="Total Queue Length")
plt.xlabel("Simulation Step")
plt.ylabel("Total Queue Length")
plt.title("DQN Training: Queue Length")
plt.legend()
plt.grid(True)
plt.show()
