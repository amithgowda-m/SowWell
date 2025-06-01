// frontend/src/pages/WelcomePage.tsx

import React from "react";
import { Link } from "react-router-dom";

const WelcomePage: React.FC = () => {
  return (
    <div className="text-center py-10">
      <h1 className="text-4xl font-bold text-green-700 mb-6">🌱 Welcome to SowWell</h1>
      <p className="text-xl text-gray-700 mb-10">
        A Smart Agriculture Platform for Scientific Farming Guidance
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
        <Link
          to="/recommendation"
          className="bg-green-100 p-6 rounded-lg shadow-md hover:shadow-lg border border-green-200 transition transform hover:scale-105"
        >
          <h2 className="text-2xl font-semibold text-green-800 mb-2">🌾 Crop Recommendation</h2>
          <p className="text-gray-600">
            Get personalized crop suggestions based on soil and climate.
          </p>
        </Link>

        <Link
          to="/disease"
          className="bg-green-100 p-6 rounded-lg shadow-md hover:shadow-lg border border-green-200 transition transform hover:scale-105"
        >
          <h2 className="text-2xl font-semibold text-green-800 mb-2">🔍 Plant Disease Detection</h2>
          <p className="text-gray-600">
            Upload an image and get real-time disease detection and prevention steps.
          </p>
        </Link>

        <Link
          to="/weather"
          className="bg-green-100 p-6 rounded-lg shadow-md hover:shadow-lg border border-green-200 transition transform hover:scale-105"
        >
          <h2 className="text-2xl font-semibold text-green-800 mb-2">🌤️ Weather Forecast</h2>
          <p className="text-gray-600">
            Check local weather before irrigation, pesticide application, or harvesting.
          </p>
        </Link>
      </div>
    </div>
  );
};

export default WelcomePage;