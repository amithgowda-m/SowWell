// App.tsx

import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import WelcomePage from "./pages/WelcomePage";
import WeatherDashboard from "./pages/WeatherDashboard";
import CropRecommendation from "./pages/CropRecommendation";
import DiseaseDetection from "./pages/DiseaseDetection";

const App: React.FC = () => {
  return (
    <Router
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <nav className="bg-green-700 p-4 flex justify-between items-center">
        <div className="text-white text-xl font-bold">
          SowWell - A Scientific Farming Guidance Platform
        </div>
        <div className="space-x-4">
          <Link to="/" className="text-white hover:underline">
            Home
          </Link>
          <Link to="/recommendation" className="text-white hover:underline">
            Crop Recommendation
          </Link>
          <Link to="/disease" className="text-white hover:underline">
            Disease Detection
          </Link>
        </div>
      </nav>

      <main className="container mx-auto p-4">
        <Routes>
          <Route path="/" element={<WelcomePage />} />
          <Route path="/recommendation" element={<CropRecommendation />} />
          <Route path="/disease" element={<DiseaseDetection />} />
           <Route path="/weather" element={<WeatherDashboard />} />
        </Routes>
      </main>
    </Router>
  );
};

export default App;