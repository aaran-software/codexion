import { Routes, Route } from "react-router-dom";
import ScrollToTop from "../../../resources/components/common/scrolltotop";
import {
  FaEnvelope,
  FaInstagram,
  FaPhoneAlt,
  FaWhatsapp,
} from "react-icons/fa";
import { lazy, Suspense } from "react";
import LoadingScreen from "../../../resources/components/loading/LoadingScreen";
import PortfolioFooter3 from "../../../resources/UIBlocks/footer/PortfolioFooter3";
import { AiFillClockCircle } from "react-icons/ai";
import NotFound from "../../../resources/components/notfound/NotFound";
const Home = lazy(() => import("./pages/Home"));
const Product = lazy(() => import("./pages/Product"));
const Contact = lazy(() => import("./pages/Contact"));
const About = lazy(() => import("./pages/about"));
const Manufacture = lazy(() => import("./pages/Manufacture"));
const HeaderPortfolio = lazy(
  () => import("../../../resources/UIBlocks/header/header-portfolio")
);
import ScrollToTopButton from "../../../resources/components/common/scrolltotopbutton";
function AppRoutes() {

  // Header contact details
  const contactItems = [
    {
      icon: FaPhoneAlt,
      value: "+91 42124 71568",
      href: "https://wa.me/914212471568",
    },
    {
      icon: FaEnvelope,
      value: "velu@pvrinternational.com",
      href: "mailto:velu@pvrinternational.com",
    },
  ];
  // footer

  const contacts = [
    {
      icon: FaPhoneAlt,
      value: "+91 98948 64679",
      href: "https://wa.me/917395944679",
    },
    { icon: AiFillClockCircle, value: "Mon-Sat: 9.00-18.00" },
    {
      icon: FaEnvelope,
      value: "exports@linkagro.in",
      href: "mailto:exports@linkagro.in",
    },
  ];

  const socialLinks = [
    {
      href: "https://www.instagram.com/linkagroexports",
      icon: <FaInstagram />,
    },
    { href: "https://wa.me/917395944679", icon: <FaWhatsapp /> },
  ];

  const pages = [
    { label: "Home", href: "/" },
    { label: "About Us", href: "/about" },
    { label: "Product", href: "/product" },
    { label: "Blogs", href: "/blog" },
    { label: "Manufacture", href: "/manufacture" },
    { label: "Contact", href: "/contact" },
  ];

  const newsletterText = "Subscribe to get the latest updates.";
  return (
    <div className="overflow-y-hidden bg-background">
      <ScrollToTop />
      <ScrollToTopButton />
      <Suspense fallback={<LoadingScreen image={"/assets/logo/logo.svg"} />}>
       
        <HeaderPortfolio
          menu={[
            { label: "Home", path: "/" },
            { label: "About Us", path: "/about" },
            { label: "Products", path: "/products" },
            { label: "Manufacture", path: "/manufacture" },
            { label: "Contact", path: "/contact" },
          ]}
          contact={contactItems}
          contactHeader={true}
          contactHeaderPath={"contact"}
        />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/product" element={<Product />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/about" element={<About />} />
          <Route path="/manufacture" element={<Manufacture />} />
          <Route
            path="*"
            element={
              <NotFound
                title="Oops! Page not found"
                description="The page you are looking for might have been moved or deleted."
                buttonLabel="Back to Home"
                homePath="/"
                highlightColor="text-red-500"
              />
            }
          />
        </Routes>

        <PortfolioFooter3
          address="79/22-B-4, EASWARAMOORTHY GOUNDER LAYOUT,
SAMUNDIPURAM EAST, GANDHI NAGAR PO,
TIRUPUR - 641 603, TAMILNADU, INDIA"
          contacts={contacts}
          socialLinks={socialLinks}
          pages={pages}
          newsletterText={newsletterText}
          newsletterPlaceholder="Your email"
          newsletterButtonText="Subscribe"
          companyName="Link Agro Exports"
          textColor="text-background"
        />
      </Suspense>
    </div>
  );
}

export default AppRoutes;
