import { Routes, Route } from "react-router-dom";
import ScrollToTop from "../../../resources/components/common/scrolltotop";
import {
  FaFacebookF,
  FaInstagram,
  FaLinkedinIn,
  FaTwitter,
} from "react-icons/fa";
import { CiFacebook } from "react-icons/ci";
import { RiTwitterXLine } from "react-icons/ri";
import { lazy, Suspense } from "react";
import LoadingScreen from "../../../resources/components/loading/LoadingScreen";
import FooterLayout2 from "../../../resources/UIBlocks/footer/FooterLayout2";
import TransparentHeader from "../../../resources/UIBlocks/header/TransparentHeader";
import PortfolioFooter from "../../../resources/UIBlocks/footer/PortfolioFooter2";
const Home = lazy(() => import("./pages/Home"));

function AppRoutes() {
  return (
    <div className="overflow-y-hidden">
      <ScrollToTop />
      <Suspense
        fallback={<LoadingScreen image={"/assets/linkagro_logo.jpg"} />}
      >
        <TransparentHeader
          logo={{
            path: "/assets/svg/logo.png",
            mode: "logo",
            company_name: "Codexion",
            font_size: 2,
            height: 80,
            padding: 6,
            position: "center",
            // box_shadow: "0 4px 10px rgba(0,0,0,0.3)",
            // text_shadow: "2px 2px 4px rgba(0,0,0,0.3)",
          }}
          menu={[
            { label: "Home", path: "home" },
            { label: "About Us", path: "about" },
            { label: "Product", path: "product" },
            { label: "Contact", path: "contact" },
          ]}
        />

        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>

        <PortfolioFooter
          logo="assets/svg/logo.png"
          newsletterTitle="Subscribe Our Newsletter"
          newsletterPlaceholder="Email Address"
          newsletterButton="Submit Now"
          companyLinks={[
            { label: "Features", url: "#" },
            { label: "Pricing", url: "#" },
            { label: "Testimonials", url: "#" },
            { label: "FAQ’s", url: "#" },
          ]}
          utilityLinks={[
            { label: "Style Guide", url: "#" },
            { label: "Licenses", url: "#" },
            { label: "Changelog", url: "#" },
          ]}
          socialLinks={[
            { icon: <FaFacebookF />, label: "Facebook", url: "#" },
            { icon: <FaInstagram />, label: "Instagram", url: "#" },
            { icon: <FaTwitter />, label: "Twitter", url: "#" },
            { icon: <FaLinkedinIn />, label: "LinkedIn", url: "#" },
          ]}
          copyright="Copyright © 2025 Aaran."
        />
      </Suspense>
    </div>
  );
}

export default AppRoutes;
