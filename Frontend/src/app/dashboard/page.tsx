"use client";

import { logout } from "../login/actions";
import { ... } from "../../lib/api";

// Tymczasowo udawaj, że użytkownik jest zalogowany
const fakeSession = { user: { token: "FAKE_TOKEN" } };
const sessionToUse = session || fakeSession;

export default function Dashboard() {
  return (
    <div>
      <button onClick={() => logout()}>Logout</button>
    </div>
  );
}