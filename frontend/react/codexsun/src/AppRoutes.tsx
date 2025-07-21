// // import { Routes, Route } from "react-router-dom";
// // import Login from "./pages/auth/Login";
// // import SignUp from "./pages/auth/Signup";
// // import NotFound from "./Components/NotFound";
// // import { AuthProvider } from "./pages/auth/AuthContext";

// // import "animate.css";
// // import ProtectedRoute from "./pages/auth/ProtectedRoute";
// // import Admin from "./pages/app/codexsun/Admin";

// // export default function AppRoutes() {
// //   return (
// //     <AuthProvider>
// //       <Routes>
// //         <Route path="/" element={<Login />} />
// //         <Route path="/signup" element={<SignUp />} />

// //         <Route
// //           path="/dashboard/:component?"
// //           element={
// //             <ProtectedRoute>
// //               <Admin />
// //             </ProtectedRoute>
// //           }
// //         />

// //         <Route path="*" element={<NotFound />} />
// //       </Routes>
// //     </AuthProvider>
// //   );
// // }


// // src/routes/index.tsx
// import { BrowserRouter, Routes, Route } from "react-router-dom";
// import { useAppContext } from "./pages/GlobalContext/AppContaxt";
// import Codexsun from './pages/app/codexsun/route'
// import Cortex from './pages/app/cortex/route'
// const AppRouter = () => {
//   const { APP_CODE } = useAppContext(); // e.g., 'ecart', 'crm', 'lms'

//   const getRoutes = () => {
//     switch (APP_CODE) {
//       case "ecart":
//         return <Codexsun />;
//       case "crm":
//         return <Cortex />;
//       default:
//         return <div>App Not Found</div>;
//     }
//   };

//   return (
//     <BrowserRouter>
//       <Routes>{getRoutes()}</Routes>
//     </BrowserRouter>
//   );
// };

// export default AppRouter;

// src/AppRouter.tsx
import { BrowserRouter } from "react-router-dom";
import { useRoutes } from "react-router-dom";
import { useAppContext } from "./pages/GlobalContext/AppContaxt";
import Codexsun from "./pages/app/codexsun/route";
import Cortex from "./pages/app/cortex/route";

const AppRoutes = () => {
  const { APP_CODE } = useAppContext();

  const routes = (() => {
    switch (APP_CODE) {
      case "web2":
        return Codexsun();
      case "web":
        return Cortex();
      default:
        return [
          {
            path: "*",
            element: <div>App Not Found</div>,
          },
        ];
    }
  })();

  return useRoutes(routes);
};

const AppRouter = () => (
  <BrowserRouter>
    <AppRoutes />
  </BrowserRouter>
);

export default AppRouter;

