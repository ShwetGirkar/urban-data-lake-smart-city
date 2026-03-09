import KpiCards from "../components/kpi/KpiCards";
import CityMap from "../components/map/CityMap";
import UrbanStressPanel from "../components/panels/UrbanStressPanel";
import CityZones from "../components/zones/CityZones";
import { RiDashboardFill } from "react-icons/ri";

export default function Overview() {

  return (
    <div>

      <h2 className="logo"><RiDashboardFill style={{marginRight:"10px",color:"#38bdf8"}}/>Smart City Dashboard</h2>

      {/* KPI Cards */}
      <KpiCards />

      {/* Panel + Map Row */}
      <div className="overview-grid">

      <div className="stress-panel">
      <UrbanStressPanel />
      </div>

      <div className="map-panel">
      <CityMap />
      </div>

      </div>
      <CityZones/>

    </div>
  );
}