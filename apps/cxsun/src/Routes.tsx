import React from 'react'
import {Routes, Route} from 'react-router-dom'
import Login from "../../../resources/global/auth/Login";
import SignUp from "../../../resources/global/auth/Signup";
import ProtectedRoute from "../../../resources/global/auth/ProtectedRoute";
import Admin from "./pages/Admin";
import Docs from "../../ecart/src/docs";

function AppRoutes() {
    return (
        <Routes>
            {/* <Docs /> */}
            <Route path='/' element={<Login/>}/>
            <Route path='/signup' element={<SignUp/>}/>
            <Route path="/docs" element={<Docs/>}/>
            <Route
                path="/dashboard/:component?"
                element={
                    <ProtectedRoute>
                        <Admin/>
                    </ProtectedRoute>
                }
            />
        </Routes>
    )
}

export default AppRoutes
