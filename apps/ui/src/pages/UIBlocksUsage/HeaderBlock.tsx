import React from "react";
import DocsWrapper from "../DocsWrapper";
import AppFooter from "../../../../../resources/UIBlocks/footer/AppFooter";
import AppHeader from "../../../../../resources/UIBlocks/header/AppHeader";
import ContactHeader from "../../../../../resources/UIBlocks/header/ContactHeader";
import HeaderPortfolio from "../../../../../resources/UIBlocks/header/header-portfolio";
import HeaderPortfolio2 from "../../../../../resources/UIBlocks/header/HeaderPortfolio2";
import TransparentHeader from "../../../../../resources/UIBlocks/header/TransparentHeader";
import Header from "../../../../../resources/UIBlocks/header/Header";
import { FaEnvelope, FaPhoneAlt } from "react-icons/fa";
import { AiFillClockCircle } from "react-icons/ai";
import settings from "../../../public/settings.json";
import { useNavigate } from "react-router-dom";
function HeaderBlock() {
  const navigate = useNavigate();

  const contactItems = [
    {
      icon: FaPhoneAlt,
      value: "+91 98765 43210",
      href: "https://wa.me/919543439311",
    },
    { icon: AiFillClockCircle, value: "Mon-Sat: 9.00-18.00" },
    {
      icon: FaEnvelope,
      value: "info@logicx.com",
      href: "mailto:info@example.com",
    },
  ];

  const logo = {
    ...settings.logo,
    position: settings.logo.position as "left" | "center" | "right",
    mode: settings.logo.mode as "logo" | "name" | "both",
  };

  // Example menu items
  const menuItems = [
    { label: "My Profile", path: "/profile", icon: "user" },
    { label: "My Orders", path: "/orders", icon: "plus" },
    { label: "Wishlist", path: "/wishlist", icon: "like" },
    { label: "Logout", path: "/", icon: "logout" },
  ];
  const logout = async () => {
    console.log("Logging out...");
    // ...logout logic, e.g., clear tokens
    navigate("/login");
  };
  // Example mock user
  const user = { name: "John Doe", id: 123 };

  return (
    <div className="flex flex-col gap-10">
      <DocsWrapper
        title="AppFooter"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/header/AppFooter",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <AppHeader />
      </DocsWrapper>

      <DocsWrapper
        title="ContactHeader"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/header/ContactHeader",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <ContactHeader contacts={contactItems} buttonLabel="Get a Quote" />
      </DocsWrapper>


      {/* <DocsWrapper
        title="HeaderPortfolio"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/header/AppFooter",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <HeaderPortfolio
          menu={[
            { label: "Home", path: "home" },
            { label: "About Us", path: "about" },
            { label: "Services", path: "services" },
            { label: "Contact", path: "contact" },
          ]}
          contact={contactItems}
          contactHeader={false}
        />
      </DocsWrapper> */}

      <DocsWrapper
        title="Header"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/header/Header",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <Header
          logo={logo}
          showLogin={false} // Toggle login and cart section
          user={user} // Pass null if no user logged in
          logout={logout}
          menuItems={menuItems}
          showSearch={true} // Toggle search bar
          onSearchApi={`/api/resource/Catalog Details?fields=["name","image_1","price"]`}
          onNavigate={(path) => navigate(path)}
        />
      </DocsWrapper>

      {/* <DocsWrapper
        title="HeaderPortfolio2"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/header/HeaderPortfolio2",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
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

      </DocsWrapper>
      <DocsWrapper
        title="TransparentHeader"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/header/TransparentHeader",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
         <TransparentHeader
          menu={[
            { label: "Home", path: "home" },
            { label: "About Us", path: "about" },
            { label: "Product", path: "product" },
            { label: "Contact", path: "contact" },
          ]}
        />
      </DocsWrapper> */}

    </div>
  );
}

export default HeaderBlock;
