import { lazy, Suspense, useEffect, useState } from "react";
import { Routes, Route, useLocation, useNavigate } from "react-router-dom";

const SignUp = lazy(() => import("../../global/auth/Signup"));
const ProtectedRoute = lazy(() => import("../../global/auth/ProtectedRoute"));
const Admin = lazy(() => import("./pages/Admin"));
const Home = lazy(() => import("./pages/Home"));
const ProductPage = lazy(
  () => import("../../../resources/UIBlocks/ProductPage")
);
const CategoryPage = lazy(
  () => import("./pages/CategoryPage")
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
import ScrollToTop from "../../../resources/components/common/scrolltotop";
import ScrollToTopButton from "../../../resources/components/common/scrolltotopbutton";
function AppRoutes() {
  const navigate = useNavigate();
  const location = useLocation();
  const hideLayout =
    location.pathname === "/login" ||
    location.pathname === "/signup" ||
    location.pathname === "/test" ||
    location.pathname.startsWith("/dashboard");

  const routeTitles: { pattern: RegExp; title: string }[] = [
    { pattern: /^\/$/, title: "Tech Media - Home" },
    { pattern: /^\/cart$/, title: "Tech Media - Cart" },
    { pattern: /^\/wishlist$/, title: "Tech Media - Wishlist" },
    { pattern: /^\/login$/, title: "Tech Media - Login" },
    { pattern: /^\/signup$/, title: "Tech Media - Signup" },
    { pattern: /^\/productpage\/[^/]+$/, title: "Tech Media - Product Page" },
    { pattern: /^\/category\/[^/]+$/, title: "Tech Media - Category" },
    { pattern: /^\/special\/[^/]+$/, title: "Tech Media - Special Offer" },
    { pattern: /^\/dashboard(\/[^/]*)?$/, title: "Tech Media - Dashboard" },
  ];

  useEffect(() => {
    const match = routeTitles.find(({ pattern }) =>
      pattern.test(location.pathname)
    );
    document.title = match?.title || "Tech Media";
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
        <ScrollToTop />
        <ScrollToTopButton />
        {!hideLayout && (
          <Header
            logo={logo}
            showLogin={false} // Toggle login and cart section
            user={user} // Pass null if no user logged in
            logout={logout}
            menuItems={menuItems}
            showSearch={true} // Toggle search bar
            onSearchApi={`/api/resource/Catalog Details?fields=["name","image_1","price"]`}
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
          <Route path="/category/:category?" element={<CategoryPage />} />
          <Route path="/special/:id" element={<SpecialCategory />} />
          <Route path="/wishlist" element={<Wishlist />} />
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
        {!hideLayout && (
          <Footer
            aboutLinks={[
              { label: "Our Company", path: "/contactus" },
              { label: "Brand Assets", path: "/contactus" },
              { label: "Contact Us", path: "/contactus" },
              { label: "Jobs", path: "/contactus" },
              { label: "Events", path: "/contactus" },
              { label: "Blog", path: "/payment" },
              { label: "Customers", path: "/payment" },
              { label: "Level Privacy", path: "/payment" },
            ]}
            servicesLinks={[
              { label: "Support", path: "/payment" },
              { label: "Become a Partner", path: "/payment" },
              { label: "Web Service", path: "/payment" },
              { label: "Software", path: "/payment" },
              { label: "FAQ", path: "/FAQ" },
            ]}
            policyLinks={[
              { label: "Terms of Use", path: "/termsofuse" },
              { label: "Security", path: "/security" },
              { label: "Privacy", path: "/privacy" },
            ]}
            contact={{
              phone: "9894244450",
              email: "support@techmedia.in",
            }}
            address={{
              company: "Tech Media",
              lines: [
                "436, Avinashi Road,",
                "Near CITU Office,",
                "Tiruppur, Tamil Nadu 641602",
              ],
              website: "www.techmedia.in",
              infoEmail: "info@techmedia.in",
            }}
            social={{
              whatsapp: "https://wa.me/9894244450",
              facebook: "https://facebook.com/techmedia",
              twitter: "https://twitter.com/techmedia",
              instagram: "https://instagram.com/techmedia",
            }}
            version="V 1.0.1"
          />
        )}
      </div>
    </Suspense>
  );
}

export default AppRoutes;
