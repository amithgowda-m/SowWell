import React, { useState } from "react";
import axios from "axios";

const DiseaseDetection: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setFile(e.target.files[0]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post("/api/predict-disease/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    setResult(res.data);
  };

  return (
    <div className="max-w-xl mx-auto bg-white shadow-lg rounded-lg p-8 mt-8">
      <h2 className="text-2xl font-bold mb-6 text-green-700">Disease Detection</h2>
      <form className="space-y-4" onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleFileChange} required className="w-full" />
        <button className="w-full bg-green-600 text-white rounded py-2 hover:bg-green-700 transition" type="submit">Detect</button>
      </form>
      {result && (
        <div className="mt-8 bg-green-50 p-4 rounded">
          <h3 className="text-xl font-semibold mb-2">Disease: <span className="text-green-800">{result.disease}</span></h3>
          <h4 className="font-semibold">Prevention Steps:</h4>
          <ul className="list-disc list-inside">
            {result.prevention_steps.map((step: string, idx: number) => (
              <li key={idx}>{step}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DiseaseDetection;
