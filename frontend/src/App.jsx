import { BrowserRouter, Routes, Route } from "react-router-dom";
import Overview from "./pages/Overview";
import AirQuality from "./pages/AirQuality";
import Traffic from "./pages/Traffic";
import Alerts from "./pages/Alerts";
import DashboardLayout from "./layouts/DashboardLayout";

function App() {
  return (
    <BrowserRouter>
      <DashboardLayout>
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/air-quality" element={<AirQuality />} />
          <Route path="/traffic" element={<Traffic />} />
          <Route path="/alerts" element={<Alerts />} />
        </Routes>
      </DashboardLayout>
    </BrowserRouter>
  );
}

export default App;