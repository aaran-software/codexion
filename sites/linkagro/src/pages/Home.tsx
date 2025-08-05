import DynamicCard from "../../../../resources/components/card/DynamicCard";
import Carousel from "../../../../resources/components/carousel";
import Button from "../../../../resources/components/button/Button";
import Card2 from "../../../../resources/components/card/Card2";

function Home() {
  const images = [
    "/assets/Benefits Application 2.jpg",
    "/assets/Homepage4.jpg",
    "/assets/banner1.jpg",
    "/assets/banner2.jpg",
    "/assets/banner3.jpg",
  ];

  const product = [
    {
      image: "/assets/product/bb6501.png",
      title: "COCO PEAT BRIQUETTE (650Grams)",
      animate: "animate__animated animate__fadeInDown animate__faster",
    },
    {
      image: "/assets/product/coco-coins.png",
      title: "COCOPEAT GROW BAGS & DISCS",
      animate: "animate__animated animate__fadeInDown animate__fast",
    },
    {
      image: "/assets/product/CoirFiber.jpeg",
      title: "COCO COIR FIBER",
      animate: "animate__animated animate__fadeInDown animate__slow",
    },
    {
      image: "/assets/product/Cocopeat5kgBlock.png",
      title: "Coco Peat 5KG Blocks",
      animate: "animate__animated animate__fadeInUp animate__slow",
    },
    {
      image: "/assets/product/Coco husk chips block 1.png",
      title: "COCO HUSK CHIPS",
      animate: "animate__animated animate__fadeInUp animate__fast",
    },
    {
      image: "/assets/product/Cocodiscsseedling.png",
      title: "Coco disc seedling",
      animate: "animate__animated animate__fadeInUp animate__faster",
    },
  ];

  const company = [
    {
      title: "Trusted Manufacturer & Exporter of Coco Peat Products",
      body: `Pioneers in the industry
since 2014, exporting
globally to South Korea,
Japan, Vietnam & more.`,
      animate: "animate__animated animate__fadeInLeft animate__fast",
    },
    {
      title: `Premium-Grade
Products for Horticulture
& Agriculture`,
      body: `Delivering Coir Peat
Blocks, Bricks, Grow Bags,
Discs & Fibers tailored for
nurseries, greenhouses, and
landscaping.`,
      animate: "animate__animated animate__fadeInUp animate__fast",
    },
    {
      title: `State-of-the-Art
Manufacturing Facility in
Tamil Nadu`,
      body: `From coconut husk sourcing
to final compression, we
maintain strict quality
standards with customizable
packing options.`,
      animate: "animate__animated animate__fadeInRight animate__fast",
    },
  ];
  return (
    <div className="">
      <Carousel autoSlide autoSlideInterval={4000} startIndex={0}>
        {images.map((src, index) => (
          <img
            key={index}
            src={src}
            alt={`Slide ${index + 1}`}
            className="w-full h-[60vh] md:h-[80vh] object-fit"
          />
        ))}
      </Carousel>

      <h1 className="text-center font-bold text-4xl mt-5 animate__animated animate__fadeInDown animate__fast">Link Agro Exports</h1>
      <div className="container mx-auto px-5 md:px-[10%]">
        <Card2
          items={company}
          containerStyle={"grid-cols-1 sm:grid-cols-3"}
          lineStyle="w-3 h-12"
        />
      </div>
      <div className="relative h-[80vh] sm:h-[60vh] md:h-[70vh] mt-10 w-full">
        {/* Background Image */}
        <img
          src="/assets/Homepage1.jpg"
          alt="Sample"
          className="h-full w-full object-cover"
        />

        {/* Overlay */}
        <div className="absolute inset-0 bg-foreground/60"></div>

        {/* Text Content */}
        <div className="absolute inset-0 flex items-center animate__animated animate__fadeInRight animate__fast">
          <div className="md:w-2/3 px-[10%] text-white space-y-4">
            <h1 className="text-4xl font-bold">Link Agro Exports</h1>
            <p className="text-sm md:text-md">
              Link Agro Exports is a distinguished manufacturer and exporter of
              high-quality coco peat products. Our plant is located in Uchipuli,
              Tamilnadu which is known for its conducive climate for coconut
              cultivation, particularly for tender coconut (green coconut). And
              this place has excellent ground water source. Hence this
              geographical feasibility enables us producing good quality coir
              and coco-peat products.
            </p>
            <Button
              label="Read More"
              path="/about"
              className="border border-ring/40"
            />
          </div>
        </div>
      </div>

      <div className="px-5 lg:px-[10%]">
        <h1 className="text-center font-bold text-4xl my-5">Our Products</h1>
        <DynamicCard
          Card={product}
          containerStyle="grid-cols-1 sm:grid-cols-2 md:grid-cols-3"
        />
      </div>

      {/* <Button
        label="View More"
        path="/product"
        className="border border-ring/40 !rounded-full block mx-auto my-3 w-max"
      /> */}
    </div>
  );
}

export default Home;
