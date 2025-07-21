
// src/AppRouter.tsx
import { BrowserRouter } from "react-router-dom";
import { useRoutes } from "react-router-dom";
import { useAppContext } from "./pages/GlobalContext/AppContaxt";
import Codexsun from "./pages/app/codexsun/route";
import Cortex from "./pages/app/cortex/route";

const AppRoutes = () => {
  const { APP_CODE } = useAppContext();
console.log("type",APP_CODE)
  const routes = (() => {
    switch (APP_CODE) {
      case "billing":
        return Codexsun();
      case "cortex":
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

