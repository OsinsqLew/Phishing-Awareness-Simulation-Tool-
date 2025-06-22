import { LoginForm } from "./LoginForm";

export default function LoginPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-center mt-10">Logowanie</h1>
      <LoginForm />
      <div className="text-center mt-4">
        <a href="/register" className="underline text-blue-500">Nie masz konta? Zarejestruj się</a>
      </div>
    </div>
  );
}