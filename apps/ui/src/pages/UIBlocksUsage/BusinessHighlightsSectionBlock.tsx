import DocsWrapper from "../DocsWrapper";
import BusinessHighlightsSection from "../../../../../resources/UIBlocks/businessHighlights/BusinessHighlightsSection";
import BusinessHighlightsSection2 from "../../../../../resources/UIBlocks/businessHighlights/BusinessHighlightsSection2";

function BusinessHighlightsSectionBlock() {
  const companyInfo = [
    {
      icon: "/assets/svg/client.svg",
      count: 310,
      symbol: "k",
      field: "Client Request",
    },
    {
      icon: "/assets/svg/member.svg",
      count: 150,
      symbol: "",
      field: "Experts",
    },
    {
      icon: "/assets/svg/experience.svg",
      count: 15,
      symbol: "",
      field: "Experience",
    },
    { icon: "/assets/svg/award.svg", count: 120, symbol: "", field: "Award" },
  ];

  const cta = {
    title: "Start your ERP journey with a free consultation today.",
    buttonText: "Enquiry Now",
    buttonLink: "#contact",
  };
  return (
    <div>
      <DocsWrapper
        title="BusinessHighlightsSection"
        propDocs={[
          {
            name: "companyInfo",
            description:
              "Array of statistic objects with `icon`, `count`, `symbol`, and `field` to display key company metrics.",
          },
          {
            name: "backgroundImage",
            description: "Background image URL for the section.",
          },
          {
            name: "cta",
            description:
              "Call-to-action object with `title`, `buttonText`, and `buttonLink`.",
          },
        ]}
        paths={{
          file: "resources/UIBlocks/businessHighlights/BusinessHighlightsSection",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <BusinessHighlightsSection
          companyInfo={companyInfo}
          backgroundImage="/assets/bg.jpg"
          cta={cta}
        />
      </DocsWrapper>

      <DocsWrapper
        title="BusinessHighlightsSection2"
        propDocs={[
          {
            name: "backgroundImage",
            description: "Background image URL for the section.",
          },
          {
            name: "cta",
            description:
              "Call-to-action object containing the following properties:\n" +
              "- `title`: The main heading for the section.\n" +
              "- `subTitle` (optional): Additional description text.\n" +
              "- `buttonText`: Text displayed on the CTA button.\n" +
              "- `buttonLink`: Scroll ID or external link for the CTA button.\n" +
              "- `contacts` (optional): Array of contact objects with `icon`, `title`, and `value` to display contact info.",
          },
        ]}
        paths={{
          file: "resources/UIBlocks/businessHighlights/BusinessHighlightsSection2",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <BusinessHighlightsSection2
          backgroundImage="/images/office-bg.jpg"
          cta={{
            title: "Start your ERP journey today!",
            subTitle: "Get in touch with our experts for a free consultation.",
            buttonText: "CONTACT US",
            buttonLink: "#contact",
            contacts: [
              {
                icon: "/assets/svg/phone.svg",
                title: "Call Us",
                value: "+91 12345 67890",
              },
              {
                icon: "/assets/svg/email.svg",
                title: "Email Us",
                value: "support@example.com",
              },
            ],
          }}
        />
      </DocsWrapper>
    </div>
  );
}

export default BusinessHighlightsSectionBlock;
