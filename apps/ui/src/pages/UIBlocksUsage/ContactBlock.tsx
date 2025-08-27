import React from "react";
import DocsWrapper from "../DocsWrapper";
import PortfolioContact from "../../../../../resources/UIBlocks/contact/PortfolioContact";

function ContactBlock() {
  return (
    <div>
      <DocsWrapper
        title="AnimatedCard"
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
    </div>
  );
}

export default ContactBlock;
