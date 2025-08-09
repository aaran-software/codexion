import { lazy, Suspense, useEffect, useState } from "react";
import { Routes, Route, useLocation, useNavigate } from "react-router-dom";

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
const SpecialCategory = lazy(
  () => import("../../../resources/UIBlocks/SpecialCategory")
);
import settings from "../public/settings.json";
import LoadingScreen from "../../../resources/components/loading/LoadingScreen";
import Test from "./pages/Test";
function AppRoutes() {
  const navigate = useNavigate();
  const location = useLocation();
  const hideLayout =
    location.pathname === "/login" ||
    location.pathname === "/signup" ||
    location.pathname === "/test" ||
    location.pathname.startsWith("/dashboard");

  const routeTitles: { pattern: RegExp; title: string }[] = [
    { pattern: /^\/$/, title: "Tmnext - Home" },
    { pattern: /^\/cart$/, title: "Tmnext - Cart" },
    { pattern: /^\/wishlist$/, title: "Tmnext - Wishlist" },
    { pattern: /^\/login$/, title: "Tmnext - Login" },
    { pattern: /^\/signup$/, title: "Tmnext - Signup" },
    { pattern: /^\/productform$/, title: "Tmnext - Add Product" },
    { pattern: /^\/productpage\/[^/]+$/, title: "Tmnext - Product Page" },
    { pattern: /^\/category\/[^/]+$/, title: "Tmnext - Category Page" },
    { pattern: /^\/dashboard(\/[^/]*)?$/, title: "Tmnext - Admin Dashboard" },
  ];

  useEffect(() => {
    const match = routeTitles.find(({ pattern }) =>
      pattern.test(location.pathname)
    );
    document.title = match?.title || "Tmnext";
  }, [location.pathname]);

  const logo = {
    ...settings.logo,
    position: settings.logo.position as "left" | "center" | "right",
    mode: settings.logo.mode as "logo" | "name" | "both",
  };

  // Example menu items
  const menuItems = [
    { label: "My Profile", path: "/profile", icon: "user" },
    { label: "My Orders", path: "/orders", icon: "plus" },
    { label: "Wishlist", path: "/wishlist", icon: "like" },
    { label: "Logout", path: "/", icon: "logout" },
  ];

  // Example mock user
  const user = { name: "John Doe", id: 123 };

  // Logout handler
  const logout = async () => {
    console.log("Logging out...");
    // ...logout logic, e.g., clear tokens
    navigate("/login");
  };

  return (
    <Suspense fallback={<LoadingScreen image={"/assets/svg/logo.svg"} />}>
      <div>
        {!hideLayout && (
          <Header
            logo={logo}
            showLogin={true} // Toggle login section
            user={user} // Pass null if no user logged in
            logout={logout}
            menuItems={menuItems}
            showSearch={true} // Toggle search bar
            onSearchApi={`/api/resource/Product?fields=["name","image","price"]`}
            onNavigate={(path) => navigate(path)}
          />
        )}

        <Routes>
          {/* <App /> */}
          <Route path="/" element={<Home />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/login" element={<FrappeLoginForm />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/productpage/:id" element={<ProductPage />} />
          <Route path="/category/:category" element={<CategoryPage />} />
          <Route path="/special/:id" element={<SpecialCategory />} />
          <Route path="/wishlist" element={<Wishlist />} />
          <Route path="/productform" element={<ProductForm />} />
          <Route path="/test" element={<Test />} />
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
