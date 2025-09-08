import { lazy } from "react";
import HeroBanner2 from "../../../../resources/UIBlocks/banner/HeroBanner2";
import AboutSection from "../../../../resources/UIBlocks/about/AboutSection";
import BusinessHighlightsSection2 from "../../../../resources/UIBlocks/businessHighlights/BusinessHighlightsSection2";
import AnimatedCard from "../../../../resources/UIBlocks/card/AnimatedCard";
import FlexColCard from "../../../../resources/UIBlocks/card/FlexColCard";
const CardShowcase = lazy(
  () => import("../../../../resources/UIBlocks/CardShowcase")
);
import Roadmap from "../../../../resources/UIBlocks/timeline/Roadmap";
import { Rocket, Target, Users } from "lucide-react";

const BrandMarquee = lazy(
  () => import("../../../../resources/components/marquee/BrandMarquee")
);
import SimpleBanner from "../../../../resources/UIBlocks/banner/SimpleBanner";

function Home() {
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
      year: "2015",
      title: "Founded the Company",
      description: "Started with a small team of passionate developers.",
      icon: <Users className="w-5 h-5 text-white" />,
      color: "#F59E0B", // amber
    },
    {
      year: "2018",
      title: "First Enterprise Client",
      description: "Delivered scalable ERP solution for a global manufacturer.",
      icon: <Target className="w-5 h-5 text-white" />,
      color: "#10B981", // green
    },
    {
      year: "2023",
      title: "AI & Cloud Innovation",
      description: "Launched SaaS products leveraging AI and cloud computing.",
      icon: <Rocket className="w-5 h-5 text-white" />,
      color: "#3B82F6", // blue
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
    <div className="mt-20">
      <HeroBanner2
        images={bannerImages}
        interval={5000}
        title="Welcome to Codexion"
        description="We build smart solutions that accelerate your business growth."
        videoPath={"/assets/banner/bannervideo.mp4"}
      />

      <div className="my-10">
        <AnimatedCard
          title="Why Choose Us"
          description="We provide high quality services for your business"
          cards={whyChooseUs}
        />
      </div>

      <div className="mx-4 py-10 md:mx-[10%]">
        <FlexColCard heading="Our Expertise" items={ourExpertise} />
      </div>
      <div className="mx-4 py-10 md:mx-[10%]">
        <CardShowcase items={projects} />
      </div>

<div className="py-10">
<Roadmap
        items={roadmapData}
        RoadmapHeading={"Our Journey & Future Roadmap"}
      />
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
        onButtonClick={() => alert("Go to About Page")}
      />

      <BusinessHighlightsSection2
        backgroundImage="/assets/banner/banner1.jpg"
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
              href:"tel:+911234567890"
            },
            {
              icon: "/assets/svg/email.svg",
              title: "Email Us",
              value: "support@example.com",
              href:"mailto:support@example.com"
            },
          ],
        }}
      />

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
