'use client';

import Link from 'next/link';
import { useGlobalContext } from './global-context';

export default function Home() {
  const { state, setState } = useGlobalContext();
  const { session } = state;
  // console.log(session);

  if (!session)
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400">
        <div className="flex w-full max-w-md flex-col items-center gap-6 rounded-xl bg-white p-8 shadow-2xl">
          <h1 className="mb-4 text-4xl font-bold text-blue-900">
            Phishing Awareness
          </h1>
          <a
            href="/login"
            className="text-lg text-blue-700 underline hover:text-blue-900"
          >
            Zaloguj się
          </a>
        </div>
      </div>
    );

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400">
      <div className="w-full max-w-2xl rounded-xl bg-white p-8 shadow-2xl">
        <h1 className="mb-4 text-center text-4xl font-bold text-blue-900">
          Phishing Awareness - Dashboard
        </h1>
        <button
          onClick={() => setState({ session: null })}
          className="mx-auto mb-6 block rounded-lg bg-blue-700 px-4 py-2 font-bold text-white transition hover:bg-blue-800"
        >
          Wyloguj
        </button>
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <div>
            <h2 className="mb-2 font-bold text-blue-900">Dane użytkownika</h2>
            <pre className="rounded bg-gray-100 p-2 text-sm">
              <Link
                href="/user_data"
                className="text-lg text-blue-700 underline hover:text-blue-900"
              >
                /user_data
              </Link>
            </pre>
            <h2 className="mt-4 mb-2 font-bold text-blue-900">
              Statystyki użytkownika
            </h2>
            <pre className="rounded bg-gray-100 p-2 text-sm">
              <Link
                href="/user_stats"
                className="text-lg text-blue-700 underline hover:text-blue-900"
              >
                /user_stats
              </Link>
            </pre>
          </div>
          <div>
            <h2 className="mb-2 font-bold text-blue-900">
              Statystyki globalne
            </h2>
            <pre className="rounded bg-gray-100 p-2 text-sm">
              <Link
                href="/global_stats"
                className="text-lg text-blue-700 underline hover:text-blue-900"
              >
                /global_stats
              </Link>
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
