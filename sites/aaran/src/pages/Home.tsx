import { lazy } from "react";
import HeroBanner from "../../../../resources/UIBlocks/banner/HeroBanner";
import StartingSection1 from "../../../../resources/UIBlocks/startingsection/StartingSection1";
import TestimonialCarousel from "../../../../resources/UIBlocks/testimonials/TestimonialCard";
import ContactCard from "../../../../resources/UIBlocks/card/ContactCard";
import Team2 from "../../../../resources/layouts/team/team2";
import TypingText from "../../../../resources/AnimationComponents/TypingText";
import Roadmap from "../../../../resources/UIBlocks/timeline/Roadmap";
import { Rocket, Award, Target, Users } from "lucide-react"; // optional icons
import HalfOrbit from "../../../../resources/UIBlocks/Orbit/HalfOrbit";
import { FaBullseye, FaEye, FaHandshake } from "react-icons/fa";
import HighlightCardWithIcon from "../../../../resources/UIBlocks/card/HighlightedCardwithIcon";
import Consultant from "../../../../resources/UIBlocks/consultant/consultant";

const TransparentCard = lazy(
  () => import("../../../../resources/UIBlocks/card/TransparentCard")
);
const AnimatedCard = lazy(
  () => import("../../../../resources/UIBlocks/card/animatedCard")
);
const Pricing = lazy(
  () => import("../../../../resources/UIBlocks/pricingcard/Pricing")
);
const PortfolioContact = lazy(
  () => import("../../../../resources/UIBlocks/contact/PortfolioContact")
);
const FlexColCard = lazy(
  () => import("../../../../resources/UIBlocks/card/FlexColCard")
);
const ProjectCarousel = lazy(
  () => import("../../../../resources/UIBlocks/carousel/ProjectCarousel")
);

const BrandMarquee = lazy(
  () => import("../../../../resources/components/marquee/BrandMarquee")
);
function Home() {
  const brands = [
    { name: "DELL" },
    { name: "HP" },
    { name: "BENQ" },
    { name: "SAMSUNG" },
    { name: "APPLE" },
  ];

  const VisionMission = [
    {
      title: "Our Vision",
      text: "To be a global leader in software innovation, creating solutions that empower businesses and enrich lives.",
      icon: <FaEye />,
    },
    {
      title: "Our Mission",
      text: "Deliver cutting-edge, scalable software solutions that drive efficiency, growth, and digital transformation for our clients.",
      icon: <FaBullseye />,
    },
    {
      title: "Our Values",
      text: "Integrity, innovation, collaboration, and excellence guide every project we undertake and every relationship we build.",
      icon: <FaHandshake />,
    },
  ];

  // Company Info Card
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
    title:
      "We craft powerful ERP software and stunning portfolios to help your business grow.",
    buttonText: "Enquire Now",
    buttonLink: "#contact",
  };

  const cardData = [
    {
      title: "ERPNext Customization",
      description:
        "Tailored ERPNext solutions to streamline your business operations with automation, reporting, and scalability.",
      image: "assets/svg/animatesvg/dashboard.svg",
      hoverColor: "from-primary via-primary/0 to-primary/0",
    },
    {
      title: "QBill – Smart Billing",
      description:
        "Simplify invoicing, track payments, and manage accounts effortlessly with our secure billing software.",
      image: "assets/svg/animatesvg/qbilling.svg",
      hoverColor: "from-primary via-primary/0 to-primary/0",
    },
    {
      title: "eCart Solutions",
      description:
        "Custom e-commerce platforms with product management, payment integration, and advanced analytics.",
      image: "assets/svg/animatesvg/ecart.svg",
      hoverColor: "from-primary via-primary/0 to-primary/0",
    },
  ];
  const plans = [
    {
      id: "free",
      name: "Free",
      price: 0,
      description: "Basic features for individuals",
      features: [
        { id: 1, text: "Access to core features" },
        { id: 2, text: "1 Project" },
        { id: 3, text: "Community Support" },
        { id: 4, text: "Basic Analytics" },
        { id: 5, text: "Email Alerts" },
        { id: 6, text: "Single User" },
        { id: 7, text: "Basic Templates" },
        { id: 8, text: "Limited Storage" },
      ],
    },
    {
      id: "pro",
      name: "Pro",
      price: 15,
      description: "Advanced features for professionals",
      highlight: true, // highlight this plan
      features: [
        { id: 1, text: "Everything in Free" },
        { id: 2, text: "Unlimited Projects" },
        { id: 3, text: "Priority Support" },
        { id: 4, text: "Advanced Analytics" },
        { id: 5, text: "Team Collaboration" },
        { id: 6, text: "Export Data" },
        { id: 7, text: "Custom Branding" },
        { id: 8, text: "Cloud Backup" },
        { id: 9, text: "Role Management" },
      ],
    },
    {
      id: "premium",
      name: "Premium",
      price: 30,
      description: "All features for large teams",
      features: [
        { id: 1, text: "Everything in Pro" },
        { id: 2, text: "Dedicated Manager" },
        { id: 3, text: "Custom Integrations" },
        { id: 4, text: "API Access" },
        { id: 5, text: "Advanced Security" },
        { id: 6, text: "24/7 Support" },
        { id: 7, text: "Custom Workflows" },
        { id: 8, text: "Unlimited Storage" },
      ],
    },
  ];

  const data = [
    {
      id: "sales",
      label: "Sales",
      title: "Define and automate your sales process",
      description:
        "Give your sales team the means to sell efficiently across channels with a structured and repeatable sales process.",
      navLink: "/sales",
      image: "assets/dashboard.png",
      subImages: [
        "assets/react.svg",
        "/assets/react.svg",
        "/assets/react.svg",
        "/assets/react.svg",
      ],
    },
    {
      id: "marketing",
      label: "Marketing",
      title: "Plan and execute marketing campaigns",
      description:
        "Automate campaign workflows, capture leads, and analyze performance for better ROI.",
      navLink: "/marketing",
      image: "assets/dashboard.png",
      subImages: ["assets/react.svg"],
    },
    {
      id: "service",
      label: "Service",
      title: "Deliver better customer support",
      description:
        "Track tickets, resolve issues faster, and improve customer satisfaction.",
      navLink: "/service",
      image: "assets/dashboard.png",
      subImages: ["/assets/react.svg"],
    },
  ];

  const product = [
    {
      id: 1,
      title: "Linkagro Exports Portfolio",
      description: "A modern personal portfolio site.",
      category: "website",
      image: "/assets/product/linkagro.jpg",
      link: "https://fabulous-queijadas-684a73.netlify.app/",
    },
    {
      id: 2,
      title: "Tech media eCart",
      description: "Mobile app for shopping.",
      category: "app",
      image: "/assets/product/techmedia.png",
      link: "https://techmedia.in",
    },
    {
      id: 3,
      title: "Logicx Portfolio",
      description: "Corporate business website.",
      category: "website",
      image: "/assets/product/logicx.png",
      link: "https://logicx.in/",
    },
    {
      id: 4,
      title: "Aaran Portfolio",
      description: "Corporate business website.",
      category: "website",
      image: "/assets/product/aaran.png",
      link: "https://aaransoftware.netlify.app/",
    },
    {
      id: 5,
      title: "ERPNext",
      description: "Corporate business website.",
      category: "app",
      image: "/assets/product/erp.png",
      link: "https://example.com/company",
    },
  ];

  const teamMembers = [
    {
      name: "Sundar D",
      designation: "CEO",
      description: "Leads the company with vision and integrity.",
      image: "/assets/team/sundar.webp",
      circleColor: "#3B82F6", // blue
      circlePosition: "bottom-left" as const,
    },
    {
      name: "Haris R",
      designation: "Business Analyst",
      description: "Brings creativity to every project.",
      image: "/assets/team/haris.webp",
      circleColor: "#10B981", // green
      circlePosition: "top-left" as const,
    },
    {
      name: "Muthu Kumaran R",
      designation: "Software Developer",
      description: "Builds robust and scalable solutions.",
      image: "/assets/team/muthukumaran.jpg",
      circleColor: "#F59E0B", // yellow
      circlePosition: "top-right" as const,
    },
    {
      name: "Saran R",
      designation: "Full Stack Developer",
      description: "Connects our brand with the world.",
      image: "/assets/team/saran.webp",
      circleColor: "#EF4444", // red
      circlePosition: "bottom-right" as const,
    },
    {
      name: "Mukila K",
      designation: "Customer Success Manager",
      description: "Builds robust and scalable solutions.",
      image: "/assets/team/mukila.webp",
      circleColor: "#F59E0B", // yellow
      circlePosition: "top-right" as const,
    },
    {
      name: "Arunesh S",
      designation: "Full Stack Developer",
      description: "Connects our brand with the world.",
      image: "/assets/team/arunesh.webp",
      circleColor: "#EF4444", // red
      circlePosition: "bottom-right" as const,
    },
  ];

  const Testimonials = [
    {
      id: 1,
      company: "TechCorp",
      logo: "/assets/team/haris.webp",
      feedback: "The software streamlined our operations...",
      client: "John Doe, CTO",
    },
    {
      id: 2,
      company: "HealthPlus",
      logo: "/assets/team/saran.webp",
      feedback: "We reduced costs by 25% after implementing...",
      client: "Sarah Lee, Operations Head",
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

  return (
    <div className="overflow-x-auto">
      <div id="home">
        <StartingSection1 />
      </div>

      <div className="px-4 md:px-[10%] ">
        <FlexColCard items={data} heading="automate your sales" />
      </div>

      <div id="about" className="px-4 py-20 lg:px-[10%]">
        <Roadmap
          items={roadmapData}
          RoadmapHeading={"Our Journey & Future Roadmap"}
        />

        <div className="mt-10">
          {/* vision mission section */}
          <HighlightCardWithIcon
            className="grid-cols-1 md:grid-cols-3"
            sectionTitle=""
            items={VisionMission}
          />
        </div>
      </div>

      <div className="py-20 ">
        <Consultant
          companyInfo={companyInfo}
          backgroundImage="/assets/bg.jpeg"
          cta={cta}
        />
      </div>

      <div className="mt-24"></div>

      <AnimatedCard
        cards={cardData}
        title={"Our Products"}
        description={
          "Explore our wide range of products crafted with quality and precision. Designed to meet your needs and deliver the best experience."
        }
      />

      <div className="mt-20">
        <TransparentCard image="assets/dashboard.png" />
      </div>

      <div className="mt-20 px-4 md:px-[10%]">
        <Pricing plans={plans} />
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

      <div className="py-20">
        <HalfOrbit
          centerImage="/assets/tech/tech.jpeg"
          items={[
            { name: "React", icon: "/assets/tech/react.png" },
            { name: "Node.js", icon: "/assets/tech/node.png" },
            { name: "Python", icon: "/assets/tech/python.jpeg" },
            { name: "JavaScript", icon: "/assets/tech/js.png" },
            { name: "Tailwind", icon: "/assets/tech/tailwind.png" },
            { name: "Frappe", icon: "/assets/tech/frappe.png" },
            { name: "TypeScript", icon: "/assets/tech/ts.png" },
          ]}
          arcAngle={Math.PI / 1.0}
        />
      </div>

      <div className="px-4 flex flex-col gap-5 md:px-[10%]" id="product">
        <TypingText
          fixedMessage="Choose From"
          messages={[
            "Predesigned Templates",
            "Software Modules",
            "Ready-Made Layouts",
          ]}
          typingSpeed={100}
          pauseTime={1500}
          className="text-4xl md:text-5xl font-bold text-gray-900"
        />

        {/* Description */}
        <p className=" text-gray-700 text-base md:text-lg leading-relaxed my-10 text-center">
          Use our pre-designed templates to kickstart your project. Customize
          colors, layouts, and styles to create a professional and inviting
          interface for your users. All templates are fully responsive and ready
          to integrate into your software or website.
        </p>
        <ProjectCarousel
          products={product}
          autoSlide={true}
          autoSlideInterval={4000}
        />
        <HeroBanner
          badgeText="⚡ Trusted Protection for Every Doorstep"
          title="Your safety is our mission. Your trust is our commitment"
          subtitle="Click below to schedule your free risk assessment and learn how we can help protect your world."
          buttonText="Start Protecting Your Presence"
          buttonLink="/contact"
        />
      </div>

      <div className="px-2 lg:px-[10%] py-10">
        <Team2 members={teamMembers} />
      </div>

      <div className="my-25">
        <TestimonialCarousel
          heading={"What Our Client Says"}
          testimonials={Testimonials}
          autoSlide={true}
        />
      </div>

      <div id="contact" className="px-4 py-20 md:px-[10%]">
        <PortfolioContact
          mapSrc={`https://www.google.com/maps/embed?pb=!1m10!1m8!1m3!1d2448.1917350159647!2d80.0961770382818!3d13.082598423466093!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2sin!4v1756699621503!5m2!1sen!2sin`}
        />

        <ContactCard
          contact={{
            address: "Mahavishnu Nagar, Tiruppur, Tamil Nadu",
            phone: ["+91 98765 43210", "+91 91234 56789"], // multiple numbers
            email: ["hello@example.com", "support@example.com"], // multiple emails
          }}
        />
      </div>
    </div>
  );
}

export default Home;
