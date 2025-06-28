"use client";
import { useEffect, useState } from "react";
import { getUserData } from "@/lib/api";
import { useSession } from "next-auth/react";

export default function GetUserDataPage() {
  const { data: session, status } = useSession();
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (status === "authenticated" && session?.user?.token && session?.user?.user_id) {
      getUserData(session.user.token, session.user.user_id)
        .then(res => setData(res.data))
        .catch(err => setError(err.message));
    }
  }, [session, status]);

  if (status === "loading") {
    return (
      <div className="min-h-screen flex items-center justify-center text-white text-xl">
        Ładowanie...
      </div>
    );
  }

  if (status !== "authenticated") {
    return (
      <div className="min-h-screen flex items-center justify-center text-white text-xl">
        Musisz być zalogowany, aby zobaczyć dane użytkownika.
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-xl">
        <h1 className="text-3xl font-bold text-blue-900 mb-4 text-center">Dane użytkownika</h1>
        {error && <div className="text-red-600 mb-4">{error}</div>}
        <pre className="bg-gray-100 rounded p-4 text-sm overflow-x-auto">{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  );
}