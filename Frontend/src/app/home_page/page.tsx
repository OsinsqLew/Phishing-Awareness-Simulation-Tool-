"use client";
import { useState } from "react";
import axios from "axios";

export default function HomePage() {
  const [reference, setReference] = useState("");
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    try {
      const res = await axios.get(
        process.env.NEXT_PUBLIC_API_URL + "/home_page",
        { params: { reference } }
      );
      setResult(res.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400">
      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-md flex flex-col gap-4"
      >
        <h1 className="text-3xl font-bold text-blue-900 mb-4 text-center">
          Kliknięcie w phishing
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
          Wyślij
        </button>
        {result && (
          <pre className="bg-green-100 rounded p-2 mt-2">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
        {error && <div className="text-red-600 mt-2">{error}</div>}
      </form>
    </div>
  );
}