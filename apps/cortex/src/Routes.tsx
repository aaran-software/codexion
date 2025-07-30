
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
