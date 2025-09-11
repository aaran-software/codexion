import React from "react";
import DocsWrapper from "../DocsWrapper";
import PortfolioContact from "../../../../../resources/UIBlocks/contact/PortfolioContact";
import Contact1 from "../../../../../resources/UIBlocks/contact/Contact1";
import Contact2 from "../../../../../resources/UIBlocks/contact/Contact2";
import { FaIndustry } from "react-icons/fa";
import { IoBusiness } from "react-icons/io5";
import { TbTruckDelivery } from "react-icons/tb";
function ContactBlock() {
  return (
    <div>
      <DocsWrapper
        title="1. PortfolioContact"
        propDocs={[
          {
            name: "mapSrc",
            description:
              "Google Maps embed URL used as the source for the iframe map display.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/contact/PortfolioContact",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <PortfolioContact
          mapSrc={
            "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d557.9677738430108!2d77.33628450184978!3d11.1131330605361!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3ba907abde6b9b0b%3A0x15ed72f683d49e9b!2sTech%20Media%20Retail!5e1!3m2!1sen!2sin!4v1755945911404!5m2!1sen!2sin"
          }
        />
      </DocsWrapper>

      <DocsWrapper
        title="2. Contact1"
        propDocs={[
          {
            name: "mapSrc",
            description:
              "Google Maps embed URL used as the source for the iframe map display.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/contact/PortfolioContact",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <Contact1
          addresses={[
            {
              title: "Registered Office",
              details: `Link Agro Exports
No: 3/306-A, Thandradevi Pattinam,
Paramakudi-623707
Ramnad District.`,
              icon: IoBusiness,
            },
            {
              title: "Logistics Centre",
              details: `Link Agro Exports
274, North Masi Street,
Madurai – 625001`,
              icon: TbTruckDelivery,
            },
            {
              title: "Plant Address",
              details: `Tamarakularm,
Uchipuli Post,
Ramanathapuram District
Tamilnadu - 623534`,
              icon: FaIndustry,
            },
          ]}
          socialLinks={[
            {
              id: "instagram",
              href: "linkagroexports",
              img: "/assets/svg/instagram.svg",
              alt: "Instagram",
            },
            {
              id: "whatsapp",
              href: "917395944679",
              img: "/assets/svg/whatsapp.svg",
              alt: "WhatsApp",
            },
            {
              id: "email",
              href: "exports@linkagro.in",
              img: "/assets/svg/email.svg",
              alt: "WhatsApp",
            },
            {
              id: "phone",
              href: "9894864679",
              img: "/assets/svg/phone.svg",
              alt: "WhatsApp",
            },
          ]}
          iconSize="w-8 h-8"
        />
      </DocsWrapper>

      <DocsWrapper
        title="3. Contact2"
        propDocs={[
          {
            name: "addresses",
            description: "Physical address displayed in the contact section.",
          },
          {
            name: "email",
            description:
              "Array of email objects with label (display text) and value (mailto link).",
          },
          {
            name: "phone",
            description:
              "Array of phone objects with label (display number) and value (tel number).",
          },
          {
            name: "subTitle",
            description:
              "Optional subtitle displayed below the main title. Example: 'Get In Touch With Us'.",
          },
          {
            name: "title",
            description: "Main title of the section. Defaults to 'Contact Us'.",
          },
          {
            name: "description",
            description:
              "Optional description paragraph to provide context about contacting.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/contact/Contact1",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Contact Section",
            "Service Pages",
            "Landing Pages",
            "Portfolio",
          ],
        }}
      >
        <Contact2
          addresses={`No: 3/306-A, Thandradevi Pattinam,
Paramakudi-623707
Ramnad District.`}
          email={[{ label: "demo@gmail.com", value: "demo@gmail.com" }]}
          phone={[{ label: "+91 98760 12345", value: "919876012345" }]}
          subTitle="Get In Touch With Us"
          description="Lorem ipsum dolor sit amet consectetur adipisicing elit. Eligendi error excepturi cum quod provident ipsam."
        />
      </DocsWrapper>
    </div>
  );
}

export default ContactBlock;
