import { useEffect, useState } from "react";
import { fetchSummary } from "../../api/summaryApi";

import { FaSmog } from "react-icons/fa";
import { FaTrafficLight } from "react-icons/fa";
import { WiDaySunny } from "react-icons/wi";
import { FaExclamationTriangle } from "react-icons/fa";
import { FaClock } from "react-icons/fa";
export default function KpiCards() {

  const [summary, setSummary] = useState(null);

  useEffect(() => {
    const loadSummary = async () => {
      const data = await fetchSummary();
      setSummary(data);
    };

    loadSummary();
  }, []);

  if (!summary) return <p>Loading dashboard...</p>;

    return (
    <div className="kpi-container">

        <div className="kpi-card">
        <div className="kpi-header">
            <span className="kpi-title">Avg AQI</span>
            <FaSmog className="kpi-icon"/>
        </div>
        <div className="kpi-value">{summary.avg_aqi.toFixed(2)}</div>
        <div className="kpi-tag moderate">Moderate</div>
        </div>

        <div className="kpi-card">
        <div className="kpi-header">
            <span className="kpi-title">Congestion</span>
            <FaTrafficLight className="kpi-icon"/>
        </div>
        <div className="kpi-value">{(summary.avg_congestion * 100).toFixed(0)}%</div>
        <div className="kpi-sub">City-wide</div>
        </div>

        <div className="kpi-card">
        <div className="kpi-header">
            <span className="kpi-title">Weather</span>
            <WiDaySunny className="kpi-icon"/>
        </div>
        <div className="kpi-value">{summary.avg_temperature}°C</div>
        <div className="kpi-sub">Average</div>
        </div>

        <div className="kpi-card">
        <div className="kpi-header">
            <span className="kpi-title">Worst Zone</span>
            <FaExclamationTriangle className="kpi-icon"/>
        </div>
        <div className="kpi-value">{summary.worst_city}</div>
        <div className="kpi-sub">Highest Stress</div>
        </div>

        <div className="kpi-card">
        <div className="kpi-header">
         <span className="kpi-title">Last Updated</span>
            <FaClock className="kpi-icon"/>
        </div>
        <div className="kpi-value">
         {new Date(summary.last_updated).toLocaleTimeString()}
        </div>
        <div className="kpi-sub">System Time</div>
        </div>

    </div>
    );
}