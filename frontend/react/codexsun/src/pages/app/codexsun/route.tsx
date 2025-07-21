import Login from "../auth/Login";
import SignUp from "../auth/Signup";
import ProtectedRoute from "../auth/ProtectedRoute";
import Admin from "./Admin";

const Codexsun = () => [
  {
    path: "/",
    element: <Login />,
  },
  {
    path: "/signup",
    element: <SignUp />,
  },
  {
    path: "/dashboard/:component?",
    element: (
      <ProtectedRoute>
        <Admin />
      </ProtectedRoute>
    ),
  },
];

export default Codexsun;
