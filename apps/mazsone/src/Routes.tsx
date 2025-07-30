import React from 'react'
import {Routes, Route, useLocation} from 'react-router-dom'
import SignUp from "../../global/auth/Signup";
import ProtectedRoute from "../../global/auth/ProtectedRoute";
import Admin from "./pages/Admin";
import Home from "./pages/Home";
import ProductForm from "./pages/ProductForm";
import ProductPage from "../../../resources/UIBlocks/ProductPage";
import CategoryPage from "../../../resources/UIBlocks/CategoryPage";
import Wishlist from "../../../resources/UIBlocks/Wishlist";
import Cart from "./pages/Cart";
import Footer from "../../../resources/components/footer/Footer";
import Header from "../../../resources/components/header/Header";
import {FrappeLoginForm} from "../../../resources/components/auth/frappe-login";

function AppRoutes() {
    const location = useLocation();
    const hideLayout =
        location.pathname === '/login' ||
        location.pathname === '/signup' ||
        location.pathname.startsWith('/dashboard');
    return (
        <div>
            {!hideLayout && <Header/>}

            <Routes>

                {/* <App /> */}
                <Route path="/" element={<Home/>}/>
                <Route path="/cart" element={<Cart/>}/>
                <Route path="/login" element={<FrappeLoginForm/>}/>
                <Route path="/signup" element={<SignUp/>}/>
                <Route path="/productpage/:id" element={<ProductPage/>}/>
                <Route path="/category/:category" element={<CategoryPage/>}/>
                <Route path="/wishlist" element={<Wishlist/>}/>
                <Route path="/productform" element={<ProductForm/>}/>
                <Route
                    path="/dashboard/:component?"
                    element={
                        <ProtectedRoute>
                            <Admin/>
                        </ProtectedRoute>
                    }
                />
            </Routes>
            {!hideLayout && <Footer/>}

        </div>
    )
}

export default AppRoutes
