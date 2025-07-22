// src/AppRouter.tsx
import { BrowserRouter } from "react-router-dom";
import { useRoutes } from "react-router-dom";
import { useAppContext } from "./pages/GlobalContext/AppContaxt";
import Codexsun from "./pages/app/codexsun/route";
import Cortex from "./pages/app/cortex/route";
import Ecart from "./pages/app/ecart/route";
import Mazsone from "./pages/app/mazsone/route";
import Logicx from "./pages/Website/Logicx/route";

const AppRoutes = () => {
  const { APP_CODE } = useAppContext();
  console.log("type", APP_CODE);
  const routes = (() => {
    switch (APP_CODE) {
      case "billing":
        return Codexsun();
      case "cortex":
        return Cortex();
      case "ecart":
        return Ecart();
      case "mazsone":
        return Mazsone();
      case "logicx":
        return Logicx();
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
