// frontend/src/pages/WeatherDashboard.tsx

import React, { useState } from 'react';

interface WeatherData {
  temperature: number;
  humidity: number;
  rainfall?: number | null;
  description: string;
  timestamp?: string;
}

const WeatherDashboard: React.FC = () => {
  const [location, setLocation] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);

  const handleSearch = async () => {
    if (!location.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/api/weather/forecast?place=${encodeURIComponent(location)}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch weather data');
      }

      const data = await response.json();
      setWeatherData(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-green-700 mb-6"> Weather Forecast for Farmers</h1>

      <div className="mb-6 flex space-x-2">
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Enter crop field name or location"
          className="flex-grow p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="bg-green-700 hover:bg-green-800 text-white px-6 py-3 rounded-md transition disabled:opacity-50"
        >
          {loading ? 'Loading...' : 'Get Weather'}
        </button>
      </div>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      {weatherData && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
          {/* Temperature Card */}
          <div className="bg-blue-50 p-4 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold text-blue-700">🌡️ Temperature</h2>
            <p className="text-3xl font-bold mt-2">{weatherData.temperature}°C</p>
            <p className="text-sm text-gray-600 mt-1">Updated: {new Date().toLocaleString()}</p>
          </div>

          {/* Humidity Card */}
          <div className="bg-teal-50 p-4 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold text-teal-700">💧 Humidity</h2>
            <p className="text-3xl font-bold mt-2">{weatherData.humidity}%</p>
          </div>

          {/* Rainfall Card */}
          <div className="bg-indigo-50 p-4 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold text-indigo-700">🌧️ Rainfall (mm)</h2>
            <p className="text-3xl font-bold mt-2">{weatherData.rainfall ?? 'N/A'}</p>
          </div>

          {/* Conditions Card */}
          <div className="bg-yellow-50 p-4 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold text-yellow-700">📝 Conditions</h2>
            <p className="text-2xl font-medium mt-2">{weatherData.description}</p>
          </div>
        </div>
      )}

      {!weatherData && !loading && (
        <div className="mt-6 text-center text-gray-500">
          Enter a location and click "Get Weather" to view current conditions.
        </div>
      )}
    </div>
  );
};

export default WeatherDashboard;