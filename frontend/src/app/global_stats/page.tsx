'use client';
import { useEffect, useState } from 'react';

export default function StatisticsPage() {
  const [data, setData] = useState<unknown>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const get_stats = async () => {
      try {
        const response = await fetch(
          encodeURI(`/proxy/statistics`)
        );
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setData(data);
      } catch (error) {
        console.error(error);
        setError('Błąd podczas pobierania statystyk');
      }
    };

    get_stats();
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400 text-black">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-xl">
        <h1 className="text-3xl font-bold text-blue-900 mb-4 text-center">
          Statystyki globalne
        </h1>
        {error && <div className="text-red-600 mb-4">{error}</div>}
        <pre className="bg-gray-100 rounded p-4 text-sm overflow-x-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    </div>
  );
}
