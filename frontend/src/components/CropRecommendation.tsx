import React, { useState } from "react";
import { recommendCrop } from "../utils/api";

export default function CropRecommendation() {
  const [soilType, setSoilType] = useState("");
  const [fertilizerName, setFertilizerName] = useState("");
  // Add other input states as needed
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<null | {
    recommended_crop: string;
    crop_lifecycle: string[];
  }>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit() {
    if (!soilType || !fertilizerName) {
      setError("Please fill all required fields.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await recommendCrop({ soilType, fertilizerName });
      setResult(res);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl mx-auto p-6 bg-white rounded shadow-md mt-6">
      <h2 className="text-2xl font-semibold mb-4">Crop Recommendation</h2>

      <label className="block mb-2 font-medium">Soil Type</label>
      <input
        type="text"
        value={soilType}
        onChange={(e) => setSoilType(e.target.value)}
        className="w-full p-2 border rounded mb-4"
        placeholder="Enter soil type"
      />

      <label className="block mb-2 font-medium">Fertilizer Name</label>
      <input
        type="text"
        value={fertilizerName}
        onChange={(e) => setFertilizerName(e.target.value)}
        className="w-full p-2 border rounded mb-4"
        placeholder="Enter fertilizer name"
      />

      {/* Add more inputs here */}

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Fetching..." : "Get Recommendation"}
      </button>

      {error && (
        <p className="mt-4 text-red-600 font-medium">{error}</p>
      )}

      {result && (
        <div className="mt-6 bg-blue-50 p-4 rounded border border-blue-200">
          <h3 className="text-xl font-bold mb-2">
            Recommended Crop: {result.recommended_crop}
          </h3>
          <strong>Crop Lifecycle Steps:</strong>
          <ol className="list-decimal list-inside ml-4 mt-1">
            {result.crop_lifecycle.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}
