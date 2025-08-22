import React, { JSX } from "react";
import { IconType } from "react-icons";
import { href } from "react-router-dom";

type ContactInfo = {
  icon: IconType;
  value: string;
  href?:string
};

type SocialLink = {
  href: string;
  icon: JSX.Element;
};

type PageLink = {
  label: string;
  href: string;
};

type FooterProps = {
  address: string;
  contacts: ContactInfo[];
  socialLinks?: SocialLink[];
  pages?: PageLink[];
  newsletterText?: string;
  newsletterPlaceholder?: string;
  newsletterButtonText?: string;
  companyName: string;
  companyLogo: string;
};

const PortfolioFooter3: React.FC<FooterProps> = ({
  address,
  contacts,
  socialLinks,
  pages,
  newsletterText,
  newsletterPlaceholder = "Enter your email",
  newsletterButtonText = "Subscribe",
  companyName,
  companyLogo,
}) => {
  return (
    <footer className="bg-gray-800 text-white pt-12 pb-6">
      {/* Top Contact Section */}

      <div className="flex flex-col md:flex-row justify-evenly gap-4 md:px-[10%]">
        {contacts.map((item, idx) => {
          const IconComponent = item.icon;
          return (
            <div
              key={idx}
              className="flex items-center gap-2 border-b-2 border-ring/30 p-5 border-b-primary w-full text-sm"
            >
              <IconComponent className="w-12 h-12 p-2 shrink-0  hover:scale-110" />
              <a href={item.href}  target="_blank" className="text-lg font-bold border-l-2 pl-2 border-primary cursor-pointer">
                {item.value}
              </a>
            </div>
          );
        })}
      </div>

      {/* Main Footer */}
      <div className="md:px-[10%] mx-auto px-5 grid grid-cols-1 md:grid-cols-3 gap-8 mt-8">
        {/* Company Info */}
        <div className="space-y-4">
          <img src={companyLogo} alt="" className="w-[50%] hover:scale-105" />
          <p>{address}</p>
          <div className="flex gap-3 mt-2">
            {socialLinks?.map((item, idx) => (
              <a
                key={idx}
                href={item.href}
                target="_blank"
                rel="noreferrer"
                className="p-2 rounded-full bg-primary text-background hover:opacity-90 transition hover:scale-105"
              >
                {item.icon}
              </a>
            ))}
          </div>
        </div>

        {/* Pages */}
        <div className="space-y-2">
          <h3 className="font-bold text-lg">Pages</h3>
          <ul className="space-y-1">
            {pages?.map((page, idx) => (
              <li key={idx}>
                <a href={page.href} className="text-primary">
                  {page.label}
                </a>
              </li>
            ))}
          </ul>
        </div>

        <div className="flex flex-col gap-4">
          <h3 className="font-bold text-lg">Subscribe</h3>
          <p>{newsletterText}</p>
          <form className="flex items-center h-max bg-white rounded-full overflow-hidden w-full ">
            <input
              type="email"
              placeholder={newsletterPlaceholder}
              className="flex-1 px-2 py-3 text-gray-800 outline-none"
            />
            <button
              type="submit"
              className="bg-gradient-to-r from-primary to-primary/30 hover:to-primary px-6 py-3 m-1 cursor-pointer text-foreground whitespace-normal font-medium rounded-r-full"
            >
              {newsletterButtonText}
            </button>
          </form>
        </div>
      </div>

      {/* Footer Bottom */}
      <div className="text-center border-t border-ring/30 text-gray-400 mt-10 pt-4">
        &copy; {new Date().getFullYear()} {companyName} All rights reserved.
      </div>
    </footer>
  );
};

export default PortfolioFooter3;
