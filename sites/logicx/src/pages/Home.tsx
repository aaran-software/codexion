import React, { Suspense, useState } from "react";
import Button from "../../../../resources/components/button/Button";
import Plan from "../../../../resources/components/website/plan";
import Carousel from "../../../../resources/components/carousel";
import { Link as ScrollLink } from "react-scroll";
import ScrollToTop from "../../../../resources/components/common/scrolltotopbutton";
import Team from "../../../../resources/components/website/team";
import Articles from "../../../../resources/components/website/articles";
import Review from "../../../../resources/components/website/review";
import About from "./About";
import Services from "./Services";
import Contact from "./Contact";
import Industry from "./Industry";
import HeaderPortfolio from "../../../../resources/components/header/header-portfolio";
import FooterPortfolio from "../../../../resources/components/footer/footer-portfolio";
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
    { text: "20+ Years in Business Automation & IT" },
    { text: "Cross‑platform Integration Experts" },
    { text: "Open‑source + Proprietary Stack Capabilities" },
    { text: "Local Support with Global Standards" },
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
  return (
    <main>
      <Suspense
        fallback={<LoadingScreen image={"/assets/linkagro_logo.jpg"} />}
      >
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
                  <img src={item.icon} alt="" />
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

          {/* Why Choose LogicX? */}
          <section className="px-5 py-20 lg:px-[12%] bg-website-background text-website-foreground">
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
                    className="w-2 h-8 bg-green-600 rounded"
                    aria-hidden="true"
                  />

                  <p className="text-lg font-medium text-gray-700">
                    {item.text}
                  </p>
                </div>
              ))}
            </div>
          </section>

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
          <Industry />
        </section>

        {/* services Component */}
        <section id="services" className="min-h-[100vh] pb-20">
          <Services />

          <Team />
          <Review />
          {/* Company Info Section */}
          <div className="px-5 py-10 lg:px-[12%] grid grid-cols-1 lg:grid-cols-4 gap-10 bg-[#128d57]">
            {companyInfo.map((item, index) => (
              <div
                key={index}
                className="flex flex-col justify-center gap-3 items-center border-b lg:border-0 border-gray-100 last:border-b-0 pb-3"
              >
                <img className="w-15" src={item.icon} alt="" />
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
