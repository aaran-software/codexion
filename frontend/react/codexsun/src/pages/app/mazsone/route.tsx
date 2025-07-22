// src/pages/app/ecart/route.tsx
import NotFound from "../../../Components/NotFound";
import CategoryPage from "../../../Resources/UIBlocks/CategoryPage";
import ProductPage from "../../../Resources/UIBlocks/ProductPage";
import Wishlist from "../../../Resources/UIBlocks/Wishlist";
import Login from "../auth/Login";
import SignUp from "../auth/Signup";
import ProtectedRoute from "../auth/ProtectedRoute";
import Admin from "./Admin";
import ProductForm from "./Forms/ProductForm";
import Home from "./Home";
import RouteLayout from "../../../RouteLayout";
import Cart from "./Cart";

const Mazsone = () => [
  // ✅ Layout applied to these pages
  {
    path: "/",
    element: <RouteLayout />,
    children: [
      { index: true, element: <Home /> },
      { path: "productpage/:id", element: <ProductPage /> },
      { path: "category/:category", element: <CategoryPage /> },
      { path: "wishlist", element: <Wishlist /> },
      { path: "productform", element: <ProductForm /> },
      { path: "cart", element: <Cart /> },
      { path: "*", element: <NotFound /> },
    ],
  },

  // ❌ No Layout applied (login/signup/admin stand alone)
  { path: "/login", element: <Login /> },
  { path: "/signup", element: <SignUp /> },
  {
    path: "/dashboard/:component?",
    element: (
      <ProtectedRoute>
        <Admin />
      </ProtectedRoute>
    ),
  },
];

export default Mazsone;
