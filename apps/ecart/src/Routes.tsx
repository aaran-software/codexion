import React, { lazy, Suspense } from "react";
import { Routes, Route, useLocation } from "react-router-dom";

const SignUp = lazy(() => import("../../global/auth/Signup"));
const ProtectedRoute = lazy(() => import("../../global/auth/ProtectedRoute"));
const Admin = lazy(() => import("./pages/Admin"));
const Home = lazy(() => import("./pages/Home"));
const ProductForm = lazy(() => import("./pages/ProductForm"));
const ProductPage = lazy(
  () => import("../../../resources/UIBlocks/ProductPage")
);
const CategoryPage = lazy(
  () => import("../../../resources/UIBlocks/CategoryPage")
);
const Wishlist = lazy(() => import("../../../resources/UIBlocks/Wishlist"));
const Cart = lazy(() => import("./pages/Cart"));
const Footer = lazy(
  () => import("../../../resources/components/footer/Footer")
);
const Header = lazy(
  () => import("../../../resources/components/header/Header")
);
const FrappeLoginForm = lazy(
  () => import("../../../resources/components/auth/frappe-login")
);
// import { FrappeLoginForm } from "../../../resources/components/auth/frappe-login";
// ✅ Optional: import your custom loader
import LoadingScreen from "../../../resources/components/loading/LoadingScreen";
function AppRoutes() {
  const location = useLocation();
  const hideLayout =
    location.pathname === "/login" ||
    location.pathname === "/signup" ||
    location.pathname.startsWith("/dashboard");
  return (
    <Suspense fallback={<LoadingScreen image={"/assets/svg/logo.svg"} />}>
      <div>
        {!hideLayout && <Header />}

        <Routes>
          {/* <App /> */}
          <Route path="/" element={<Home />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/login" element={<FrappeLoginForm />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/productpage/:id" element={<ProductPage />} />
          <Route path="/category/:category" element={<CategoryPage />} />
          <Route path="/wishlist" element={<Wishlist />} />
          <Route path="/productform" element={<ProductForm />} />
          <Route
            path="/dashboard/:component?"
            element={
              <ProtectedRoute>
                <Admin />
              </ProtectedRoute>
            }
          />
        </Routes>
        {!hideLayout && <Footer />}
      </div>
    </Suspense>
  );
}

export default AppRoutes;
