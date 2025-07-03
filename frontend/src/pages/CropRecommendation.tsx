import React, { useState } from "react";
import axios from "axios";

export default function CropRecommendation() {
  const [form, setForm] = useState({
    temperature: "",
    humidity: "",
    moisture: "",
    soilType: "",
    n: "",
    p: "",
    k: "",
    rainfall: ""
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<{
    recommended_crop: string;
    fertilizer: string;
    lifecycle: string[];
    why_fertilizer: string;
  } | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError(null);
      setResult(null); // Reset previous result to avoid stale data

      interface ApiResponse {
        error?: string;
        recommended_crop?: string;
        fertilizer?: string;
        lifecycle?: string[];
        why_fertilizer?: string;
      }

      const res = await axios.post<ApiResponse>(
        "http://localhost:8000/api/crops/recommend-crop",
        {
          temperature: parseFloat(form.temperature),
          humidity: parseFloat(form.humidity),
          moisture: parseFloat(form.moisture),
          soil_type: form.soilType, // Note: Backend expects "soil_type", not "soilType"
          n: parseFloat(form.n),
          p: parseFloat(form.p),
          k: parseFloat(form.k),
          rainfall: parseFloat(form.rainfall)
        }
      );

      console.log("API Response:", res.data); // Debug line to check response in browser console

      // Validate and set result
      const data = res.data;
      if (data.error) {
        setError(data.error);
        setResult(null);
      } else {
        setResult({
          recommended_crop: data.recommended_crop || "Unknown Crop",
          fertilizer: data.fertilizer || "Unknown Fertilizer",
          lifecycle: Array.isArray(data.lifecycle) ? data.lifecycle : [],
          why_fertilizer: data.why_fertilizer || "No reason provided."
        });
      }
    } catch (err: any) {
      console.error("Axios Error:", err); // Debug line for network or other errors
      setError(err.response?.data?.error || "An error occurred while fetching the recommendation.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6 bg-white rounded shadow-md mt-6">
      <h2 className="text-2xl font-semibold mb-4">Crop Recommendation</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Input fields */}
        <input
          name="temperature"
          placeholder="Temperature"
          value={form.temperature}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border rounded"
        />
        <input
          name="humidity"
          placeholder="Humidity"
          value={form.humidity}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border rounded"
        />
        <input
          name="moisture"
          placeholder="Moisture"
          value={form.moisture}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border rounded"
        />
        <select
          name="soilType"
          value={form.soilType}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border rounded"
        >
          <option value="">Select Soil Type</option>
          <option value="Sandy">Sandy</option>
          <option value="Loamy">Loamy</option>
          <option value="Clay">Clay</option>
        </select>
        <input
          name="n"
          placeholder="Nitrogen (N)"
          value={form.n}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border rounded"
        />
        <input
          name="p"
          placeholder="Phosphorus (P)"
          value={form.p}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border rounded"
        />
        <input
          name="k"
          placeholder="Potassium (K)"
          value={form.k}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border rounded"
        />
        <input
          name="rainfall"
          placeholder="Rainfall (mm)"
          value={form.rainfall}
          onChange={handleChange}
          required
          className="w-full px-3 py-2 border rounded"
        />

        <button
          type="submit"
          disabled={loading}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 w-full"
        >
          {loading ? "Fetching..." : "Get Recommendation"}
        </button>
      </form>

      {error && <p className="mt-4 text-red-600">{error}</p>}

      {result && (
        <div className="mt-6 bg-green-50 p-4 border border-green-200 rounded">
          <h3 className="text-xl font-bold mb-2">
            Recommended Crop:{" "}
            <span className="text-green-800">{result.recommended_crop}</span>
          </h3>
          <p>
            <strong>Fertilizer:</strong> {result.fertilizer}
          </p>
          <p>{result.why_fertilizer}</p>
          <h4 className="font-semibold mt-4">Lifecycle Steps:</h4>
          <ul className="list-disc ml-5">
            {result.lifecycle && result.lifecycle.length > 0 ? (
              result.lifecycle.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))
            ) : (
              <li>No lifecycle steps available.</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}