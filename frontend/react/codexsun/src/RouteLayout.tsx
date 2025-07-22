// src/Components/RouteLayout.tsx
import { Outlet } from "react-router-dom";

// Headers & Footers
import { useAppContext } from "./pages/GlobalContext/AppContaxt";
import AppHeader from "./Components/Header/AppHeader";
import HeaderPortfolio from "./Components/Header/header-portfolio";
import Footer from "./Components/footer/Footer";
import FooterPortfolio from "./Components/footer/footer-portfolio";
import EcartHeader from "./Components/Header/EcartHeader";

const RouteLayout = () => {
  const { APP_CODE } = useAppContext();

  const getHeader = () => {
    switch (APP_CODE) {
      case "ecart":
        return <EcartHeader />;
      case "billing":
        return <AppHeader />;
      case "logicx":
        return <HeaderPortfolio />;
      default:
        return <HeaderPortfolio />;
    }
  };

  const getFooter = () => {
    switch (APP_CODE) {
      case "ecart":
        return <Footer />;
      case "billing":
        return <FooterPortfolio />;
      case "logicx":
        return <FooterPortfolio />;
      default:
        return <Footer />;
    }
  };

  return (
    <>
      {getHeader()}
      <main className="min-h-screen">
        <Outlet />
      </main>
      {getFooter()}
    </>
  );
};

export default RouteLayout;
