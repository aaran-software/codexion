import React from "react";
import DocsWrapper from "../DocsWrapper";
import FooterPortfolio from "../../../../../resources/UIBlocks/footer/footer-portfolio";
import PortfolioFooter3 from "../../../../../resources/UIBlocks/footer/PortfolioFooter3";
import FooterLayout1 from "../../../../../resources/UIBlocks/footer/FooterLayout1";
import FooterLayout2 from "../../../../../resources/UIBlocks/footer/FooterLayout2";
import PortfolioFooter from "../../../../../resources/UIBlocks/footer/PortfolioFooter2";
import {
  FaFacebookF,
  FaTwitter,
  FaInstagram,
  FaEnvelope,
  FaPhoneAlt,
  FaLinkedinIn,
} from "react-icons/fa";
import { AiFillClockCircle } from "react-icons/ai";
import AppFooter from "../../../../../resources/UIBlocks/footer/AppFooter";
import Footer from "../../../../../resources/UIBlocks/footer/Footer";
import { CiFacebook } from "react-icons/ci";
import { FiTwitter } from "react-icons/fi";
function FooterBlock() {
  const contacts = [
    {
      icon: FaPhoneAlt,
      value: "+919894244450",
      href: "https://wa.me/919894244450",
    },
    { icon: AiFillClockCircle, value: "Mon-Sat: 9.00-18.00" },
    {
      icon: FaEnvelope,
      value: "info@logicx.com",
      href: "mailto:info@example.com",
    },
  ];

  const socialLinks = [
    { href: "https://facebook.com", icon: <FaFacebookF /> },
    { href: "https://twitter.com", icon: <FaTwitter /> },
    { href: "https://instagram.com", icon: <FaInstagram /> },
  ];

  const pages = [
    { label: "Home", href: "/" },
    { label: "About", href: "/about" },
    { label: "Services", href: "/services" },
    { label: "Contact", href: "/contact" },
  ];

  const newsletterText = "Subscribe to get the latest updates.";

  return (
    <div className="flex flex-col gap-10">
      
      <DocsWrapper
        title="PortfolioFooter3"
        propDocs={[
          {
            name: "address",
            description: "Company address displayed in the footer.",
          },
          {
            name: "contacts",
            description:
              "Array of contact details. Each item has `icon`, `value`, and optional `href` for links.",
          },
          {
            name: "socialLinks",
            description:
              "Array of social media links with `href` and `icon` (ReactNode).",
          },
          {
            name: "pages",
            description:
              "Navigation links for quick access. Each item has `label` and `href`.",
          },
          {
            name: "newsletterText",
            description: "Text displayed above the newsletter input field.",
          },
          {
            name: "newsletterPlaceholder",
            description:
              "Placeholder text inside the newsletter email input field.",
          },
          {
            name: "newsletterButtonText",
            description: "Text displayed on the newsletter subscribe button.",
          },
          {
            name: "companyName",
            description: "Company name shown in the footer copyright section.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/footer/PortfolioFooter3",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div className="bg-black">
          <PortfolioFooter3
            address="436, Avinashi Road, Near CITU Office, Tiruppur, Tamil Nadu 641602"
            contacts={contacts}
            socialLinks={socialLinks}
            pages={pages}
            newsletterText={newsletterText}
            newsletterPlaceholder="Your email"
            newsletterButtonText="Subscribe"
            companyName="Logicx"
          />
        </div>
      </DocsWrapper>

      <DocsWrapper
        title="AppFooter"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/footer/AppFooter",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <AppFooter />
      </DocsWrapper>

      <DocsWrapper
        title="Footer"
        propDocs={[
          {
            name: "aboutLinks",
            description:
              "Array of navigation links under 'About'. Each item has `label` and `path`.",
          },
          {
            name: "servicesLinks",
            description:
              "Array of navigation links under 'Services'. Each item has `label` and `path`.",
          },
          {
            name: "policyLinks",
            description:
              "Array of navigation links under 'Policy'. Each item has `label` and `path`.",
          },
          {
            name: "contact",
            description:
              "Contact information object with `phone` and `email` fields.",
          },
          {
            name: "address",
            description:
              "Company address details with `company`, `lines` (array of strings), `website`, and `infoEmail`.",
          },
          {
            name: "social",
            description:
              "Social media links object. Example keys: `whatsapp`, `facebook`, `twitter`, `instagram` (all URLs).",
          },
          {
            name: "version",
            description: "Footer version text displayed at the bottom.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/footer/Footer",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div className="bg-black">
          <Footer
            aboutLinks={[
              { label: "Our Company", path: "/contactus" },
              { label: "Brand Assets", path: "/contactus" },
              { label: "Contact Us", path: "/contactus" },
              { label: "Jobs", path: "/contactus" },
              { label: "Events", path: "/contactus" },
              { label: "Blog", path: "/payment" },
              { label: "Customers", path: "/payment" },
              { label: "Level Privacy", path: "/payment" },
            ]}
            servicesLinks={[
              { label: "Support", path: "/payment" },
              { label: "Become a Partner", path: "/payment" },
              { label: "Web Service", path: "/payment" },
              { label: "Software", path: "/payment" },
              { label: "FAQ", path: "/FAQ" },
            ]}
            policyLinks={[
              { label: "Terms of Use", path: "/termsofuse" },
              { label: "Security", path: "/security" },
              { label: "Privacy", path: "/privacy" },
            ]}
            contact={{
              phone: "9894244450",
              email: "support@techmedia.in",
            }}
            address={{
              company: "Tech Media",
              lines: [
                "436, Avinashi Road,",
                "Near CITU Office,",
                "Tiruppur, Tamil Nadu 641602",
              ],
              website: "www.techmedia.in",
              infoEmail: "info@techmedia.in",
            }}
            social={{
              whatsapp: "https://wa.me/9894244450",
              facebook: "https://facebook.com/techmedia",
              twitter: "https://twitter.com/techmedia",
              instagram: "https://instagram.com/techmedia",
            }}
            version="V 1.0.1"
          />
        </div>
      </DocsWrapper>

      <DocsWrapper
        title="FooterPortfolio"
        propDocs={[
          {
            name: "address",
            description:
              "Array of strings representing company address lines to be displayed in the footer.",
          },
          {
            name: "contact",
            description:
              "Array of strings for contact details (e.g., email, phone number).",
          },
          {
            name: "company",
            description:
              "Navigation links under the 'Company' section. Each item has `label` and `link`.",
          },
          {
            name: "project",
            description:
              "Navigation links under the 'Project' section. Each item has `label` and `link`.",
          },
          {
            name: "legal",
            description:
              "Navigation links under the 'Legal' section. Each item has `label` and `link`.",
          },
          {
            name: "brandName",
            description: "The company/brand name displayed in the footer.",
          },
          {
            name: "year",
            description:
              "The year displayed in the copyright section (usually current year).",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/footer/FooterPortfolio",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <FooterPortfolio
          address={["123 Street", "Coimbatore", "Tamil Nadu, India - 641001"]}
          contact={["info@techmedia.in", "+91 9843213500"]}
          company={[
            { label: "Home", link: "home" },
            { label: "About Us", link: "about" },
            { label: "Industry", link: "industry" },
            { label: "Services", link: "services" },
            { label: "Contact", link: "contact" },
          ]}
          project={[
            { label: "ERPNext", link: "/billing" },
            { label: "Ecart", link: "/billing" },
            { label: "Portfolio", link: "/portfolio" },
          ]}
          legal={[
            { label: "Privacy Policy", link: "/privacy" },
            { label: "Terms & Conditions", link: "/terms" },
          ]}
          brandName="Tech Media"
          year={2025}
        />
      </DocsWrapper>

      <DocsWrapper
        title="FooterLayout1"
        propDocs={[
          {
            name: "about",
            description:
              "Section containing quick links. Has a `title` and an array of `items` (each with `label` and `href`).",
          },
          {
            name: "help",
            description:
              "Section for help-related links. Has a `title` and an array of `items` (each with `label` and `href`).",
          },
          {
            name: "consumerPolicy",
            description:
              "Section for consumer policy details. Includes `title`, `phone`, `email`, and an array of `items` (each with `label` and `href`).",
          },
          {
            name: "address",
            description:
              "Company address details. Contains `lines` (array of strings for address lines) and `socialLinks` (array of objects with `href` and `icon`).",
          },
          {
            name: "updateConfig",
            description:
              "Configuration for version update section. Includes `id`, `title`, `description`, and `api` endpoint.",
          },
          {
            name: "version",
            description: "Current version string displayed in the footer.",
          },
          {
            name: "copyrights",
            description:
              "Copyright notice text displayed at the bottom of the footer.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/footer/FooterLayout1",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div>
          <FooterLayout1
            about={{
              title: "Quick links",
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
                {
                  href: "https://instagram.com/linkagro",
                  icon: <FaInstagram />,
                },
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
        </div>
      </DocsWrapper>

      <DocsWrapper
        title="FooterLayout2"
        propDocs={[
          {
            name: "companyName",
            description:
              "Name of the company displayed prominently in the footer.",
          },
          {
            name: "about",
            description:
              "About section with `title` and `items`. Each item has `label` and `href` for navigation.",
          },
          {
            name: "consumerPolicy",
            description:
              "Consumer policy section with `title`, `phone`, `email`, and `items` (each containing `label` and `href`).",
          },
          {
            name: "address",
            description:
              "Company address details. Includes `lines` (array of strings for address lines) and `socialLinks` (array of objects with `icon` and `href`).",
          },
          {
            name: "updateConfig",
            description:
              "Configuration for updates section. Contains `id`, `title`, `description`, and `api` endpoint.",
          },
          {
            name: "mapLink",
            description:
              "Google Maps embed link used to display the company’s location on a map.",
          },
          {
            name: "version",
            description: "Version string displayed in the footer.",
          },
          {
            name: "copyrights",
            description: "Copyright year or text displayed in the footer.",
          },
          {
            name: "copyrights_company",
            description: "Company name displayed alongside the copyright text.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/footer/FooterLayout2",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <FooterLayout2
          companyName="Logicx"
          about={{
            title: "About",
            items: [
              { label: "Who We Are", href: "/about" },
              { label: "Careers", href: "/careers" },
              { label: "Blog", href: "/blog" },
            ],
          }}
          consumerPolicy={{
            title: "Consumer Policy",
            items: [
              { label: "Privacy Policy", href: "/privacy" },
              { label: "Terms of Service", href: "/terms" },
            ],
            phone: "+919894244450",
            email: "info@logicx.com",
          }}
          address={{
            lines: [
              "436, Avinashi Road, Near CITU Office",
              "Tiruppur, Tamil Nadu 641602",
            ],
            socialLinks: [
              { icon: <FaFacebookF />, href: "https://facebook.com" },
              { icon: <FaTwitter />, href: "https://twitter.com" },
              { icon: <FaInstagram />, href: "https://instagram.com" },
            ],
          }}
          updateConfig={{
            id: "update1",
            title: "Latest Updates",
            description:
              "Check out the latest product updates and announcements.",
            api: "/api/updates", // can be your API endpoint
          }}
          mapLink="https://www.google.com/maps/embed?pb=!1m18!..." // Embed map link
          version="1.0.0"
          copyrights="2025"
          copyrights_company="Logicx"
        />
      </DocsWrapper>

      <DocsWrapper
        title="PortfolioFooter"
        propDocs={[
          {
            name: "logo",
            description:
              "Path/URL of the company logo displayed in the footer.",
          },
          {
            name: "newsletterTitle",
            description:
              "Heading text for the newsletter subscription section.",
          },
          {
            name: "newsletterPlaceholder",
            description:
              "Placeholder text inside the newsletter email input field.",
          },
          {
            name: "newsletterButton",
            description: "Label text for the newsletter subscribe button.",
          },
          {
            name: "companyLinks",
            description:
              "Array of company navigation links. Each item includes `label` and `url`.",
          },
          {
            name: "utilityLinks",
            description:
              "Array of utility/support links such as style guide or licenses. Each item includes `label` and `url`.",
          },
          {
            name: "socialLinks",
            description:
              "Array of social media links. Each contains `icon`, `label`, and `url`.",
          },
          {
            name: "copyright",
            description:
              "Text displayed at the bottom of the footer, usually containing copyright notice.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/footer/PortfolioFooter",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <PortfolioFooter
          logo="assets/svg/aaran_logo.svg"
          newsletterTitle="Subscribe Our Newsletter"
          newsletterPlaceholder="Email Address"
          newsletterButton="Submit Now"
          companyLinks={[
            { label: "Features", url: "#" },
            { label: "Pricing", url: "#" },
            { label: "Testimonials", url: "#" },
            { label: "FAQ’s", url: "#" },
          ]}
          utilityLinks={[
            { label: "Style Guide", url: "#" },
            { label: "Licenses", url: "#" },
            { label: "Changelog", url: "#" },
          ]}
          socialLinks={[
            { icon: <FaFacebookF />, label: "Facebook", url: "#" },
            { icon: <FaInstagram />, label: "Instagram", url: "#" },
            { icon: <FaTwitter />, label: "Twitter", url: "#" },
            { icon: <FaLinkedinIn />, label: "LinkedIn", url: "#" },
          ]}
          copyright="Copyright © 2025 Aaran."
        />
      </DocsWrapper>

    </div>
  );
}

export default FooterBlock;
