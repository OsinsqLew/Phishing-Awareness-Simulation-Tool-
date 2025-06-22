"use client";
import { useSession, signOut } from "next-auth/react";
import { useEffect, useState } from "react";
import {
  getUserData,
  getUserStatistics,
  getStatistics,
  getHomePage,
  trackReportPhishing
} from "@/lib/api";

export default function Home() {
  const { data: session, status } = useSession();
  const [userData, setUserData] = useState<any>(null);
  const [userStats, setUserStats] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);
  const [homePage, setHomePage] = useState<any>(null);
  const [phishingImg, setPhishingImg] = useState<string | null>(null);

  useEffect(() => {
    if (session?.user?.token) {
      getUserData(session.user.token).then(res => setUserData(res.data));
      getUserStatistics(session.user.token).then(res => setUserStats(res.data));
      getStatistics(session.user.token).then(res => setStats(res.data));
      getHomePage(session.user.token).then(res => setHomePage(res.data));
      trackReportPhishing().then(res => {
        const blob = new Blob([res.data], { type: "image/png" });
        setPhishingImg(URL.createObjectURL(blob));
      });
    }
  }, [session]);

  if (status === "loading") return <div className="flex min-h-screen items-center justify-center text-white text-xl">Ładowanie...</div>;
  if (!session) return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-md flex flex-col gap-6 items-center">
        <h1 className="text-4xl font-bold text-blue-900 mb-4">Phishing Awareness</h1>
        <a href="/login" className="underline text-blue-700 hover:text-blue-900 text-lg">Zaloguj się</a>
      </div>
    </div>
  );

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-blue-900 to-blue-400">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-2xl">
        <h1 className="text-4xl font-bold text-blue-900 mb-4 text-center">Phishing Awareness - Dashboard</h1>
        <button
          onClick={() => signOut({ callbackUrl: "/login" })}
          className="mb-6 bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded-lg transition block mx-auto"
        >
          Wyloguj
        </button>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h2 className="font-bold text-blue-900 mb-2">Dane użytkownika</h2>
            <pre className="bg-gray-100 rounded p-2 text-sm">{JSON.stringify(userData, null, 2)}</pre>
            <h2 className="font-bold text-blue-900 mt-4 mb-2">Statystyki użytkownika</h2>
            <pre className="bg-gray-100 rounded p-2 text-sm">{JSON.stringify(userStats, null, 2)}</pre>
          </div>
          <div>
            <h2 className="font-bold text-blue-900 mb-2">Statystyki globalne</h2>
            <pre className="bg-gray-100 rounded p-2 text-sm">{JSON.stringify(stats, null, 2)}</pre>
            <h2 className="font-bold text-blue-900 mt-4 mb-2">Home Page</h2>
            <pre className="bg-gray-100 rounded p-2 text-sm">{JSON.stringify(homePage, null, 2)}</pre>
            <h2 className="font-bold text-blue-900 mt-4 mb-2">Track Report Phishing</h2>
            {phishingImg && <img src={phishingImg} alt="Track Report Phishing" className="rounded shadow" />}
          </div>
        </div>
      </div>
    </div>
  );
}
