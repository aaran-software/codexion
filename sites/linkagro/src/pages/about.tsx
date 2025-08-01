import React from 'react';

function About() {
  return (
    <div className="mt-10">
      {/* Hero Section */}
      <div className="relative h-[80vh] w-full">
        <img
          src="/assets/Homepage1.jpg"
          alt="Sample"
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-foreground/60" />
        <div className="absolute inset-0 flex items-center">
          <div className="md:w-1/2 px-[10%] text-white space-y-4">
            <h1 className="text-4xl font-bold">
              Our Premium Coco Peat Products
            </h1>
            <p className="text-lg">
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
      <div className="bg-white text-gray-800 py-16 px-4 md:px-12 lg:px-24">
        <div className="max-w-6xl mx-auto">
          <p className="text-lg leading-relaxed mb-8">
            We incepted our coco-peat production factory in 2014. Initially, we
            supplied our products to leading exporting companies in Tamil Nadu.
            Later, we decided to cater our services directly to end-users who
            are emerging globally by exporting.
          </p>

          <div className="grid md:grid-cols-2 gap-12 mb-12">
            {/* Left Column */}
            <div>
              <h3 className="text-2xl font-semibold text-green-600 mb-4">
                Over a Decade of Excellence
              </h3>
              <p className="text-base leading-relaxed">
                With more than a decade of experience, we specialize in
                supplying premium-grade products for horticulture, farming, and
                landscaping applications across global markets. As one of the
                pioneers in the coir pith industry, Link Agro Exports has
                established a strong international presence by exporting to
                countries like South Korea, Spain, Vietnam, and Japan.
                <br />
                <br />
                Our commitment to quality, innovation, and customer
                satisfaction has positioned us as a trusted leader in the
                field.
              </p>
            </div>

            {/* Right Column - Product List */}
            <div className="bg-gray-50 p-6 rounded-lg shadow-md">
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
          <div className="bg-green-100 p-6 rounded-lg shadow-md">
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
