import { useEffect, useState } from "react";
import { fetchAlerts } from "../api/alertsApi";
import KpiCards from "../components/kpi/KpiCards";
import { GoAlertFill } from "react-icons/go";

export default function Alerts() {

  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    const data = await fetchAlerts();
    setAlerts(data.alerts);
  };

  const levelColor = (level) => {
    if (level === "High") return "#dc3545";
    if (level === "Medium") return "#fd7e14";
    return "#ffc107";
  };

  return (
     
    <div style={{ padding: "20px" }}>
      <h2 className="logo"><GoAlertFill style={{marginRight:"10px",color:"#38bdf8"}}/>Active Alerts </h2>
        <KpiCards/>
      <table
        style={{
          width: "100%",
          marginTop: "20px",
          borderCollapse: "collapse"
        }}
      >

        <thead>
          <tr style={{ background: "var(--bg-panel)" }}>
            <th>No.</th>
            <th>Level</th>
            <th>Type</th>
            <th>City</th>
            <th>Message</th>
            <th>Time</th>
          </tr>
        </thead>

        <tbody>

          {alerts.map((alert, index) => (

            <tr key={index} style={{ borderBottom: "1px solid #e5e7eb" }}>

              <td>{index + 1}</td>

              <td>

                <span
                  style={{
                    background: levelColor(alert.level),
                    color: "white",
                    padding: "3px 8px",
                    borderRadius: "6px",
                    fontSize: "12px"
                  }}
                >
                  {alert.level}
                </span>

              </td>

              <td>{alert.type}</td>

              <td>{alert.city}</td>

              <td>{alert.message}</td>

              <td>
                {new Date(alert.time).toLocaleTimeString()}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );

}