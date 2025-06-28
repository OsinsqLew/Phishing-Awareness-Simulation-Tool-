"use client";
import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

export function RegisterForm() {
  const [form, setForm] = useState({
    email_address: "",
    first_name: "",
    last_name: "",
    password: "",
    confirm_password: "",
    tags: "",
  });
  const [error, setError] = useState("");
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (form.password !== form.confirm_password) {
      setError("Hasła nie są takie same.");
      return;
    }
    try {
      await axios.post(
        process.env.NEXT_PUBLIC_API_URL + "/create_user",
        {
          email_address: form.email_address,
          first_name: form.first_name,
          last_name: form.last_name,
          password: form.password,
          tags: form.tags,
        }
      );
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
          <label htmlFor="first_name" className="font-semibold text-blue-900">Imię</label>
          <input
            id="first_name"
            name="first_name"
            type="text"
            placeholder="Wpisz imię"
            required
            value={form.first_name}
            onChange={handleChange}
            className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="last_name" className="font-semibold text-blue-900">Nazwisko</label>
          <input
            id="last_name"
            name="last_name"
            type="text"
            placeholder="Wpisz nazwisko"
            required
            value={form.last_name}
            onChange={handleChange}
            className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="email_address" className="font-semibold text-blue-900">Email</label>
          <input
            id="email_address"
            name="email_address"
            type="email"
            placeholder="Wpisz email"
            required
            value={form.email_address}
            onChange={handleChange}
            className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="password" className="font-semibold text-blue-900">Hasło</label>
          <input
            id="password"
            name="password"
            type="password"
            placeholder="Wpisz hasło"
            required
            value={form.password}
            onChange={handleChange}
            className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="confirm_password" className="font-semibold text-blue-900">Powtórz hasło</label>
          <input
            id="confirm_password"
            name="confirm_password"
            type="password"
            placeholder="Powtórz hasło"
            required
            value={form.confirm_password}
            onChange={handleChange}
            className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="tags" className="font-semibold text-blue-900">Tagi (opcjonalnie)</label>
          <input
            id="tags"
            name="tags"
            type="text"
            placeholder="Wpisz tagi"
            value={form.tags}
            onChange={handleChange}
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