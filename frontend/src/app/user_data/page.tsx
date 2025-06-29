'use client';
import { useEffect, useState } from 'react';
import { useGlobalContext } from '../global-context';

export default function GetUserDataPage() {
  const { state } = useGlobalContext();
  const { session } = state;
  const [data, setData] = useState<{
    email_address: string;
    first_name: string;
    last_name: string;
    tags: string;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (session) {
      const get_user_data = async () => {
        try {
          const response = await fetch(
            encodeURI(
              `/proxy/get_user_data?user_id=${session.user_id}&token=${session.token}`
            )
          );
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          const data = await response.json();
          setData(data);
        } catch (error) {
          console.error(error);
          setError('Błąd podczas pobierania danych użytkownika');
        }
      };

      get_user_data();
    }
  }, [session]);

  if (!session) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white text-xl">
        Musisz być zalogowany, aby zobaczyć dane użytkownika.
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400 text-black">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-xl">
        <h1 className="text-3xl font-bold text-blue-900 mb-4 text-center">
          Dane użytkownika
        </h1>
        {error && <div className="text-red-600 mb-4">{error}</div>}
        <pre className="bg-gray-100 rounded p-4 text-sm overflow-x-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    </div>
  );
}
