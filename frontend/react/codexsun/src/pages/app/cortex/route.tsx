import Login from "../auth/Login";
import SignUp from "../auth/Signup";

const Cortex = () => [
  {
    path: "/",
    element: <Login />
  },
  {
    path: "/signup",
    element: <SignUp />
  }
];

export default Cortex;
