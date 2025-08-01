import DynamicCard from "../../../../resources/components/card/DynamicCard";
import Carousel from "../../../../resources/components/carousel";
import Button from "../../../../resources/components/button/Button";
function Home() {
  const images = [
    "/assets/sample1.jpg",
    "/assets/sample2.jpg",
    "/assets/sample3.jpg",
  ];

  const product = [
    {
      image: "/assets/sample1.jpg",
      title: "Creative Design",
    },
    {
      image: "/assets/sample2.jpg",
      title: "Tech Landing",
    },
    {
      image: "/assets/sample3.jpg",
      title: "E-commerce Showcase",
    },
  ];
  return (
    <div className="mt-20">
      <Carousel autoSlide autoSlideInterval={4000} startIndex={0}>
        {images.map((src, index) => (
          <img
            key={index}
            src={src}
            alt={`Slide ${index + 1}`}
            className="w-full h-[400px] object-cover"
          />
        ))}
      </Carousel>

      <div className="px-[10%]">
        <h1 className="text-center font-bold text-4xl my-5">Our Products</h1>
        <DynamicCard
          Card={product}
          containerStyle="grid-cols-1 sm:grid-cols-2 md:grid-cols-3"
        />
      </div>

      <Button
        label="View More"
        path="/product"
        className="border border-ring/40 !rounded-full block mx-auto my-3 w-max"
      />

      <div className="relative h-[80vh] w-full">
        {/* Background Image */}
        <img
          src="/assets/sample1.jpg"
          alt="Sample"
          className="h-full w-full object-cover"
        />

        {/* Overlay */}
        <div className="absolute inset-0 bg-foreground/60"></div>

        {/* Text Content */}
        <div className="absolute inset-0 flex items-center">
          <div className="w-1/2 px-[10%] text-white space-y-4">
            <h1 className="text-4xl font-bold">Title</h1>
            <p className="text-lg">Description goes here.</p>
            <Button
              label="Read More"
              path="/about"
              className="border border-ring/40"
            />
          </div>
        </div>
      </div>

      <div className="px-[10%]">
        <h1 className="text-center font-bold text-4xl my-5">Manufacturing</h1>
        <DynamicCard
          Card={product}
          containerStyle="grid-cols-1 sm:grid-cols-2 md:grid-cols-3"
          rounded
        />
      </div>
      <Button
        label="View More"
        path="/product"
        className="border border-ring/40 !rounded-full block mx-auto my-3 w-max"
      />
    </div>
  );
}

export default Home;
