import React from "react";
import PortfolioProduct1 from "../../../../resources/UIBlocks/portfolioProducts/PortfolioProduct1";

const steps = [
  {
    title: "Coconut Husk Sourcing",
    description:
      "We source good-sized coconut husks directly from local coconut farmers who cultivate trees nearby.",
    image: "/assets/manufacturing/1 Coconut Husk Sourcing.jpg",
  },
  {
    title: "Coconut Husk Processing",
    description:
      "The husks are soaked and fed into fiber-making machines, initiating the separation of fiber from peat.",
    image: "/assets/manufacturing/2 Coconut Husk processing.jpg",
  },
  {
    title: "Filtering Fibers from Peat",
    description:
      "Coarse fibers are filtered out during processing to isolate cocopeat particles.",
    image: "/assets/manufacturing/3 Filtering Fibers from Peat.jpg",
  },
  {
    title: "Sieved CocoPeat Separation",
    description:
      "We sieve the remaining material to completely separate fine cocopeat from residual fibers.",
    image: "/assets/manufacturing/4 Seived CocoPeat Separation.jpg",
  },
  {
    title: "Washing Cocopeat",
    description:
      "Cocopeat is washed using soft water to reduce electrical conductivity (EC) for low EC applications.",
    image: "/assets/manufacturing/5 Washing Cocopeat.JPG",
  },
  {
    title: "Drying",
    description:
      "The washed cocopeat is sun-dried thoroughly to preserve its quality and moisture level.",
    image: "/assets/manufacturing/6 Drying.jpg",
  },
  {
    title: "Cocopeat compressed into 5KG Blocks",
    description:
      "Once dried and filtered, the cocopeat is compressed into standard 5KG blocks for easy handling.",
    image: "/assets/manufacturing/7 Cocopeat compressed as 5KG Blocks.jpg",
  },
  {
    title: "5KG Blocks Ready to Ship",
    description:
      "The final compressed blocks are packaged and made ready for export or direct client delivery.",
    image: "/assets/manufacturing/8 5Kg blocks ready to be shipped.jpg",
  },
];

function Manufacture() {
  return (
    <div className="mt-20">
      <div className="relative h-[80vh] w-full">
        {/* Background Image */}
        <img
          src="/assets/Benefits Application 2.jpg"
          alt="Sample"
          className="h-full w-full object-fit"
        />

        {/* Overlay */}
        <div className="absolute inset-0 bg-foreground/60"></div>

        {/* Text Content */}
        <div className="absolute inset-0 flex items-center">
          <div className="md:w-1/2 px-[10%] text-white space-y-4">
            <h1 className="text-4xl font-bold">
              From Husk to Harvest: Inside Our Cocopeat Manufacturing Process
            </h1>
            <p className="text-lg">
              At Link Agro Exports, our cocopeat production journey is a careful
              blend of tradition, innovation, and sustainability. Explore each
              stage of our manufacturing process — from sourcing premium coconut
              husks to delivering high-quality, low EC cocopeat blocks ready for
              global export. Every step is meticulously designed to ensure
              superior quality, purity, and performance in horticulture,
              hydroponics, and farming applications..
            </p>
          </div>
        </div>
      </div>
      <div className="mx-[10%] px-4 py-12">
        <h2 className="text-4xl font-bold text-center mb-12">
          Cocopeat Manufacturing Process
        </h2>
        {steps.map((item, index) => (
          <PortfolioProduct1
            key={index}
            item={item}
            reverse={index % 2 === 1}
          />
        ))}
      </div>
    </div>
  );
}

export default Manufacture;
