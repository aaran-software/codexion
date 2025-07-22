import NotFound from "../../../Components/NotFound";
import CategoryPage from "../../../Resources/UIBlocks/CategoryPage";
import ProductPage from "../../../Resources/UIBlocks/ProductPage";
import Wishlist from "../../../Resources/UIBlocks/Wishlist";
import Login from "../auth/Login";
import ProtectedRoute from "../auth/ProtectedRoute";
// import ProtectedRoute from "../auth/ProtectedRoute";
import SignUp from "../auth/Signup";
import Admin from "./Admin";
import ProductForm from "./Forms/ProductForm";
import Home from "./Home";

const Ecart = () => [
  {
    path: "/",
    element: <Home />
  },
  {
    path: "/signup",
    element: <SignUp />
  },
 {
    path: "/login",
    element: <Login />
  },{
    path: "/productpage/:id",
    element: <ProductPage />
  },{
    path: "/category/:category",
    element: <CategoryPage />
  },{
    path: "/wishlist",
    element: <Wishlist />
  },{
    path: "/productform",
    element: <ProductForm />
  },{
    path: "*",
    element: <NotFound />
  },
   {
    path: "/admin/:component?",
    element: (
      <ProtectedRoute>
        <Admin />
      </ProtectedRoute>
    ),
  },
];

export default Ecart;
