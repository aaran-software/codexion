import React from "react";
import { useInView } from "react-intersection-observer";
import Card2 from "../../../../resources/components/card/Card2";

function About() {
  const [ref1, inView1] = useInView({ triggerOnce: true, threshold: 0.1 });
  const [ref2, inView2] = useInView({ triggerOnce: true, threshold: 0.1 });
  const [ref3, inView3] = useInView({ triggerOnce: true, threshold: 0.1 });
  const [ref4, inView4] = useInView({ triggerOnce: true, threshold: 0.1 });

  const company = [
    {
      title: "Our Strength",
      body: `High Quality Products - Right time delivery - Best price in the market – Tailor made services - 100% Positive Feedback`,
      animate: "animate__animated animate__fadeInLeft animate__fast",
    },

    {
      title: `Our Process`,
      body: `Coconut Husk Feeding – Crushing – Separating Peat from Fiber – Peat Washing – Drying – Compressing as blocks`,
      animate: "animate__animated animate__fadeInRight animate__fast",
    },
  ];
  return (
    <div className="">
      {/* Hero Section */}
      <div className="relative h-[50vh] md:h-[70vh] w-full">
        <img
          src="/assets/Homepage1.jpg"
          alt="Sample"
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-foreground/60" />
        <div className="absolute inset-0 flex items-center">
          <div className="md:w-2/3 px-[10%] text-white space-y-4">
            <h1 className="text-2xl md:text-4xl font-bold">
              Our Premium Coco Peat Products
            </h1>
            <p className="text-sm sm:text-md md:text-lg text-justify">
              Discover Link Agro Exports' diverse range of high-quality coco
              peat products, including 5KG blocks, briquettes, grow bags, husk
              chips, and coir fiber. Engineered for superior water retention,
              low EC, and eco-friendly applications, our products are ideal for
              horticulture, greenhouse farming, and hydroponics. Each product
              comes with detailed specifications and global shipping options to
              suit your agricultural needs.
            </p>
          </div>
        </div>
      </div>

      {/* About Content Section */}
      <div className="text-gray-800 py-16 px-4 md:px-12 lg:px-[10%]">
        <div className="mx-auto">
          <p
            className={`text-lg leading-relaxed first-letter:text-2xl first-letter:font-bold ${
              inView1 ? "animate__animated animate__fadeInDown" : "opacity-0"
            }`}
            ref={ref1}
          >
            We incepted our coco-peat production factory in 2014. Initially, we
            supplied our products to leading exporting companies in Tamil Nadu.
            Later, we decided to cater our services directly to end-users who
            are emerging globally by exporting.
          </p>

          <div className="container px-5 py-10">
            <Card2
              items={company}
              containerStyle={"grid-cols-1 sm:grid-cols-2"}
              lineStyle="w-3 h-12"
            />
          </div>
          <div className="grid md:grid-cols-2 gap-12 mb-12">
            {/* Left Column */}
            <div
              className={`text-lg leading-relaxed mb-8 ${
                inView2 ? "animate__animated animate__fadeInLeft" : "opacity-0"
              }`}
              ref={ref2}
            >
              <h3 className="text-2xl font-semibold text-green-600 mb-4">
                Over a Decade of Excellence
              </h3>
              <p className="text-base leading-relaxed">
                With more than a decade of experience, we specialize in
                supplying premium-grade products for horticulture, farming, and
                landscaping applications across global markets. As one of the
                pioneers in the coir pith industry, Link Agro Exports has
                established a strong international presence by exporting to
                countries like{" "}
                <span className="font-bold text-lg">
                  South Korea, Spain, Vietnam, and Japan
                </span>
                .
                <br />
                <br />
                Our commitment to quality, innovation, and customer satisfaction
                has positioned us as a trusted leader in the field.
              </p>
            </div>

            {/* Right Column - Product List */}
            <div
              className={`bg-gray-50 p-6 rounded-lg shadow-md ${
                inView3 ? "animate__animated animate__fadeInRight" : "opacity-0"
              }`}
              ref={ref3}
            >
              <h3 className="text-2xl font-semibold text-green-600 mb-4">
                What We Deliver
              </h3>
              <ul className="list-disc list-inside space-y-2 text-base">
                <li>Coir Peat Blocks</li>
                <li>Coir Peat Bricks</li>
                <li>Coco Mats</li>
                <li>Coco Discs</li>
                <li>Coir Fibers</li>
                <li>Grow Bags</li>
              </ul>
            </div>
          </div>

          {/* Our Commitment */}
          <div
            className={`bg-green-100 p-6 rounded-lg shadow-md  ${
              inView4 ? "animate__animated animate__fadeInUp" : "opacity-0"
            }`}
            ref={ref4}
          >
            <h3 className="text-2xl font-semibold text-green-700 mb-4">
              Our Commitment
            </h3>
            <p className="text-base leading-relaxed">
              We, at Link Agro Exports, adhere to the highest quality standards
              and consistently produce flawless end products. We believe our
              success depends on delivering the best possible quality to our
              customers.
              <br />
              <br />
              Our experienced professionals are dedicated to providing
              uninterrupted logistics services to our global clients. The most
              active and efficient employees and talented managers strive
              tirelessly to keep Link Agro Exports at the forefront of the
              industry.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default About;
