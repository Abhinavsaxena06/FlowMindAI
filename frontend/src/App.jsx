import {
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import AppShell from "./components/layout/AppShell";

import Dashboard from "./pages/Dashboard";
import LiveMonitoring from "./pages/LiveMonitoring";
import Predictions from "./pages/Predictions";
import SignalControl from "./pages/SignalControl";
import NetworkView from "./pages/NetworkView";
import Simulation from "./pages/Simulation";

export default function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>

        <Route
          path="/"
          element={<Dashboard />}
        />

        <Route
          path="/live"
          element={<LiveMonitoring />}
        />

        <Route
          path="/predictions"
          element={<Predictions />}
        />

        <Route
          path="/signals"
          element={<SignalControl />}
        />

        <Route
          path="/network"
          element={<NetworkView />}
        />

        <Route
          path="/simulation"
          element={<Simulation />}
        />

        <Route
          path="*"
          element={
            <Navigate
              to="/"
              replace
            />
          }
        />

      </Route>
    </Routes>
  );
}