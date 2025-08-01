import PortfolioProduct1 from "../../../../resources/UIBlocks/portfolioProducts/PortfolioProduct1";

function Product() {
  const portfolioData = [
    {
      image: "/assets/sample1.jpg",
      title: "Creative Design",
      description: "Modern and minimal portfolio layout for agencies.",
    },
    {
      image: "/assets/sample2.jpg",
      title: "Tech Landing",
      description: "Landing page optimized for SaaS and startups.",
    },
    {
      image: "/assets/sample3.jpg",
      title: "E-commerce Showcase",
      description: "Product-focused layout for online stores.",
    },
  ];
  return (
    <div>
      <div className="px-[10%]">
        <PortfolioProduct1 items={portfolioData} />
      </div>
    </div>
  );
}

export default Product;
