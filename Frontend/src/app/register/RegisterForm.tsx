"use client";
import { useState } from "react";
import { createUser } from "@/lib/api";
import { useRouter } from "next/navigation";

export function RegisterForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      await createUser(email, password);
      router.push("/login");
    } catch {
      setError("Błąd rejestracji");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400">
      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-md flex flex-col gap-6"
      >
        <h2 className="text-3xl font-bold text-center text-blue-900 mb-2">Rejestracja</h2>
        <div className="flex flex-col gap-2">
          <label htmlFor="email" className="font-semibold text-blue-900">Email</label>
          <input
            id="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            name="email"
            type="email"
            placeholder="Wpisz email"
            required
            className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="password" className="font-semibold text-blue-900">Hasło</label>
          <input
            id="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            name="password"
            type="password"
            placeholder="Wpisz hasło"
            required
            className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        {error && <p className="text-red-600 text-center">{error}</p>}
        <button
          type="submit"
          className="bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 rounded-lg transition"
        >
          Zarejestruj się
        </button>
        <div className="text-center mt-2">
          <a href="/login" className="text-blue-700 underline hover:text-blue-900">
            Masz już konto? Zaloguj się
          </a>
        </div>
      </form>
    </div>
  );
}