// import Login from "../../../../../../../apps/global/auth/Login";
// import ProtectedRoute from "../../../../../../../apps/global/auth/ProtectedRoute";
// import SignUp from "../../../../../../../apps/global/auth/Signup";
// import Admin from "./pages/Admin";
//
// const Cortex = () => [
//   {
//     path: "/",
//     element: <Login />
//   },
//   {
//     path: "/signup",
//     element: <SignUp />
//   },
//    {
//     path: "/dashboard/:component?",
//     element: (
//       <ProtectedRoute>
//         <Admin />
//       </ProtectedRoute>
//     ),
//   },
// ];
//
// export default Cortex;


import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Login from "../../global/auth/Login";
import SignUp from "../../global/auth/Signup";
import ProtectedRoute from "../../global/auth/ProtectedRoute";
import Admin from "./pages/Admin";


function AppRoutes() {
  return (
    <Routes>
        {/* <App /> */}
      <Route path='/' element={<Login />} />
      <Route path='/signup' element={<SignUp />} />
       <Route
          path="/dashboard/:component?"
          element={
            <ProtectedRoute>
              <Admin />
            </ProtectedRoute>
          }
        />
    </Routes>
  )
}

export default AppRoutes
