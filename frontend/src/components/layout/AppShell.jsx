import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import MobileNav from "./MobileNav";

export default function AppShell() {
  return (
    <div className="app-shell">

      <Sidebar />

      <div className="main-shell">

        <Topbar />

        <main className="page-content">
          <Outlet />
        </main>

      </div>

      <MobileNav />

    </div>
  );
}