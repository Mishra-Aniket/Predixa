import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

// ✅ Use environment variable (Vercel-friendly)
const API_BASE = import.meta.env.VITE_API_URL;

function App() {
  const [days, setDays] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  // Fetch prediction history
  const fetchHistory = async () => {
    try {
      const res = await axios.get(`${API_BASE}/history/`);
      setHistory(res.data);
    } catch (err) {
      console.warn("History fetch failed");
    }
  };

  // Predict price
  const predictPrice = async () => {
    if (!days) return;

    setError("");
    try {
      const res = await axios.get(`${API_BASE}/predict/`, {
        params: { days: Number(days) },
      });

      setResult(res.data);
      fetchHistory();
    } catch (err) {
      console.error(
        "Prediction error:",
        err.response?.data || err.message
      );
      setError(err.response?.data?.error || "Prediction failed");
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="container">
      <h1>📈 Predixa Dashboard</h1>

      <div className="card">
        <input
          type="number"
          placeholder="Days ahead"
          value={days}
          onChange={(e) => setDays(e.target.value)}
        />
        <button onClick={predictPrice}>Predict</button>
      </div>

      {result && (
        <p className="result">
          Predicted Price: ₹{result.predicted_price}
        </p>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Prediction History</h2>

      <table>
        <thead>
          <tr>
            <th>Days</th>
            <th>Price</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {history.map((item) => (
            <tr key={item.id}>
              <td>{item.days_ahead}</td>
              <td>₹{item.predicted_price.toFixed(2)}</td>
              <td>{new Date(item.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* 📊 CHART */}
      {history.length > 0 && (
        <>
          <h2>Price Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={[...history].reverse()}>
              <XAxis dataKey="created_at" tickFormatter={(v) =>
                new Date(v).toLocaleTimeString()
              } />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="predicted_price"
                stroke="#2563eb"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </>
      )}
    </div>
  );
}

export default App;
