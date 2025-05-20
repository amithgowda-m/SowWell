import React, { useState } from "react";
import axios from "axios";

const CropRecommendation: React.FC = () => {
  const [form, setForm] = useState({
    temperature: "",
    humidity: "",
    moisture: "",
    soil_type: "",
    n: "",
    p: "",
    k: "",
  });
  const [result, setResult] = useState<any>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await axios.post("/api/recommend-crop/", {
      ...form,
      temperature: parseFloat(form.temperature),
      humidity: parseFloat(form.humidity),
      moisture: parseFloat(form.moisture),
      n: parseFloat(form.n),
      p: parseFloat(form.p),
      k: parseFloat(form.k),
    });
    setResult(res.data);
  };

  return (
    <div className="max-w-xl mx-auto bg-white shadow-lg rounded-lg p-8 mt-8">
      <h2 className="text-2xl font-bold mb-6 text-green-700">Crop & Fertilizer Recommendation</h2>
      <form className="space-y-4" onSubmit={handleSubmit}>
        <input className="w-full border rounded px-3 py-2" name="temperature" placeholder="Temperature" value={form.temperature} onChange={handleChange} required />
        <input className="w-full border rounded px-3 py-2" name="humidity" placeholder="Humidity" value={form.humidity} onChange={handleChange} required />
        <input className="w-full border rounded px-3 py-2" name="moisture" placeholder="Moisture" value={form.moisture} onChange={handleChange} required />
        <select className="w-full border rounded px-3 py-2" name="soil_type" value={form.soil_type} onChange={handleChange} required>
          <option value="">Select Soil Type</option>
          <option value="Sandy">Sandy</option>
          <option value="Clay">Clay</option>
          <option value="Loamy">Loamy</option>
        </select>
        <input className="w-full border rounded px-3 py-2" name="n" placeholder="Nitrogen (N)" value={form.n} onChange={handleChange} required />
        <input className="w-full border rounded px-3 py-2" name="p" placeholder="Phosphorus (P)" value={form.p} onChange={handleChange} required />
        <input className="w-full border rounded px-3 py-2" name="k" placeholder="Potassium (K)" value={form.k} onChange={handleChange} required />
        <button className="w-full bg-green-600 text-white rounded py-2 hover:bg-green-700 transition" type="submit">Recommend</button>
      </form>
      {result && (
        <div className="mt-8 bg-green-50 p-4 rounded">
          <h3 className="text-xl font-semibold mb-2">Recommended Crop: <span className="text-green-800">{result.crop}</span></h3>
          <h4 className="font-semibold">Fertilizer: <span className="text-green-700">{result.fertilizer}</span></h4>
          <p className="mb-2">{result.why_fertilizer}</p>
          <h4 className="font-semibold">Lifecycle Steps:</h4>
          <ol className="list-decimal list-inside">
            {result.lifecycle.map((step: string, idx: number) => (
              <li key={idx}>{step}</li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
};

export default CropRecommendation;
