import { Link } from "react-router-dom";
import { FaPhone } from "react-icons/fa";
import { MdEmail } from "react-icons/md";
import React from "react";

interface FooterColumn {
  title: string;
  items: { label: string; href: string }[];
}
interface FooterLayoutProps {
  about: FooterColumn;
  companyName: string;
  address: {
    lines: string[];
    socialLinks: { icon: React.ReactNode; href: string }[];
  };
  phone: string;
  email: string;
  mapLink: string;
  version: string;
  copyrights: string;
  copyrights_company: string;
}

const FooterLayout2: React.FC<FooterLayoutProps> = ({
  about,
  companyName,
  // consumerPolicy,
  address,
  version,
  copyrights,
  copyrights_company,
  mapLink,
  phone,
  email,
}) => {
  const renderColumn = (column: FooterColumn) => (
    <div>
      <h5 className="font-bold mb-2 text-xl text-primary">{column.title}</h5>
      <ul className="space-y-1">
        {column.items.map((item, idx) => (
          <li key={idx}>
            <Link to={item.href} className="hover:underline text-white">
              {item.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );

  return (
    <footer className="bg-neutral-900 text-white text-sm mt-5">
      <div className="grid grid-cols-1 px-[5%] sm:grid-cols-2 md:grid-cols-3 gap-6 py-10">
        {/* Address */}

        <div>
          <h5 className="font-bold mb-2 text-2xl text-primary">
            {companyName}
          </h5>
          <p className="text-white leading-6">
            {address.lines.map((line, idx) => (
              <span key={idx}>
                {line.split(",").map((part, i, arr) => (
                  <React.Fragment key={i}>
                    {part.trim()}
                    {i < arr.length - 1 && ","} 
                    {i < arr.length - 1 && <br />}{" "}
                    
                  </React.Fragment>
                ))}
                {idx < address.lines.length - 1 && <br />}{" "}
                {/* break between lines */}
              </span>
            ))}
          </p>
          <p className="my-3">
            <a href={`tel:${phone}`} className="flex items-center gap-1">
              <FaPhone className="rotate-90 shrink-0 w-5 h-5" /> {phone}
            </a>
            <br />
            <a href={`mailto:${email}`} className="flex items-center gap-1">
              <MdEmail className="shrink-0 w-5 h-5" /> {email}
            </a>
          </p>
          <div className="flex gap-3 mt-1">
            {address.socialLinks.map((link, idx) => (
              <a
                key={idx}
                href={link.href}
                target="_blank"
                rel="noopener noreferrer"
              >
                <div className="w-10 h-10 p-2 hover:-translate-y-1 transition-transform cursor-pointer text-white text-2xl">
                  {link.icon}
                </div>
              </a>
            ))}
          </div>
        </div>

        {renderColumn(about)}

        {/* Consumer Policy */}
        <div>
          <h1 className="font-bold mb-2 text-xl text-primary">Visit Us</h1>
          <iframe
            src={mapLink}
            className="w-[100%] md:w-[80%]"
            height="max"
            loading="lazy"
          ></iframe>
        </div>
      </div>

      <div className="flex flex-row gap-3 justify-between border-t border-white/10">
        <div></div>
        <div className="text-center py-3 bg-neutral-900">
          &copy; {copyrights}{" "}
          <a href="https://my.codexsun.com/" target="_blank">
            {copyrights_company}
          </a>
        </div>
        <div className="block my-auto text-background/50 pr-5 cursor-pointer whitespace-nowrap">
          V {version}
        </div>
      </div>
    </footer>
  );
};

export default FooterLayout2;
