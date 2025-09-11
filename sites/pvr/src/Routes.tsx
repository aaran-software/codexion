import { Routes, Route } from "react-router-dom";
import ScrollToTop from "../../../resources/components/common/scrolltotop";
import {
  FaEnvelope,
  FaInstagram,
  FaPhoneAlt,
  FaTwitter,
  FaWhatsapp,
} from "react-icons/fa";
import { lazy, Suspense } from "react";
import LoadingScreen from "../../../resources/components/loading/LoadingScreen";
import FooterLayout2 from "../../../resources/UIBlocks/footer/FooterLayout2";
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
  const socialLinks = [
    {
      href: "https://www.instagram.com/linkagroexports",
      icon: <FaInstagram />,
    },
    { href: "https://wa.me/917395944679", icon: <FaWhatsapp /> },
    { icon: <FaTwitter />, href: "https://twitter.com" },
  ];

  const pages = [
    { label: "Home", href: "/" },
    { label: "About Us", href: "/about" },
    { label: "Product", href: "/product" },
    { label: "Manufacture", href: "/manufacture" },
    { label: "Contact", href: "/contact" },
  ];

  return (
    <div className="overflow-y-hidden bg-background">
      <ScrollToTop />
      <ScrollToTopButton />
      <Suspense fallback={<LoadingScreen image={"/assets/logo/logo.svg"} />}>
        <HeaderPortfolio
          menu={[
            { label: "Home", route: "/" },
            { label: "About Us", route: "/about" },
            { label: "Products", route: "/products" },
            { label: "Manufacture", route: "/manufacture" },
            { label: "Contact", route: "/contact" },
          ]}
          contact={contactItems}
          contactHeader={true}
          contactHeaderPath={"contact"}
        />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/productS" element={<Product />} />
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

        {/* <PortfolioFooter4
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
          mapSrc={`https://www.google.com/maps/embed?pb=!1m16!1m12!1m3!1d3914.8392617362874!2d77.31750527370102!3d11.125346452663674!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!2m1!1s79%2F22-B-4%2C%20EASWARAMOORTHY%20GOUNDER%20LAYOUT%2C%20SAMUNDIPURAM%20EAST%2C%20GANDHI%20NAGAR%20PO%2C%20TIRUPUR%20-%20641%20603%2C%20TAMILNADU%2C%20INDIA.!5e0!3m2!1sen!2sin!4v1757349543666!5m2!1sen!2sin`}
        /> */}
        <FooterLayout2
          companyName="PVR & DEENU International"
          about={{
            title: "Pages",
            items: pages,
          }}
          phone="+914212471568"
          email="velu@pvrinternational.com"
          address={{
            lines: [
              `79/22-B-4, EASWARAMOORTHY GOUNDER LAYOUT,
SAMUNDIPURAM EAST, GANDHI NAGAR PO,
TIRUPUR - 641 603, TAMILNADU, INDIA`
            ],
            socialLinks: socialLinks,
          }}
          
          mapLink={`https://www.google.com/maps/embed?pb=!1m16!1m12!1m3!1d3914.8392617362874!2d77.31750527370102!3d11.125346452663674!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!2m1!1s79%2F22-B-4%2C%20EASWARAMOORTHY%20GOUNDER%20LAYOUT%2C%20SAMUNDIPURAM%20EAST%2C%20GANDHI%20NAGAR%20PO%2C%20TIRUPUR%20-%20641%20603%2C%20TAMILNADU%2C%20INDIA.!5e0!3m2!1sen!2sin!4v1757349543666!5m2!1sen!2sin`} // Embed map link
          version="1.0.0"
          copyrights="2025 All copyrights."
          copyrights_company="Aaran Software"
        />
      </Suspense>
    </div>
  );
}

export default AppRoutes;
