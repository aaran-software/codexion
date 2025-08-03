import { Routes, Route } from "react-router-dom";
import ScrollToTop from "../../../resources/components/common/scrolltotop";
import { FaInstagram } from "react-icons/fa";
import { CiFacebook } from "react-icons/ci";
import { FiTwitter } from "react-icons/fi";
import React, { lazy, Suspense } from "react";
import LoadingScreen from "../../../resources/components/loading/LoadingScreen";
const Home = lazy(() => import("./pages/Home"));
const Product = lazy(() => import("./pages/Product"));
const Contact = lazy(() => import("./pages/Contact"));
const About = lazy(() => import("./pages/about"));
const Manufacture = lazy(() => import("./pages/Manufacture"));
const HeaderPortfolio2 = lazy(
  () => import("../../../resources/components/header/HeaderPortfolio2")
);
const FooterLayout1 = lazy(
  () => import("../../../resources/UIBlocks/footer/FooterLayout1")
);
const BlogLayout1 = lazy(
  () => import("../../../resources/layouts/blog/BlogLayout1")
);

const Blog = React.lazy(() => import("./pages/Blog"));
function AppRoutes() {
  return (
    <div>
      <ScrollToTop />
      <Suspense
        fallback={
          <LoadingScreen image={"/assets/linkagro_logo.jpg"} />
        }
      >
        <HeaderPortfolio2
          menu={[
            { label: "Home", path: "/" },
            { label: "About Us", path: "/about" },
            { label: "Product", path: "/product" },
            { label: "Blogs", path: "/blog" },
            { label: "Manufacture", path: "/manufacture" },
            { label: "Contact", path: "/contact" },
          ]}
        />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/product" element={<Product />} />
          <Route path="/blog" element={<Blog />} />
          <Route path="/blog/:id" element={<BlogLayout1 />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/about" element={<About />} />
          <Route path="/manufacture" element={<Manufacture />} />
        </Routes>
        <FooterLayout1
          about={{
            title: "Link Agro",
            items: [
              { label: "Home", href: "/" },
              { label: "About Us", href: "/about" },
              { label: "Product", href: "/product" },
              { label: "Blogs", href: "/blog" },
              { label: "Manufacture", href: "/manufacture" },
            ],
          }}
          help={{
            title: "Help",
            items: [
              { label: "FAQs", href: "/faq" },
              { label: "Contact", href: "/contact" },
            ],
          }}
          consumerPolicy={{
            title: "Consumer Policy",
            phone: "+91 98765 43210",
            email: "info@linkagro.com",
            items: [
              { label: "Privacy Policy", href: "/privacy" },
              { label: "Terms of Service", href: "/terms" },
            ],
          }}
          address={{
            lines: ["123 Agro Street", "Tamil Nadu, India", "PIN - 600001"],
            socialLinks: [
              { href: "https://instagram.com/linkagro", icon: <FaInstagram /> },
              { href: "https://facebook.com/linkagro", icon: <CiFacebook /> },
              { href: "https://twitter.com/linkagro", icon: <FiTwitter /> },
            ],
          }}
          updateConfig={{
            id: "version-check",
            title: "Version Update",
            description: "Click to check if you're on the latest version.",
            api: "/api/check-version", // Replace with your actual endpoint or mock
          }}
          version="1.0.0"
          copyrights="2025 Link Agro Exports. All Rights Reserved. Powered by Aaran Software"
        />
      </Suspense>
    </div>
  );
}

export default AppRoutes;
