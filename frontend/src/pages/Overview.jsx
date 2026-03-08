import KpiCards from "../components/kpi/KpiCards";
import CityMap from "../components/map/CityMap";
import UrbanStressPanel from "../components/panels/UrbanStressPanel";
import CityZones from "../components/zones/CityZones";

export default function Overview() {

  return (
    <div>

      <h1>Smart City Dashboard</h1>

      {/* KPI Cards */}
      <KpiCards />

      {/* Panel + Map Row */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "320px 1fr",
          gap: "20px",
          marginTop: "20px"
        }}
      >

        <UrbanStressPanel />

        <CityMap />

      </div>
      <CityZones/>

      <p>Overview Page</p>

    </div>
  );
}