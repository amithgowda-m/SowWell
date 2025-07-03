import React, { useState } from "react";
import axios from "axios";

interface PredictionResult {
  disease: string;
  confidence: number;
  prevention_steps: string[];
}

const DiseaseDetection: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [language, setLanguage] = useState<string>("en"); // 👈 Language state

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleSubmit = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setPrediction(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        `http://localhost:8000/api/disease/predict?lang=${language}`, // 👈 Add language param
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setPrediction(response.data as PredictionResult);
    } catch (err: any) {
      console.error("Error predicting disease:", err);
      setError(
        err.response?.data?.detail ||
        "Failed to get prediction. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6 bg-white rounded shadow-md mt-6">
      <h2 className="text-2xl font-semibold mb-4">Plant Disease Detection</h2>
      <p className="mb-4 text-gray-600">
        Upload a plant image to detect possible diseases and get prevention suggestions.
      </p>

      {/* Language Selector */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Select Language:
        </label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="w-full border rounded px-3 py-2"
        >
          <option value="en">English</option>
          <option value="kn">Kannada</option>
        </select>
      </div>

      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        disabled={loading}
        className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
      />

      <button
        onClick={handleSubmit}
        disabled={!file || loading}
        className={`mt-4 w-full px-4 py-2 rounded text-white ${
          !file || loading ? "bg-gray-400 cursor-not-allowed" : "bg-green-600 hover:bg-green-700"
        }`}
      >
        {loading ? "Predicting..." : "Detect Disease"}
      </button>

      {loading && <p className="mt-4 text-blue-600">Analyzing image...</p>}
      {error && <p className="mt-4 text-red-600">{error}</p>}

      {prediction && (
        <div className="mt-6 bg-green-50 p-4 border border-green-200 rounded">
          <h3 className="text-xl font-bold mb-2 text-green-800">
            Predicted Disease: {prediction.disease}
          </h3>
          <p>
            <strong>Confidence:</strong> {(prediction.confidence * 100).toFixed(2)}%
          </p>
          <h4 className="font-semibold mt-4">Prevention Steps:</h4>
          <ul className="list-disc ml-5">
            {prediction.prevention_steps.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DiseaseDetection;