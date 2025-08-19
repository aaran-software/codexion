import React, { lazy, Suspense, useState } from "react";
import Plan from "../../../../resources/components/website/plan";
import Carousel from "../../../../resources/components/carousel";
import { Link as ScrollLink } from "react-scroll";
import ScrollToTop from "../../../../resources/components/common/scrolltotopbutton";
const Team = lazy(() => import("../../../../resources/layouts/portfolio/team"));
const Articles = lazy(
  () => import("../../../../resources/components/website/articles")
);
const Review = lazy(
  () => import("../../../../resources/components/website/review")
);
const About = lazy(() => import("./About"));
const Contact = lazy(() => import("./Contact"));
const HeaderPortfolio = lazy(
  () => import("../../../../resources/UIBlocks/header/header-portfolio")
);
const FooterPortfolio = lazy(
  () => import("../../../../resources/UIBlocks/footer/footer-portfolio")
);
const CardShowcase = lazy(
  () => import("../../../../resources/UIBlocks/CardShowcase")
);
import LoadingScreen from "../../../../resources/components/loading/LoadingScreen";

const Home: React.FC = () => {
  // Company About Card

  const [card] = useState<{ icon: string; label: string }[]>([
    { icon: "/assets/svg/ideas.svg", label: "ERP Strategy" },
    { icon: "/assets/svg/research.svg", label: "Industry Expertise" },
    { icon: "/assets/svg/seo.svg", label: "E-Commerce" },
    { icon: "/assets/svg/design.svg", label: "Custom Design" },
    { icon: "/assets/svg/support.svg", label: "Training & Support" },
  ]);

  const [whyChoose] = useState<{ text: string }[]>([
    {
      text: "20+ Years of Proven Experience in both software development and product distribution.",
    },
    { text: "Dual Expertise – Technology + Trading." },
    { text: "Scalable Solutions – From startups to enterprises." },
    {
      text: "Long-Term Client Partnerships built on trust, innovation, and support.",
    },
  ]);

  // Company Info Card
  const [companyInfo] = useState<
    { icon: string; count: string | number; field: string }[]
  >([
    { icon: "/assets/svg/client.svg", count: "310k", field: "Client Request" },
    { icon: "/assets/svg/member.svg", count: 150, field: "Experts" },
    { icon: "/assets/svg/experience.svg", count: 15, field: "Experience" },
    { icon: "/assets/svg/award.svg", count: 120, field: "Award" },
  ]);

  const slides = [
    {
      id: 1,
      title1: "Smarter Operations.",
      title2: "Simplified ERP.",
      description:
        "Tailored ERP solutions to streamline your business—from inventory to invoicing, everything in one place.",
      buttonLabel: "GET STARTED",
      buttonPath: "/contact",
      image: "/assets/svg/home-hero.svg",
      bgClass: "bg-website-background text-website-foreground",
    },
    {
      id: 2,
      title1: "Powerful Integration.",
      title2: "Limitless Growth.",
      description:
        "Connect your ERP with Tally, WooCommerce, payment gateways, and more—for seamless business automation.",
      buttonLabel: "LEARN MORE",
      buttonPath: "/about",
      image: "/assets/svg/create.svg",
      bgClass: "bg-website-background text-website-foreground",
    },
    {
      id: 3,
      title1: "Custom Workflows.",
      title2: "Exact Fit ERP.",
      description:
        "We don’t just deploy—our domain experts craft workflows for retail, textile, manufacturing & service sectors.",
      buttonLabel: "EXPLORE MORE",
      buttonPath: "/design",
      image: "/assets/svg/home-hero.svg",
      bgClass: "bg-website-background text-website-foreground",
    },
    {
      id: 4,
      title1: "Actionable Insights.",
      title2: "Better Decisions.",
      description:
        "Leverage analytics and reporting tools to make data-driven decisions and boost efficiency.",
      buttonLabel: "DISCOVER HOW",
      buttonPath: "/analytics",
      image: "/assets/svg/slider.svg",
      bgClass: "bg-website-background text-website-foreground",
    },
    {
      id: 5,
      title1: "Reliable Support.",
      title2: "Real Results.",
      description:
        "From cloud hosting to training and migration, we stay with you at every step of your ERP journey.",
      buttonLabel: "GET IN TOUCH",
      buttonPath: "/contact-us",
      image: "/assets/svg/slider.svg",
      bgClass: "bg-website-background text-website-foreground",
    },
  ];

  const portfolio = [
    "/assets/sample1.jpg",
    "/assets/sample2.jpg",
    "/assets/sample4.jpg",
    "/assets/sample1.jpg",
    "/assets/sample2.jpg",
    "/assets/sample4.jpg",
  ];
  const [sliderVisible, setSliderVisible] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);

  const industries = [
    {
      title: "Software Industry Solutions",
      image: "/assets/industry/software.png",
      description:
        "We deliver tailored ERP, billing, and e-commerce solutions designed to streamline operations and accelerate growth for software companies.",
      services: [
        {
          heading: "ERP for IT Services",
          description:
            "Manage projects, timesheets, client billing, and HR seamlessly with ERP integration.",
        },
        {
          heading: "License & Subscription Management",
          description:
            "Automate software license distribution, renewals, and subscription billing.",
        },
        {
          heading: "Client & Support Portal",
          description:
            "Provide a customer portal for ticketing, updates, and self-service support.",
        },
        {
          heading: "Analytics & Reporting",
          description:
            "Get real-time insights into project profitability, resource utilization, and client satisfaction.",
        },
      ],
    },
    {
      title: "Electronics Retail & Distribution",
      image: "/assets/industry/electronics.png",
      description:
        "Our ERP and e-commerce platforms empower electronics wholesalers, retailers, and distributors to manage high-volume inventory and multi-channel sales.",
      services: [
        {
          heading: "Inventory & Warehouse Management",
          description:
            "Handle thousands of SKUs with batch, serial number, and warranty tracking.",
        },
        {
          heading: "Multi-Channel E-Commerce",
          description:
            "Sell electronics online and offline with unified stock, order, and billing management.",
        },
        {
          heading: "Vendor & Customer Management",
          description:
            "Easily manage suppliers, purchase orders, and bulk customer accounts.",
        },
        {
          heading: "GST-Compliant Billing",
          description:
            "Generate invoices with GST compliance, discounts, and flexible tax rules.",
        },
        {
          heading: "After-Sales Service",
          description:
            "Track warranties, repairs, and replacements with automated service workflows.",
        },
      ],
    },
  ];

  const projects = [
    {
      title: "ERP Services We Offer",
      image: "/assets/service/erpnext.png",
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
      image: "/assets/service/ecart.png",
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
      title: "QBilling (Quick Billing)",
      image: "/assets/service/qbilling.png",
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

  const teamData = [
    {
      image: "/assets/sample1.jpg",
      name: "Desirae Dias",
      designation: "CEO",
      bio: "Visionary leader driving innovation and excellence.",
    },
    {
      image: "/assets/sample1.jpg",
      name: "Madelyn Torff",
      designation: "Marketing Head",
      bio: "Expert in growth strategies and brand management.",
    },
    {
      image: "/assets/sample1.jpg",
      name: "Tiana Gouse",
      designation: "Project Manager",
      bio: "Ensures projects are delivered with precision and care.",
    },
    {
      image: "/assets/sample1.jpg",
      name: "Livia Passaquin",
      designation: "Director",
      bio: "Guides business strategy and organizational success.",
    },
  ];

  return (
    <main>
      <Suspense fallback={<LoadingScreen image={"/assets/logicx_logo.png"} />}>
        <HeaderPortfolio
          logo={{
            path: "/assets/logo.png",
            mode: "logo",
            company_name: "Codexion",
            font_size: 2,
            height: 60,
            padding: 6,
            position: "center",
          }}
          menu={[
            { label: "Home", path: "home" },
            { label: "About Us", path: "about" },
            { label: "Industry", path: "industry" },
            { label: "Services", path: "services" },
            { label: "Contact", path: "contact" },
          ]}
        />

        <section id="home" className="pt-20">
          {/* Top view */}
          <Carousel autoSlide={true} autoSlideInterval={7000}>
            {slides.map((slide, index) => (
              <div
                key={slide.id}
                className={`lg:px-[12%] py-10 ${slide.bgClass}`}
              >
                <div
                  className={`flex ${index % 2 === 0 ? "md:flex-row gap-5 flex-col" : "md:flex-row-reverse gap-5 flex-col-reverse"} w-full lg:py-20 ${slide.bgClass}`}
                >
                  <div
                    className={`md:w-[50%] flex flex-col md:px-5 justify-center items-center md:items-start md:py-10 ${index % 2 === 0 ? "" : "lg:pl-20"} lg:py-0 gap-4 md:gap-8 `}
                  >
                    <div>
                      <h1 className="text-2xl lg:text-4xl  xl:text-5xl font-bold text-center md:text-start">
                        {slide.title1}
                      </h1>
                      <h1 className="text-2xl lg:text-4xl xl:text-5xl font-bold text-center mt-2 md:text-start">
                        {slide.title2}
                      </h1>
                    </div>
                    <h4 className="text-lg text-center md:text-left px-5 md:px-0 leading-tight line-clamp-2 md:leading-snug max-w-xl">
                      {slide.description}
                    </h4>
                    {/* <Button
                      label={slide.buttonLabel}
                      path={slide.buttonPath}
                      className="bg-gradient-to-r from-[#23aa70] to-[#0e854f] text-gray-50 md:px-10 md:py-4 text-sm md:text-xl hover:bg-gradient-to-r hover:from-[#23aa70] hover:to-[#23aa70] !cursor-pointer"
                    /> */}
                  </div>
                  <div className="sm:w-[50%] w-[70%] block mx-auto">
                    <img
                      src={slide.image}
                      alt="Home Hero"
                      className="block mx-auto"
                      loading="lazy"
                    />
                  </div>
                </div>
              </div>
            ))}
          </Carousel>

          {/* Company About Card */}
          <div className="grid grid-cols-1 lg:grid-cols-5">
            {card.map((item, index) => (
              <div
                key={index}
                className="flex flex-col p-5 lg:p-8 bg-[#17965f] gap-5 border-r-1 items-center justify-center  border-b lg:border-0 border-gray-100 last:border-b-0 pb-3"
              >
                <div className="w-15 xl:w-20">
                  <img src={item.icon} alt="" loading="lazy" />
                </div>
                <div className="text-lg uppercase mt-2 font-semibold text-gray-50">
                  {item.label}
                </div>
              </div>
            ))}
          </div>

          {/* Invite Part */}
          <div className="px-5 lg:px-[12%] grid lg:grid-cols-2 gap-15 py-20">
            <div className="flex justify-center items-center">
              <img
                src={"/assets/svg/home-hero.svg"}
                className="w-[70%] lg:w-full"
                alt="img"
                loading="lazy"
              />
            </div>
            <div className="flex flex-col  justify-center gap-8">
              <h1 className="text-xl md:text-3xl lg:text-4xl font-bold">
                Leading ERP Solution Provider in India
              </h1>
              <p>
                At LogicX, we specialize in ERP implementation, customization,
                and ongoing support for small to medium businesses across India.
                Whether you run a manufacturing unit, textile business, retail
                shop, or service-based company, our tailored ERP solutions help
                streamline operations, reduce manual errors, and improve
                decision-making.
              </p>
              <p>
                Our certified developers and domain experts ensure seamless
                integration with tools like Tally, Woo Commerce, and payment
                gateways. We offer cloud hosting, server setup, data migration,
                and training for your team—so you can focus on growth, not on
                systems.
              </p>
            </div>
          </div>

          {/* portfolio Section */}
          <div className="flex flex-col gap-3 pt-5 bg-website-background text-website-foreground">
            <h1 className="text-2xl text-center md:text-3xl lg:text-4xl font-bold p-5">
              Our ERP Success Stories
            </h1>
            <p className="text-center p-5 lg:px-[12%]">
              From textile manufacturers to retail chains and IT service
              providers, LogicX has delivered tailored ERP solutions that
              transform operations. With 20+ years of experience, we help Indian
              SMEs automate workflows, improve visibility, and scale with
              confidence.
            </p>
            <div className="grid grid-cols-2 md:grid-cols-3 mt-20">
              {portfolio.map((img, idx) => (
                <img
                  key={idx}
                  src={img}
                  onClick={() => {
                    setSliderVisible((sliderVisible) => !sliderVisible);
                    setSelectedIndex(idx);
                  }}
                  alt=""
                  loading="lazy"
                />
              ))}
            </div>
          </div>
          {sliderVisible && (
            <div
              className="bg-black/80 w-full h-full fixed top-0 left-0 z-50 flex items-center justify-center"
              onClick={() => setSliderVisible(false)}
            >
              <div
                className="w-[50%] relative"
                onClick={(e) => e.stopPropagation()}
              >
                <Carousel
                  autoSlide={true}
                  startIndex={selectedIndex}
                  autoSlideInterval={7000}
                >
                  {portfolio.map((img, idx) => (
                    <img
                      key={idx}
                      src={img}
                      onClick={() =>
                        setSliderVisible((sliderVisible) => !sliderVisible)
                      }
                      loading="lazy"
                      alt=""
                    />
                  ))}
                </Carousel>
              </div>
            </div>
          )}
          <div className="pt-10"></div>

          {/* plan details Component */}
          <Plan />

          {/* Consultation Field */}
          <div className="px-5 lg:px-[12%] py-10 flex flex-col sm:flex-row justify-between  bg-[#128d57]">
            <div className="sm:w-3/5 px-5">
              <h1 className="text-2xl text-gray-50 my-5 font-semibold">
                Start your ERP journey with a free consultation today.
              </h1>
            </div>
            <div className="sm:w-1/4 flex items-center justify-center">
              <ScrollLink
                to="contact"
                smooth={true}
                duration={600}
                offset={-70} // Adjust for any sticky headers
                className="bg-gray-50 w-max font-semibold text-[#23ab70] rounded-sm border border-gray-50 hover:bg-[#128d57] hover:text-gray-50 px-4 py-2 text-center text-sm md:text-xl cursor-pointer"
              >
                CONTACT US
              </ScrollLink>
            </div>
          </div>
        </section>

        {/* About Component */}
        <section id="about" className="min-h-[100vh] pb-20">
          <About />
        </section>

        {/* industry Component */}
        <section
          id="industry"
          className="min-h-[100vh] bg-website-background text-website-foreground flex items-center justify-center"
        >
          <CardShowcase items={industries} />

          {/* <Industry /> */}
        </section>

        {/* Why Choose LogicX? */}
        <section className="px-5 py-20 lg:px-[12%] bg-background text-website-foreground">
          <h2 className="text-3xl font-bold text-center pb-8">
            Why Choose LogicX?
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {whyChoose.map((item, idx) => (
              <div
                key={idx}
                className="flex items-start gap-4 p-4 rounded-lg shadow-md bg-gray-50"
              >
                {/* Optional icon placeholder */}
                <div
                  className="w-2 h-8 bg-primary rounded shrink-0"
                  aria-hidden="true"
                />

                <p className="text-lg font-medium text-gray-700">{item.text}</p>
              </div>
            ))}
          </div>
        </section>
        {/* services Component */}
        <section
          id="services"
          className="min-h-[100vh] bg-website-background pb-20"
        >
          <CardShowcase items={projects} />

          <Team
            title="Meet Our Professionals"
            description="Our team combines creativity, expertise, and dedication to deliver outstanding solutions for our clients."
            members={teamData}
          />
          <Review />
          {/* Company Info Section */}
          <div className="px-5 py-10 lg:px-[12%] grid grid-cols-1 lg:grid-cols-4 gap-10 bg-[#128d57]">
            {companyInfo.map((item, index) => (
              <div
                key={index}
                className="flex flex-col justify-center gap-3 items-center border-b lg:border-0 border-gray-100 last:border-b-0 pb-3"
              >
                <img className="w-15" src={item.icon} alt="" loading="lazy" />
                <div className="text-5xl text-gray-50 font-semibold">
                  {item.count}
                </div>
                <div className="text-gray-50 uppercase text-xl">
                  {item.field}
                </div>
              </div>
            ))}
          </div>
          <Articles />
        </section>

        {/* contact Component */}
        <section id="contact" className="min-h-[100vh]">
          <Contact />
        </section>

        <FooterPortfolio
          address={["123 Street", "Coimbatore", "Tamil Nadu, India - 641001"]}
          contact={["info@techmedia.in", "+91 9843213500"]}
          company={[
            { label: "Home", link: "home" },
            { label: "About Us", link: "about" },
            { label: "Industry", link: "industry" },
            { label: "Services", link: "services" },
            { label: "Contact", link: "contact" },
          ]}
          project={[
            { label: "ERPNext", link: "/billing" },
            { label: "Ecart", link: "/billing" },
            { label: "Portfolio", link: "/portfolio" },
          ]}
          legal={[
            { label: "Privacy Policy", link: "/privacy" },
            { label: "Terms & Conditions", link: "/terms" },
          ]}
          brandName="Tech Media"
          year={2025}
        />

        <ScrollToTop />
      </Suspense>
    </main>
  );
};

export default Home;
