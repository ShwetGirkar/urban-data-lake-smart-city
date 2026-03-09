import { Link, Outlet } from "react-router-dom";
import { FaDatabase } from "react-icons/fa";
import { NavLink } from "react-router-dom";

export default function DashboardLayout() {

  return (

    <div>

      {/* NAVBAR */}

      <div className="navbar">

    <div className="navbar-inner">

      <h1 className="logo">
      <FaDatabase style={{marginRight:"10px",color:"#38bdf8"}}/>
      Urban Data Lake: Real-Time Smart City Data Platform
      </h1>

      <div className="dashboard-tabs">

      <NavLink to="/">Overview</NavLink>
      <NavLink to="/air-quality">Air Quality</NavLink>
      <NavLink to="/traffic">Traffic</NavLink>
      <NavLink to="/alerts">Alerts</NavLink>

      </div>

      </div>

      </div>

      {/* PAGE CONTENT */}

      <div className="page">

        <Outlet />

      </div>

    </div>

  );

}