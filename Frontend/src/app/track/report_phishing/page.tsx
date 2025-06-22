"use client";
import { useEffect, useState } from "react";
import { trackReportPhishing } from "@/lib/api";

export default function TrackReportPhishingPage() {
  const [imgUrl, setImgUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    trackReportPhishing()
      .then(res => {
        const blob = new Blob([res.data], { type: "image/png" });
        setImgUrl(URL.createObjectURL(blob));
      })
      .catch(err => setError(err.message));
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-xl flex flex-col items-center">
        <h1 className="text-3xl font-bold text-blue-900 mb-4 text-center">Track Report Phishing</h1>
        {error && <div className="text-red-600 mb-4">{error}</div>}
        {imgUrl && <img src={imgUrl} alt="Track Report Phishing" className="rounded shadow max-w-xs" />}
      </div>
    </div>
  );
}