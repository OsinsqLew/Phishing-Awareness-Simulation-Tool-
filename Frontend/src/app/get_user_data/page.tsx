"use client";
import { useState } from "react";
import axios from "axios";

export default function GetUserDataPage() {
  const [userId, setUserId] = useState("");
  const [token, setToken] = useState("");
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setData(null);
    try {
      const res = await axios.get(
        process.env.NEXT_PUBLIC_API_URL + "/get_user_data",
        {
          params: { user_id: userId, token },
        }
      );
      setData(res.data);
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
          Dane użytkownika
        </h1>
        <input
          name="userId"
          placeholder="User ID"
          className="input"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          required
        />
        <input
          name="token"
          placeholder="Token"
          className="input"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          required
        />
        <button
          type="submit"
          className="bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 rounded-lg transition"
        >
          Pobierz dane
        </button>
        {data && (
          <pre className="bg-green-100 rounded p-2 mt-2">
            {JSON.stringify(data, null, 2)}
          </pre>
        )}
        {error && <div className="text-red-600 mt-2">{error}</div>}
      </form>
    </div>
  );
}