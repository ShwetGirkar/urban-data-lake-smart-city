import { BrowserRouter, Routes, Route } from "react-router-dom";

import Overview from "./pages/Overview";
import AirQuality from "./pages/AirQuality";
import Traffic from "./pages/Traffic";
import Alerts from "./pages/Alerts";

import DashboardLayout from "./layouts/DashboardLayout";

import "./styles/global.css";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route element={<DashboardLayout />}>

          <Route path="/" element={<Overview />} />
          <Route path="/air-quality" element={<AirQuality />} />
          <Route path="/traffic" element={<Traffic />} />
          <Route path="/alerts" element={<Alerts />} />

        </Route>

      </Routes>

    </BrowserRouter>

  );

}

export default App;