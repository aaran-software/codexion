import { Routes, Route } from "react-router-dom";
import ScrollToTop from "../../../resources/components/common/scrolltotop";
import { FaInstagram, FaWhatsapp } from "react-icons/fa";
import { CiFacebook } from "react-icons/ci";
import { RiTwitterXLine } from "react-icons/ri";
import React, { lazy, Suspense } from "react";
import LoadingScreen from "../../../resources/components/loading/LoadingScreen";
import FooterLayout2 from "../../../resources/UIBlocks/footer/FooterLayout2";
import BlogForm from "./pages/blog/BlogForm";
const Home = lazy(() => import("./pages/Home"));
const Product = lazy(() => import("./pages/Product"));
const Contact = lazy(() => import("./pages/Contact"));
const About = lazy(() => import("./pages/about"));
const Manufacture = lazy(() => import("./pages/Manufacture"));
const HeaderPortfolio2 = lazy(
  () => import("../../../resources/UIBlocks/header/HeaderPortfolio2")
);

const BlogLayout1 = lazy(
  () => import("../../../resources/layouts/blog/BlogLayout1")
);

const Blog = React.lazy(() => import("./pages/Blog"));
function AppRoutes() {
  return (
    <div className="overflow-y-hidden bg-background">
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
          <Route path="/blogForm" element={<BlogForm jsonPath="/api/config/Blog.json/blog.blogs" crudApi="/api/blog" />} />
        </Routes>
       
        <FooterLayout2
        companyName="Link Agro Exports"
          about={{
            title: "Quick links",
            items: [
              { label: "Home", href: "/" },
              { label: "About Us", href: "/about" },
              { label: "Product", href: "/product" },
              { label: "Blogs", href: "/blog" },
              { label: "Manufacture", href: "/manufacture" },
            { label: "Contact", href: "/contact" },
            ],
          }}
          
          consumerPolicy={{
            title: "Consumer Policy",
            phone: "+91 7395944679",
            email: "exports@linkagro.in",
            items: [
              { label: "Privacy Policy", href: "/privacy" },
              { label: "Terms of Service", href: "/terms" },
            ],
          }}
          address={{
            lines: ["3/306-A, Thandradevi Pattinam, Paramakudi-623707 Ramnad District."],
            socialLinks: [
              { href: "https://www.instagram.com/linkagroexports", icon: <FaInstagram /> },
              { href: "https://wa.me/917395944679", icon: <FaWhatsapp /> },
            ],
          }}
          updateConfig={{
            id: "version-check",
            title: "Version Update",
            description: "Click to check if you're on the latest version.",
            api: "/api/check-version", // Replace with your actual endpoint or mock
          }}
          mapLink="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d126257.61579297607!2d77.4701604!3d8.5429436!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2sin!4v1754183509920!5m2!1sen!2sin"
          version="1.0.0"
          copyrights="2025 Link Agro Exports. All Rights Reserved. Powered by"
          copyrights_company="Aaran Software"
        />
      </Suspense>
    </div>
  );
}

export default AppRoutes;
