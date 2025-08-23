import { Routes, Route } from "react-router-dom";
import ScrollToTop from "../../../resources/components/common/scrolltotop";
import {
  FaEnvelope,
  FaInstagram,
  FaPhoneAlt,
  FaWhatsapp,
} from "react-icons/fa";
import React, { lazy, Suspense } from "react";
import LoadingScreen from "../../../resources/components/loading/LoadingScreen";
import BlogForm from "./pages/blog/BlogForm";
import PortfolioFooter3 from "../../../resources/UIBlocks/footer/PortfolioFooter3";
import { AiFillClockCircle } from "react-icons/ai";
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
  // footer

  const contacts = [
    {
      icon: FaPhoneAlt,
      value: "+91 7395944679",
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
      <Suspense fallback={<LoadingScreen image={"/assets/logo/logo.svg"} />}>
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
          <Route
            path="/blogForm"
            element={
              <BlogForm
                jsonPath="/api/config/Blog.json/blog.blogs"
                crudApi="/api/blog"
              />
            }
          />
        </Routes>

        <PortfolioFooter3
          address="3/306-A, Thandradevi Pattinam, Paramakudi-623707, Ramnad District"
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
