import React from "react";
import TransparentCard from "../../../../resources/UIBlocks/card/TransparentCard";
import TypingText from "../../../../resources/AnimationComponents/TypingText";
import BrandMarquee from "../../../../resources/components/marquee/BrandMarquee";
import HighlightSection1 from "../../../../resources/UIBlocks/HighlightSection/HighlightSection1";
import AboutSection from "../../../../resources/UIBlocks/about/AboutSection";
import MapSection from "../../../../resources/UIBlocks/map/MapSection";
import { useNavigate } from "react-router-dom";
import HighlightCardWithIcon from "../../../../resources/UIBlocks/card/HighlightedCardwithIcon";
import { FaEye, FaBullseye, FaHandshake } from "react-icons/fa";
import { useInView } from "react-intersection-observer";
function about() {
  const navigate = useNavigate();
  const [ref4, inView4] = useInView({ triggerOnce: true, threshold: 0.1 });

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
      text: `Be chosen by customers and employees as a
trusted partner in India to manufacture high
quality garments, delivered on time, in a
mutually trusted and respected environment.`,
      icon: <FaEye />,
    },
    {
      title: "Our Mission",
      text: `Exceed our customers requirements based on
continous improvement, safety actions and using
lean and sustainable strategies.`,
      icon: <FaBullseye />,
    },
  ];
  return (
    <div className="mt-20 lg:mt-30">
      <div className="pt-10 bg-gradient-to-b from-primary via-primary/20 to-transparent mb-10">
        <TypingText
          fixedMessage="About"
          messages={["PVR International", "DEENU International"]}
          typingSpeed={100}
          pauseTime={1500}
          className="text-4xl md:text-5xl font-bold text-primary-foreground"
          TypingTextClassName="text-highlight1"
        />
        <p className="text-center mt-5 w-[80%] block mx-auto text-primary-foreground">
          Our journey started in 1995, when PVR International was founded and
          later in 2002, DEENU International was started as our sister concern.
          We have today grown into a vertically integrated manufacturer of all
          Printing, Embroidery and Stitching Units enables us to provide high
          quality garments within a short lead time.
        </p>

        <div className="mt-20 px-[10%] ">
          <TransparentCard image="assets/banner/banner1.jpg" />
        </div>
      </div>

      <div className="px-5 mt-30 lg:px-[10%]">
        <HighlightCardWithIcon
          className="grid-cols-1 md:grid-cols-2"
          sectionTitle=""
          items={VisionMission}
        />
      </div>

      <div
        className={`bg-primary p-6 mt-20 rounded-lg shadow-md mx-4 lg:mx-[10%] ${
          inView4 ? "animate__animated animate__fadeInUp" : "opacity-0"
        }`}
        ref={ref4}
      >
        <h3 className="text-2xl font-semibold text-primary-foreground mb-4">
          Our Philosophy
        </h3>
        <p className="text-base text-primary-foreground leading-relaxed text-justify">
          Our business model is based on agile, flexible, lean and sustainable
          practices that minimize environmental impact, ensure the health and
          well-being of our employees and create valuable opportunities that
          foster the economic and social development of our company and the
          community.
        </p>
      </div>

      <div className="px-4 md:px-[10%]">
        {/* Mission Component */}
        <HighlightSection1
          subtitle="OUR PEOPLE"
          title="TO END"
          title2="CYBER RISK"
          description={`Our company's greatest asset lies in the individuals
          who drive our diverse processes, serving as the
          cornerstone of our success. The unwavering
          commitment and dedication of our employees
          enable us to actively foster opportunities that
          enhance their quality of life.
          We prioritize the provision of ongoing training
          opportunities to our employees, empowering them
          to acquire fresh skills and pursue personal growth.
          As a responsible employer, we diligently extend all
          essential benefits to our employees, aiming to
          enhance their overall well-being.
          `}
          statValue={9}
          statUnit="TRILLION"
          statDescription="We analyze 9+ trillion security events on our platform per week. Click to learn more about how our platform works."
        />
        {/* Vision Component */}
        {/* <HighlightSection1
          subtitle="OUR VISION"
          title="TO END"
          title2="CYBER RISK"
          description="We envision a future without cyber risk. With our comprehensive suite of security operations solutions We envision a future without cyber risk. With our comprehensive suite of security operations solutions We envision a future without cyber risk. With our comprehensive suite of security operations solutions We envision a future without cyber risk. With our comprehensive suite of security operations solutions..."
          statValue={9}
          statUnit="TRILLION"
          statDescription="We analyze 9+ trillion security events on our platform per week. Click to learn more about how our platform works."
          reverse
        /> */}
      </div>
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
        />
      </div>

      <div className="my-10 md:my-20 py-10 md:py-10">
        <BrandMarquee
          type="big-text"
          text="Awards & Badges"
          brands={brands}
          speed={30}
          height={16}
        />
      </div>

      <div className="px-4">
        <MapSection
          title="Our Global Presence"
          description="Our factory was established in the year 1995 in the key manufacturing state of Tamil Nadu,
          India. Our factories are located in the city of Tirupur, where the political and social
          environment is always stable and the availability of skilled labor and high-quality raw
          materials are in abundance.
          We have over 25 years of experience with over 450 skilled employees helping us in the
          manufacture and export of Knitted Menswear, Womenswear and Kidswear.
          Our products are present in more than 7 countries (Canada, Netherlands, France,
          Switzerland, Germany, Belgium & India) and we are looking to expand our reach."
          startLocationName="India"
          lineColor="orange"
          markerColor="blue"
          startMarkerColor="red"
          textColor="black"
          locations={[
            { name: "India", coordinates: [-100.106713, -54.113318] }, //{x,y}
            { name: "Canada", coordinates: [15.0, 40.0] },
            { name: "Netherlands", coordinates: [7.2529, 42.2048] },
            { name: "France", coordinates: [65.0, 35.0] },
            { name: "Switzerland", coordinates: [63.0, 42.0] },
            { name: "Germany", coordinates: [70.0, 40.0] },
            { name: "Belgium ", coordinates: [68.0, 38.0] },
          ]}
          mapImage="/assets/map.png"
          mapAlign="right"
        />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-[40%_60%] md:grid-cols-[30%_70%] mt-20 overflow-hidden sm:h-[100vh] bg-primary text-primary-foreground">
        <div>
          <img
            src="/assets/owner.jpeg"
            alt=""
            className="w-full object-cover"
          />
        </div>

        {/* Right section */}
        <div className="flex flex-col justify-center h-full p-10 text-xs sm:text-sm">
          <h1 className="mb-7 font-bold text-lg">Dear Business Associates,</h1>

          <p>
            We thank you for taking your time to view our company profile. As a
            knitted garment manufacturing company, we always look for a long
            term relationship with our customers.
          </p>
          <p className="my-7">
            We guarantee to provide quality products to our customers, whilst
            ensuring safe and well established working standards for all our
            employees. We would be very grateful if you could provide us with an
            opportunity to showcase the products manufactured at our factory.
          </p>
          <p className="mb-7">
            We look forward to working with your esteemed company in the near
            future.
          </p>

          <div className="flex flex-col gap-2">
            <p className="font-bold text-lg">P Velusamy</p>
            <p className="font-bold text-lg">Managing Director</p>
            <a href="mailto:velu@pvrinternational.com">
              velu@pvrinternational.com
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default about;
