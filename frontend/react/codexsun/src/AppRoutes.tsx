import { Routes, Route } from "react-router-dom";
import Login from "./pages/auth/Login";
import SignUp from "./pages/auth/Signup";
import NotFound from "./Components/NotFound";
import Admin from "./pages/app/Admin";
import { AuthProvider } from "./pages/auth/AuthContext";

import "animate.css";
import ProtectedRoute from "./pages/auth/ProtectedRoute";

export default function AppRoutes() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />

        <Route
          path="/dashboard/:component?"
          element={
            <ProtectedRoute>
              <Admin />
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<NotFound />} />
      </Routes>
    </AuthProvider>
  );
}
