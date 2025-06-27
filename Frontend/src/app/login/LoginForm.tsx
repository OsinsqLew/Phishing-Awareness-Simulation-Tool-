"use client";
import { signIn } from "next-auth/react";
import { useState } from "react";

export function LoginForm() {
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    const formData = new FormData(e.currentTarget);
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    const res = await signIn("credentials", {
      redirect: true,
      email,
      password,
      callbackUrl: "/",
    });

    if (res?.error) setError("Nieprawidłowe dane logowania");
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400">
      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-md flex flex-col gap-6"
      >
        <h2 className="text-3xl font-bold text-center text-blue-900 mb-2">
          Logowanie
        </h2>
        <div className="flex flex-col gap-2">
          <label
            htmlFor="email"
            className="font-semibold text-blue-900"
          >
            Email
          </label>
          <input
            id="email"
            name="email"
            type="email"
            placeholder="Wpisz email"
            required
            className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        <div className="flex flex-col gap-2">
          <label
            htmlFor="password"
            className="font-semibold text-blue-900"
          >
            Hasło
          </label>
          <input
            id="password"
            name="password"
            type="password"
            placeholder="Wpisz hasło"
            required
            className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        {error && (
          <p className="text-red-600 text-center">
            {error}
          </p>
        )}
        <button
          type="submit"
          className="bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 rounded-lg transition"
        >
          Zaloguj się
        </button>
        <div className="text-center mt-2">
          <a
            href="/register"
            className="text-blue-700 underline hover:text-blue-900"
          >
            Nie masz konta? Zarejestruj się
          </a>
        </div>
      </form>
    </div>
  );
}