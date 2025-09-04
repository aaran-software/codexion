import { Routes, Route } from "react-router-dom";
import ProtectedRoute from "../../../resources/global/auth/ProtectedRoute";
import Admin from "./pages/Admin";
import FrappeLoginForm from "../../../resources/UIBlocks/auth/frappe-login";
import FrappeSignupForm from "../../../resources/UIBlocks/auth/frappe-signup";

function AppRoutes() {
  return (
    <Routes>
      {/* <Docs /> */}
      <Route path="/" element={<FrappeLoginForm />} />
      <Route path="/signup" element={<FrappeSignupForm />} />
      <Route
        path="/dashboard/:component?"
        element={
          <ProtectedRoute>
            <Admin />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

export default AppRoutes;
