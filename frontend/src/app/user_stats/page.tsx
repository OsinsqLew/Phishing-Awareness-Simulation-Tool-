'use client';
import { useEffect, useState } from 'react';
import { useGlobalContext } from '../global-context';

export default function UserStatisticsPage() {
  const { state } = useGlobalContext();
  const { session } = state;
  const [data, setData] = useState<{
    statisctics: {
      email_id: number;
      user_id: number;
      seen: number;
      clicked: number;
      tags: string;
      phishing_type: string;
    }[];
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (session) {
      const get_stats = async () => {
        try {
          const response = await fetch(
            encodeURI(
              `/proxy/user_statistics?user_id=${session.user_id}&token=${session.token}`
            )
          );
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          const data = await response.json();
          setData(data);
        } catch (error) {
          console.error(error);
          setError('Błąd podczas pobierania statystyk użytkownika');
        }
      };

      get_stats();
    }
  }, [session]);

  if (!session) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white text-xl">
        Musisz być zalogowany, aby zobaczyć statystyki użytkownika.
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400 text-black">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-xl">
        <h1 className="text-3xl font-bold text-blue-900 mb-4 text-center">
          Statystyki użytkownika
        </h1>
        {error && <div className="text-red-600 mb-4">{error}</div>}
        {data && data.statisctics && Array.isArray(data.statisctics) ? (
          <table className="w-full text-sm bg-gray-100 rounded">
            <thead>
              <tr>
                <th className="px-2 py-1 text-left">Email ID</th>
                <th className="px-2 py-1 text-left">User ID</th>
                <th className="px-2 py-1 text-left">Seen</th>
                <th className="px-2 py-1 text-left">Clicked</th>
                <th className="px-2 py-1 text-left">Tagi</th>
                <th className="px-2 py-1 text-left">Typ phishingu</th>
              </tr>
            </thead>
            <tbody>
              {data.statisctics.map((stat, idx: number) => (
                <tr key={idx}>
                  <td className="px-2 py-1">{stat.email_id}</td>
                  <td className="px-2 py-1">{stat.user_id}</td>
                  <td className="px-2 py-1">{stat.seen}</td>
                  <td className="px-2 py-1">{stat.clicked}</td>
                  <td className="px-2 py-1">{stat.tags}</td>
                  <td className="px-2 py-1">{stat.phishing_type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <pre className="bg-gray-100 rounded p-4 text-sm overflow-x-auto">
            {JSON.stringify(data, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}
