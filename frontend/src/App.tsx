import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import CropRecommendation from "./pages/CropRecommendation";
import DiseaseDetection from "./pages/DiseaseDetection";

const App: React.FC = () => (
  <Router>
    <nav className="bg-green-700 p-4 flex justify-between items-center">
      <div className="text-white text-xl font-bold">SowWell- A Scientific farming guidance platform</div>
      <div className="space-x-4">
        <Link to="/" className="text-white hover:underline">Crop Recommendation</Link>
        <Link to="/disease" className="text-white hover:underline">Disease Detection</Link>
      </div>
    </nav>
    <main className="container mx-auto p-4">
      <Routes>
        <Route path="/" element={<CropRecommendation />} />
        <Route path="/disease" element={<DiseaseDetection />} />
      </Routes>
    </main>
  </Router>
);

export default App;
