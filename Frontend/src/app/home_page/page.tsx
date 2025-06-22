"use client";
import { useEffect, useState } from "react";
import { getHomePage } from "@/lib/api";

export default function HomePage() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  
  const token = "FAKE_TOKEN";

  useEffect(() => {
    getHomePage(token)
      .then(res => setData(res.data))
      .catch(err => setError(err.message));
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-xl">
        <h1 className="text-3xl font-bold text-blue-900 mb-4 text-center">Home Page (Email Clicked)</h1>
        {error && <div className="text-red-600 mb-4">{error}</div>}
        <pre className="bg-gray-100 rounded p-4 text-sm overflow-x-auto">{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  );
}