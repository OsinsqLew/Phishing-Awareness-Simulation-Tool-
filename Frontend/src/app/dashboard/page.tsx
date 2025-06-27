"use client";
import { useState } from "react";
import axios from "axios";

export default function TrackReportPhishingPage() {
  const [reference, setReference] = useState("");
  const [imgUrl, setImgUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setImgUrl(null);
    try {
      const res = await axios.get(
        process.env.NEXT_PUBLIC_API_URL + "/track/report_phising.png",
        {
          params: { reference },
          responseType: "blob",
        }
      );
      setImgUrl(URL.createObjectURL(res.data));
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400">
      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-md flex flex-col gap-4 items-center"
      >
        <h1 className="text-3xl font-bold text-blue-900 mb-4 text-center">
          Tracking obrazka
        </h1>
        <input
          name="reference"
          placeholder="Reference"
          className="input"
          value={reference}
          onChange={(e) => setReference(e.target.value)}
          required
        />
        <button
          type="submit"
          className="bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 rounded-lg transition"
        >
          Pobierz obrazek
        </button>
        {imgUrl && (
          <img
            src={imgUrl}
            alt="Track Report Phishing"
            className="rounded shadow max-w-xs mt-4"
          />
        )}
        {error && <div className="text-red-600 mt-2">{error}</div>}
      </form>
    </div>
  );
}