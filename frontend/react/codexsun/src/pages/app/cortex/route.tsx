import Login from "../auth/Login";
import ProtectedRoute from "../auth/ProtectedRoute";
import SignUp from "../auth/Signup";
import Admin from "./Admin";

const Cortex = () => [
  {
    path: "/",
    element: <Login />
  },
  {
    path: "/signup",
    element: <SignUp />
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

export default Cortex;
