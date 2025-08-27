import DocsWrapper from "../DocsWrapper";
import Consultant from "../../../../../resources/UIBlocks/consultant/Consultant";

function ConsultantBlock() {
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
        title="Consultant"
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
          file: "/resources/UIBlocks/consultant/Consultant",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <Consultant
          companyInfo={companyInfo}
          backgroundImage="/assets/software.avif"
          cta={cta}
        />
      </DocsWrapper>
    </div>
  );
}

export default ConsultantBlock;
