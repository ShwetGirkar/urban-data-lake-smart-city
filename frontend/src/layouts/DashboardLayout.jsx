export default function DashboardLayout({ children }) {
  return (
    <div style={{ padding: "20px" }}>
      <h2>Urban Data Lake: Real Time Smart City Data Platform</h2>

      <nav style={{ marginBottom: "20px" }}>
        <a href="/">Overview</a> |{" "}
        <a href="/air-quality">Air Quality</a> |{" "}
        <a href="/traffic">Traffic</a> |{" "}
        <a href="/alerts">Alerts</a>
      </nav>

      {children}
    </div>
  );
}