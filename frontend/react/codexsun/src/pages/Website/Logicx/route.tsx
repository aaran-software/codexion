// src/pages/app/ecart/route.tsx
import RouteLayout from "../../../RouteLayout";
import Login from "../../app/auth/Login";
import ProtectedRoute from "../../app/auth/ProtectedRoute";
import SignUp from "../../app/auth/Signup";
import Admin from "../../app/codexsun/Admin";
import Home from "./pages/Home";

const Logicx = () => [
{
     path: "/",
    element: <RouteLayout />,
    children: [
      { index: true, element: <Home /> },
    ],
},
  // ❌ No Layout applied (login/signup/admin stand alone)
  { path: "/login", element: <Login /> },
  { path: "/signup", element: <SignUp /> },
  {
    path: "/dashboard/:component?",
    element: (
      <ProtectedRoute>
        <Admin />
      </ProtectedRoute>
    ),
  },
];

export default Logicx;
