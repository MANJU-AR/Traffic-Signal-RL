import React, { useEffect, useState } from "react";
import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

function Dashboard() {
  const [data, setData] = useState({
    q_EB: [0, 0, 0],
    q_SB: [0, 0, 0],
    current_phase: 0,
    total_queue: 0,
    cumulative_reward: 0
  });

  const [history, setHistory] = useState([]);
  const MAX_POINTS = 50;

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://127.0.0.1:8000/status")
        .then((res) => res.json())
        .then((json) => {
          setData(json);

          setHistory((prev) => {
            const newPoint = {
              step: prev.length > 0 ? prev[prev.length - 1].step + 1 : 0,
              total_queue: json.total_queue,
              cumulative_reward: json.cumulative_reward
            };
            return [...prev, newPoint].slice(-MAX_POINTS);
          });
        })
        .catch((err) => console.error(err));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>🚦 Smart Traffic Dashboard</h2>

      {/* Phase Indicator */}
      <div className="phase-indicator">
        <span
          className={`light eb ${data.current_phase === 0 ? "green" : ""}`}
        ></span>
        <span
          className={`light sb ${data.current_phase === 1 ? "green" : ""}`}
        ></span>
      </div>

      {/* Stats */}
      <div className="stats-card">
        <p>
          <strong>Current Phase:</strong> {data.current_phase}
        </p>
        <p>
          <strong>Total Queue:</strong> {data.total_queue}
        </p>
        <p>
          <strong>Cumulative Reward:</strong>{" "}
          {data.cumulative_reward.toFixed(2)}
        </p>
      </div>

      {/* Lane Queues */}
      <ul className="lane-queues">
        <li className="eb">EB: {data.q_EB.join(", ")}</li>
        <li className="sb">SB: {data.q_SB.join(", ")}</li>
      </ul>

      {/* Mixed Chart */}
      <h3>Graph</h3>
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={history}>
          <CartesianGrid stroke="#f5f5f5" />
          <XAxis dataKey="step" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="total_queue" barSize={30} fill="#8884d8" name="Total Queue" />
          <Line
            type="monotone"
            dataKey="cumulative_reward"
            stroke="#82ca9d"
            name="Cumulative Reward"
            strokeWidth={2}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}

export default Dashboard;
