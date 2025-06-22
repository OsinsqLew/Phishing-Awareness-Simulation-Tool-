"use client";

import { logout } from "../login/actions";
import { ... } from "../../lib/api";

export default function Dashboard() {
  return (
    <div>
      <button onClick={() => logout()}>Logout</button>
    </div>
  );
}