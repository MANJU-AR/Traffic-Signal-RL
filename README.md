# 🚦 Traffic Signal Control using Reinforcement Learning

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)
![TensorFlow](https://img.shields.io/badge/tensorflow-2.0+-orange.svg)

> **Intelligent Traffic Management System using Deep Reinforcement Learning**

This project demonstrates **Traffic Signal Optimization** using **Reinforcement Learning (RL)** with real-time visualization through a modern **React Dashboard**. Developed as part of a **Data Science Internship at INFOTACT SOLUTION**.

![Dashboard Preview](https://via.placeholder.com/800x400/2563eb/ffffff?text=Traffic+Signal+RL+Dashboard)

## 📌 Project Overview

Traffic congestion is a major urban challenge affecting millions daily. Traditional traffic lights operate on fixed timers, often leading to unnecessary delays and inefficient traffic flow. 

This project implements a **smart traffic management system** that uses a **Reinforcement Learning agent** to dynamically optimize signal timings based on real-time traffic conditions, significantly reducing waiting times and improving overall traffic flow.

### 🎯 Key Objectives
- Reduce average vehicle waiting time at intersections
- Improve traffic throughput and flow efficiency
- Demonstrate practical application of RL in urban planning
- Provide real-time monitoring through an interactive dashboard

## ✨ Features

### 🤖 Reinforcement Learning Agent
- **Deep Q-Network (DQN)** implementation for signal control
- Real-time learning from traffic patterns
- Adaptive decision making based on queue lengths and waiting times
- Continuous improvement through experience replay

### 📊 Interactive Dashboard
- **Real-time Metrics Visualization**
  - Cumulative reward tracking
  - Queue length monitoring
  - Average waiting time analysis
  - Vehicle throughput statistics
- **Live Traffic Simulation Display**
- **Performance Analytics**
- **Responsive Design** for desktop and mobile

### 🛠️ Technical Features
- RESTful API with FastAPI for real-time data serving
- SUMO integration for realistic traffic simulation
- Modern React frontend with interactive charts
- Scalable architecture supporting multiple intersections

## ⚙️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Simulation** | SUMO (Simulation of Urban MObility) |
| **RL Framework** | TensorFlow / Keras |
| **Backend API** | FastAPI |
| **Frontend** | React + Recharts |
| **Database** | MongoDB (optional) |
| **Language** | Python 3.8+ |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ and npm
- SUMO traffic simulator
- Git

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/MANJU-AR/Traffic-Signal-RL.git
cd Traffic-Signal-RL
```

### 2️⃣ Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload
```
The backend will be available at `http://127.0.0.1:8000`

### 3️⃣ Frontend Setup
```bash
# Navigate to dashboard directory
cd dashboard

# Install React dependencies
npm install

# Start the development server
npm start
```
The dashboard will open at `http://localhost:3000`

### 4️⃣ Run SUMO Simulation
```bash
# Make sure SUMO is installed and in your PATH
sumo-gui -c SUMO-files/intersection.sumocfg
```

## 📂 Project Structure

```
📦 Traffic-Signal-RL/
┣ 📁 dashboard/                 # React frontend application
┃ ┣ 📁 src/
┃ ┃ ┣ 📜 Dashboard.jsx         # Main dashboard component
┃ ┃ ┣ 📜 App.js               # App entry point
┃ ┃ ┣ 📜 App.css              # Styling
┃ ┃ ┗ 📜 index.js             # React DOM render
┃ ┣ 📜 package.json           # Dependencies
┃ ┗ 📜 public/                # Static assets
┣ 📁 SUMO-files/               # Traffic simulation config
┃ ┣ 📜 intersection.sumocfg    # SUMO configuration
┃ ┣ 📜 network.net.xml        # Road network definition
┃ ┗ 📜 routes.rou.xml         # Vehicle routes
┣ 📁 models/                   # Trained RL models
┣ 📁 logs/                     # Training logs and metrics
┣ 📜 main.py                   # FastAPI backend learning agent
┣ 📜 traffic_env.py           # SUMO environment wrapper
┣ 📜 requirements.txt         # Python dependencies
┣ 📜 README.md                # Project documentation
┗ 📜 .gitignore               # Git ignore rules
```

## 🔬 How It Works

### 1. Traffic Simulation
- **SUMO** creates realistic traffic scenarios with vehicles, routes, and intersections
- Real-time traffic data (queue lengths, waiting times) is extracted

### 2. RL Agent Training
- **State**: Current traffic conditions (queue lengths, waiting times, signal phases)
- **Actions**: Signal phase changes (North-South green, East-West green, etc.)
- **Rewards**: Based on reduced waiting times and improved throughput
- **Learning**: Deep Q-Network learns optimal policies through trial and error

### 3. Real-time Optimization
- Trained agent makes decisions every few seconds
- Signal timings adapt to current traffic conditions
- Performance metrics are continuously monitored

## 📈 Performance Metrics

The system tracks several key performance indicators:

- **Average Waiting Time**: Time vehicles spend waiting at signals
- **Queue Length**: Number of vehicles waiting per lane
- **Throughput**: Vehicles successfully passing through per hour
- **Cumulative Reward**: RL agent's learning progress
- **Fuel Consumption**: Environmental impact estimation

## 🛣️ Future Enhancements

- [ ] Multi-intersection coordination
- [ ] Integration with real traffic cameras
- [ ] Weather condition adaptation
- [ ] Mobile app for traffic updates
- [ ] Integration with city traffic management systems
- [ ] Advanced RL algorithms (A3C, PPO)


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- **SUMO Development Team** for the excellent open-source traffic simulation platform
- **TensorFlow/Keras Team** for powerful machine learning frameworks
- **FastAPI** and **React** communities for robust development tools

## 👨‍💻 About the Developer

**Manju A R**  
Data Science Intern | AI Enthusiast | Traffic Optimization Researcher

🔗 **Connect with me:**
- [LinkedIn](https://www.linkedin.com/in/manju-a-r-624466255)
- [GitHub](https://github.com/MANJU-AR)


**⭐ If you found this project helpful, please give it a star!**

#DataScience #ReinforcementLearning #TrafficManagement #MachineLearning #Python #React #AI #SmartCities