import { lazy } from "react";
import HeroBanner2 from "../../../../resources/UIBlocks/banner/HeroBanner2";
import AboutSection from "../../../../resources/UIBlocks/about/AboutSection";
import BusinessHighlightsSection2 from "../../../../resources/UIBlocks/businessHighlights/BusinessHighlightsSection2";
import AnimatedCard from "../../../../resources/UIBlocks/card/AnimatedCard";
import FlexColCard from "../../../../resources/UIBlocks/card/FlexColCard";
const CardShowcase = lazy(
  () => import("../../../../resources/UIBlocks/CardShowcase")
);
import Roadmap from "../../../../resources/UIBlocks/Roadmap/Roadmap";
import {
  Rocket,
  Target,
  Code2,
  Layers,
  ShieldCheck,
  Repeat,
  Leaf,
  Users,
  BadgeCheck,
  Clock,
  Brush,
  Ship,
  Scissors,
  Droplets,
  Shirt,
} from "lucide-react";
import { GiSewingMachine } from "react-icons/gi";
const BrandMarquee = lazy(
  () => import("../../../../resources/components/marquee/BrandMarquee")
);
import SimpleBanner from "../../../../resources/UIBlocks/banner/SimpleBanner";
import ProcessSection from "../../../../resources/UIBlocks/process/ProcessSection";
import NexusCard from "../../../../resources/UIBlocks/card/NexusCard";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();
  const bannerImages = [
    { id: "1", image: "/assets/banner/banner1.jpg" },
    { id: "2", image: "/assets/banner/banner2.jpg" },
    { id: "3", image: "/assets/banner/banner1.jpg" },
  ];

  const whyChooseUs = [
    {
      title: "Fast Delivery",
      description: "Get your products delivered within 24 hours.",
      image: "/assets/banner/banner1.jpg",
      hoverColor: "from-indigo-500 to-purple-500",
    },
    {
      title: "Secure Payments",
      description: "Your transactions are encrypted and secure.",
      image: "/assets/banner/banner1.jpg",
      hoverColor: "from-green-500 to-teal-500",
    },
    {
      title: "24/7 Support",
      description: "Our team is here to help anytime you need.",
      image: "/assets/banner/banner1.jpg",
      hoverColor: "from-pink-500 to-red-500",
    },
  ];

  const ourExpertise = [
    {
      id: "tab1",
      label: "Strategy",
      title: "Business Strategy",
      description:
        "We craft growth-focused strategies that align with your company’s vision and market opportunities.",
      navLink: "/services/strategy",
      image: "/assets/banner/banner1.jpg",
      subImages: ["/assets/banner/banner1.jpg", "/assets/banner/banner1.jpg"],
    },
    {
      id: "tab2",
      label: "Design",
      title: "Creative Design",
      description:
        "Our design team delivers stunning visuals and smooth user experiences across all platforms.",
      navLink: "/services/design",
      image: "/assets/banner/banner1.jpg",
      subImages: ["/assets/banner/banner1.jpg", "/assets/banner/banner1.jpg"],
    },
    {
      id: "tab3",
      label: "Development",
      title: "Modern Development",
      description:
        "We build scalable web and mobile apps using the latest frameworks, ensuring long-term performance.",
      navLink: "/services/development",
      image: "/assets/banner/banner1.jpg",
      subImages: ["/assets/banner/banner1.jpg", "/assets/banner/banner1.jpg"],
    },
  ];

  const projects = [
    {
      title: "ERP Services We Offer",
      image: "/assets/banner/banner2.jpg",
      services: [
        {
          heading: "Implementation & Deployment",
          description:
            "We handle the complete setup of ERP—on cloud or on-premise—with user access control, email alerts, backup, and SSL configuration.",
        },
        {
          heading: "Module Customization",
          description:
            "Customize modules like Sales, Inventory, Accounting, HR, and Manufacturing to suit your unique workflow.",
        },
        {
          heading: "Tally Integration",
          description:
            "Bridge ERP with Tally for GST filing, financial reports, and accounting sync.",
        },
        {
          heading: "WooCommerce & eCommerce Integration",
          description:
            "Automate sales, stock, and invoices between your online store and ERP.",
        },
        {
          heading: "Training & Support",
          description:
            "Get in-depth training for staff, and ongoing technical support via call, email, or remote tools.",
        },
      ],
    },
    {
      title: "Ecart – E-Commerce Platform",
      image: "/assets/banner/banner1.jpg",
      services: [
        {
          heading: "Custom Storefront",
          description:
            "Build and manage a fully customizable online store tailored to your brand identity.",
        },
        {
          heading: "Single Vendor Store",
          description:
            "Set up your own branded e-commerce store where you manage all products, orders, and customers directly.",
        },
        {
          heading: "Multi-Vendor Marketplace",
          description:
            "Launch a scalable marketplace where multiple sellers can register, list products, manage their own inventory, and receive payments through a controlled admin system.",
        },
        {
          heading: "Category & Product Management",
          description:
            "Easily manage and organize large catalogs with support for 2000+ products across multiple categories without performance issues.",
        },
        {
          heading: "Secure Payments",
          description:
            "Integrated payment gateways with safe checkout and multi-currency support.",
        },
        {
          heading: "Order Tracking",
          description:
            "Track orders and deliveries in real-time with automated status updates.",
        },
        {
          heading: "Mobile Friendly",
          description:
            "Responsive design for a smooth shopping experience across all devices.",
        },
      ],
    },
    {
      title: "QBill (Quick Bill)",
      image: "/assets/banner/banner2.jpg",
      services: [
        {
          heading: "GST-Compliant Invoicing",
          description: "Generate professional invoices with tax compliance.",
        },
        {
          heading: "POS Integration",
          description: "Fast and simple point-of-sale billing system.",
        },
        {
          heading: "Customer & Vendor Management",
          description: "Maintain customer/vendor data with ease.",
        },
        {
          heading: "Reports & Analytics",
          description: "Get detailed sales, expenses, and stock reports.",
        },
      ],
    },
  ];

  const roadmapData = [
    {
      year: "01",
      title: "RECEPTION OF THE YARN",
      description:
        "Organic, recycled & BCI cotton yarn, Recycled polyester etc",
      icon: <Users className="w-5 h-5 text-white" />,
      color: "#F59E0B",
    },
    {
      year: "02",
      title: "KNITTING",
      description: "Delivered scalable ERP solution for a global manufacturer.",
      icon: <Shirt className="w-5 h-5 text-white" />,
      color: "#10B981",
    },
    {
      year: "03",
      title: "DYEING & FINISHING",
      description: "Azo free dyes & chemicals",
      icon: <Droplets className="w-5 h-5 text-white" />,
      color: "#3B82F6",
    },
    {
      year: "04",
      title: "CUTTING",
      description: "Automatic cutting capabilities",
      icon: <Scissors className="w-5 h-5 text-white" />,
      color: "#EC4899",
    },
    {
      year: "05",
      title: "SEWING",
      description: "Type of construction: Tubular/ Side Seam",
      icon: <GiSewingMachine className="w-5 h-5 text-white" />,
      color: "#10B981",
    },
    {
      year: "06",
      title: "SCREEN PRINTING & EMBELLISHMENT",
      description: "Wide range of screenprinting and embellishment techniques",
      icon: <Brush className="w-5 h-5 text-white" />,
      color: "#F97316",
    },
    {
      year: "07",
      title: "PACKING & WORLDWIDE SHIPPING",
      description:
        "We can ship directly from our facility to any part of the world",
      icon: <Ship className="w-5 h-5 text-white" />,
      color: "#10B981",
    },
  ];

  const brands = [
    { name: "DELL" },
    { name: "HP" },
    { name: "BENQ" },
    { name: "SAMSUNG" },
    { name: "APPLE" },
  ];
  return (
    <div className="mt-20 lg:mt-30">
      <HeroBanner2
        images={bannerImages}
        interval={5000}
        title="Welcome to Codexion"
        description="We build smart solutions that accelerate your business growth."
        videoPath={"/assets/banner/bannervideo.mp4"}
      />

      {/* <div className="my-10">
        <AnimatedCard
          title="Why Choose Us"
          description="We provide high quality services for your business"
          cards={whyChooseUs}
        />
      </div> */}

      <div className="mx-4 py-10 md:mx-[10%]">
        <FlexColCard heading="Our Expertise" items={ourExpertise} />
      </div>

      <div className="mx-4 py-10 md:mx-[10%]">
        <CardShowcase items={projects} />
      </div>

      <BusinessHighlightsSection2
        backgroundImage="/assets/banner/banner1.jpg"
        cta={{
          title: "Start Your ERP Journey Today!",
          subTitle: "Get in touch with our experts for a free consultation.",
          buttonText: "CONTACT US",
          buttonLink: "#contact",
        }}
      />

      <div className="px-4 py-10">
        <ProcessSection
          items={[
            {
              title: "EASY PRODUCT DEVELOPMENT",
              description:
                "Dedicated team to convert your design into a sample product",
              icon: (
                <Code2 className="w-8 h-8 md:w-16 md:h-16 text-indigo-600" />
              ),
            },
            {
              title: "SMALL MOQ",
              description:
                "We work with small MOQ's Starting from 500pcs/Style/Colour",
              icon: (
                <Layers className="w-8 h-8 md:w-16 md:h-16 text-indigo-600" />
              ),
            },
            {
              title: "QUALITY",
              description:
                "Stage by stage quality checks ensure you High Quality Garments",
              icon: (
                <ShieldCheck className="w-8 h-8 md:w-16 md:h-16 text-indigo-600" />
              ),
            },
            {
              title: "FLEXIBILITY",
              description: "Always willing to adapt to our customer needs.",
              icon: (
                <Repeat className="w-8 h-8 md:w-16 md:h-16 text-indigo-600" />
              ),
            },
            {
              title: "SUSTAINABILITY",
              description:
                "We are taking all necessary steps towards sustainability such as Use of Solar energy, Zero discharge of effluents, use of organic/recycled materials etc.",
              icon: <Leaf className="w-8 h-8 md:w-16 md:h-16 text-green-600" />,
            },
            {
              title: "EMPLOYEE WELFARE",
              description:
                "Proud to have a workforce that has a long-term relationship with us, built on mutual trust & development",
              icon: (
                <Users className="w-8 h-8 md:w-16 md:h-16 text-indigo-600" />
              ),
            },
            {
              title: "COMPLIANCE CERTIFICATIONS",
              description:
                "We work with OEKO-TEX, GOTS, BCI, SEDEX, GRS & BSCI Certifications.",
              icon: (
                <BadgeCheck className="w-8 h-8 md:w-16 md:h-16 text-indigo-600" />
              ),
            },
            {
              title: "SHORT LEAD TIME",
              description:
                "With a vertical setup we deliver your products in a short lead time.",
              icon: (
                <Clock className="w-8 h-8 md:w-16 md:h-16 text-indigo-600" />
              ),
            },
          ]}
          title="What Makes PVR INTERNATIONAL Different?"
        />
      </div>

      <NexusCard
        sectionTitle="Ensuring the safety of
our people, customers
and the environment"
        sectionDescription="PVR INTERNATIONAL is recognized for its
genuine dedication to business growth
through the support of its people, fostering
positive relationships with the local
community, and minimizing the
environmental impact resulting from its
operations.
We have initiated the adoption of clean
energy sources, implemented a rigorous
Zero Discharge Policy, and actively
collaborate with various social compliance
organizations to ensure equitable and
sustainable work practices."
        leftClassName="text-left"
        rightClassName="grid-rows-3"
        items={[
          {
            logo: "/assets/award/bci.jpg",
            alt: "React",
            title: "React",
            className: "bg-[#3E2F89] col-span-2",
          },
          {
            logo: "/assets/award/organic.png",
            alt: "Hostinger",
            title: "Hostinger",
            className: "bg-[#c71313]",
          },
          {
            logo: "/assets/award/sedex.png",
            alt: "MySQL",
            title: "MySQL",
            className: "bg-[#67c090]",
          },
          {
            logo: "/assets/award/bci.jpg",
            alt: "Node.js",
            title: "Node.js",
            className: "bg-[#ea2264] col-span-2",
          },
          {
            logo: "/assets/award/bci.jpg",
            alt: "TailwindCSS",
            title: "TailwindCSS",
            className: "bg-[#f5babb] col-span-2",
          },
          {
            logo: "/assets/award/sedex.png",
            alt: "GitHub",
            title: "GitHub",
            className: "bg-[#b2b0e8]",
          },
        ]}
      />

      <div className="px-4">
        <AboutSection
        subtitle="About Textilery"
        title="We Provide The Best Textile Industry Since 2005"
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        experienceYears={25}
        counterDuration={2000}
        experienceLabel="Years Of Experiences"
        leftImage="/assets/banner/banner1.jpg"
        rightImage="/assets/banner/banner2.jpg"
        features={[
          { id: "f1", text: "Best Quality Standards" },
          { id: "f2", text: "100% Satisfaction Guarantee" },
          { id: "f3", text: "Quality Control System" },
          { id: "f4", text: "Commitment to Customers" },
          { id: "f5", text: "Highly Professional Team" },
        ]}
        founderName="Miya Draper"
        founderRole="PVR Groups"
        founderImage="/assets/user.png"
        buttonLabel="About Us"
        onButtonClick={() => navigate("/about")}
      />
      </div>

      <div className="py-10">
        <Roadmap
          items={roadmapData}
          RoadmapHeading={"Journey Of Our Garments"}
        />
      </div>

      <div className="grid md:grid-cols-2 gap-12 px-4 lg:px-[10%] text-justify py-5">
        {/* Left Column */}
        <div className={`text-lg leading-relaxed `}>
          <h3 className="text-2xl font-semibold text-primary mb-4">
            Vertical Integration
          </h3>
          <p>
            PVR INTERNATIONAL offers a vertically-integrated manufacturing
            process that allows direct control over our processes and a
            continuous improvement mindset enable resource and operational
            efficiencу.
          </p>
          <p>
            This model sets us apart from other apparel manufacturers and allow
            us to offer our global customers with high quality products at
            competitive costs.
          </p>
          <p>
            Facility capabilities include knitting, dyeing, and finishing
            techniques such as peaching, raising, sueding for open width and
            tubular fabric, cut & sew, laser cutting, screen printing, digital
            printing, embroidery, and embellishment.
          </p>
        </div>

        {/* Right Column - Product List */}
        <div
          className={`bg-highlight1 p-6 rounded-lg shadow-md text-lg text-highlight1-foreground`}
        >
          <h3 className="text-2xl font-semibold  mb-4">Our Customers</h3>
          <p>
            Our company manufactures products for renowned global athletic and
            lifestyle brands according to their specifications, offering a whole
            range of products at competitive prices while ensuring social and
            environmental aspects are adhered.
          </p>
          <p>
            Our customers have come to trust PVR INTERNATIONAL as a strategic
            partner for reasons including our personalized customer service,
            sustainability commitment and manuacturing expertise.
          </p>
        </div>
      </div>
      <div className="my-10 md:my-20 py-10 md:py-10 bg-primary/10">
        <BrandMarquee
          type="big-text"
          text="Our Client"
          brands={brands}
          speed={30}
          height={16}
        />
      </div>

      <div className="mx-4 py-20 md:mx-[10%]">
        <SimpleBanner
          title={"Turning Complexity into Simplicity"}
          imgPath={"/assets/h1.webp"}
          path={"contact"}
          buttonLabel={"Start Now"}
          className="bg-purple-800"
          buttonStyle="bg-foreground text-background "
          textStyle="text-background"
        />
      </div>
    </div>
  );
}

export default Home;
