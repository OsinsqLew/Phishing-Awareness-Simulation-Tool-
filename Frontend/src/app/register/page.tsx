import { RegisterForm } from "./RegisterForm";

export default function RegisterPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-center mt-10">Rejestracja</h1>
      <RegisterForm />
      <div className="text-center mt-4">
        <a href="/login" className="underline text-blue-500">Masz już konto? Zaloguj się</a>
      </div>
    </div>
  );
}