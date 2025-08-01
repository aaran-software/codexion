import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import HeaderPortfolio2 from "../../../resources/components/header/HeaderPortfolio2";
import Footer from "../../../resources/components/footer/Footer";
import Product from "./pages/Product";
import Contact from "./pages/Contact";
import About from "./pages/about";
function AppRoutes() {
  return (
    <div>
      <HeaderPortfolio2
        menu={[
          { label: "Home", path: "/" },
          { label: "About Us", path: "/about" },
          { label: "Product", path: "/product" },
          { label: "Manufacture", path: "/manufacture" },
          { label: "Contact", path: "/contact" },
        ]}
      />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/product" element={<Product />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/about" element={<About />} />
      </Routes>
      <Footer />
    </div>
  );
}

export default AppRoutes;
