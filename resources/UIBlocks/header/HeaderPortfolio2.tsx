import { useEffect, useRef, useState } from "react";
import { IoMdMenu } from "react-icons/io";
import { IoClose } from "react-icons/io5";
import { useNavigate } from "react-router-dom";
import { useAppSettings } from "../../../apps/global/useSettings";

type MenuItem = {
  label: string;
  path: string;
};

type HeaderProps = {
  menu: MenuItem[];
};

function HeaderPortfolio2({ menu }: HeaderProps) {
  const settings = useAppSettings();
  if (!settings) return null;

  const defaultLogo = {
    path: "/assets/logo.png",
    height: 20,
    padding: 8,
    position: "center",
    font_size: 2,
    company_name: "",
    text_color: "",
  };

  const logo = settings.logo || defaultLogo;
  const [menuVisible, setMenuVisible] = useState(false);
  const navigate = useNavigate();
  const menuRef = useRef<HTMLUListElement>(null);
  const toggleRef = useRef<HTMLDivElement>(null);
  const handleNav = (path: string) => {
    navigate(path);
    setMenuVisible(false);
  };
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => {
      setScrolled(window.scrollY > 10);

      // Auto-close mobile menu on scroll
      if (menuVisible) {
        setMenuVisible(false);
      }
    };

    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, [menuVisible]);

  // Close menu on outside click
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Node;
      if (
        menuVisible &&
        menuRef.current &&
        !menuRef.current.contains(target) &&
        toggleRef.current &&
        !toggleRef.current.contains(target)
      ) {
        setMenuVisible(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [menuVisible]);
  return (
    <div
      className={`${
        scrolled ? "bg-background text-foreground" : "bg-background/50"
      } flex flex-row justify-between h-20 items-center px-5 py-2 md:py-4 w-full fixed top-0 left-0 z-50 shadow-lg transition-colors duration-300`}
    >
      {/* Logo */}
      <div
        className={`flex items-${logo.position} gap-2 cursor-pointer`}
        onClick={() => navigate("/")}
      >
        {/* Mode 1: Only Logo */}
        {logo.mode === "logo" && (
          <img
            src={logo.path}
            alt="Logo"
            className={`h-${logo.height} p-${logo.padding}`}
          />
        )}

        {/* Mode 2: Only Company Name */}
        {logo.mode === "name" && (
          <h3
            className={`text-${logo.font_size}xl p-${logo.padding} ${logo.text_color} font-bold ${logo.font}`}
          >
            {logo.company_name}
          </h3>
        )}

        {/* Mode 3: Both Logo + Company Name */}
        {logo.mode === "both" && (
          <>
            <img
              src={logo.path}
              alt="Logo"
              className={`h-${logo.height} p-${logo.padding}`}
            />
            <span className={`text-${logo.font_size}xl ${logo.text_color} font-bold ${logo.font}`}>
              {logo.company_name}
            </span>
          </>
        )}
      </div>

      {/* Desktop Menu */}
      <ul className="hidden md:flex flex-row justify-between gap-10 items-center">
        {menu.map((item, index) => (
          <li
            key={index}
            className="relative group cursor-pointer text-lg text-foreground hover:text-primary hover:font-bold transition-all duration-200"
            onClick={() => handleNav(item.path)}
          >
            {item.label}
            <span className="absolute left-0 bottom-0 h-1 w-full transform scale-x-0 origin-left group-hover:scale-x-100 group-hover:bg-primary transition-transform duration-300 ease-in-out" />
          </li>
        ))}
      </ul>

      {/* Mobile Menu Icon */}
      <div
        className="flex md:hidden"
        onClick={() => setMenuVisible(!menuVisible)}
        ref={toggleRef}
      >
        <IoMdMenu size={25} />
      </div>

      {/* Mobile Dropdown */}
      <ul
        ref={menuRef}
        className={`md:hidden transform transition-all duration-400 ease-in-out flex flex-col gap-5 w-full bg-black text-gray-50 p-4 absolute top-0 left-0 z-50 ${
          menuVisible
            ? "translate-y-0 opacity-100"
            : "-translate-y-full opacity-0"
        }`}
      >
        {/* Close */}
        <div
          className="absolute right-0 top-0 mt-10 mr-5"
          onClick={() => setMenuVisible(false)}
        >
          <IoClose size={25} />
        </div>

        {/* Mobile Links */}
        <div className="flex flex-col mt-16">
          {menu.map((item, index) => (
            <div
              key={index}
              className="border-b w-full border-gray-500 p-2 mt-5 hover:text-[#23aa70] last:border-b-0 cursor-pointer"
              onClick={() => handleNav(item.path)}
            >
              {item.label}
            </div>
          ))}
        </div>
      </ul>
    </div>
  );
}

export default HeaderPortfolio2;
