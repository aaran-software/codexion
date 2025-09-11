import { useState } from "react";
import DocsWrapper from "../DocsWrapper";
import ProcessHighlightSection from "../../../../../resources/UIBlocks/process/ProcessHighlightSection";
import Stepper from "../../../../../resources/UIBlocks/Stepper";
import { useNavigate } from "react-router-dom";
import OrderSummary from "../../../../../resources/UIBlocks/OrderSummary";
import AddressSection from "../../../../../resources/UIBlocks/AddressSection";
import OrderPayment from "../../../../../resources/UIBlocks/OrderPayment";
import OrderSuccess from "../../../../../resources/UIBlocks/OrderSuccess";
import ProcessSection from "../../../../../resources/UIBlocks/process/ProcessSection";
import {
  Code2,
  Layers,
  ShieldCheck,
  Repeat,
  Leaf,
  Users,
  BadgeCheck,
  Clock,
} from "lucide-react";
function ProcessBlock() {
  const navigate = useNavigate();
  const [isPlaceOrder, setIsPlaceOrder] = useState(false);

  const [processSteps] = useState([
    {
      number: 1,
      title: "Our process",
      description:
        "We manufacture and customize coir substrates as per customer requirements with our experienced team and we guide you on the best possible growing solutions.",
    },
    {
      number: 2,
      title: "Region",
      description:
        "We are located in a place with tropical climates where we grow lush green coconut trees. Our raw materials are sourced from local farmers situated here that ensure their livelihood. And abundance of ground water source available here enables us manufacture good quality Low-EC cocopeat.",
    },
    {
      number: 3,
      title: "Logistics & Export",
      description:
        "We have our own exports and logistics team with experienced professionals. Our team directly coordinates with buyers and export agency to ensure uninterrupted transport and shipping of cocopeat across the globe.",
    },
    {
      number: 4,
      title: "Quality",
      description:
        "We have a separate team of people who involve in ensuring quality in each and every step of cocopeat manufacturing process. Right from sourcing coconut husk to producing various cocopeat final products our team follows the quality parameters to deliver top-notch products.",
    },
  ]);

  const steps = [
    {
      title: "Order Summary",
      content: <OrderSummary />,
    },
    {
      title: "Address",
      content: <AddressSection />,
    },
    {
      title: "Payment",
      content: <OrderPayment />,
    },
    {
      title: "Confirmation",
      content: (
        <OrderSuccess
          orderId="ORD12345678"
          paymentId="PAY987654321"
          onContinue={() => navigate("/")}
        />
      ),
    },
  ];
  return (
    <div>
      <DocsWrapper
        title="HeaderPortfolio"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/header/AppFooter",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <ProcessHighlightSection
          title="Why choose us?"
          description="Link Agro Cocopeat - 100% Eco-friendly and Organic soilless growing substrate"
          imageUrl="/assets/img2.jpg"
          bgimage="/assets/cocobg.jpg"
          steps={processSteps}
        />
      </DocsWrapper>

      <DocsWrapper
        title="HeaderPortfolio"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/header/AppFooter",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <Stepper
          steps={steps}
          onClose={() => setIsPlaceOrder(!isPlaceOrder)}
          onFinish={() => navigate("/")}
        />
      </DocsWrapper>
      
      <DocsWrapper
        title="ProcessSection"
        propDocs={[
          {
            name: "items",
            description:
              "Array of content objects. Each item must contain a `title` and `description`. `icon` can be a React component (e.g., Lucide icon) or an image path string.",
          },
          {
            name: "title",
            description:
              "Section heading displayed at the top (e.g., 'What Makes PVR INTERNATIONAL Different?').",
          },
          {
            name: "className",
            description:
              "Optional custom class names applied to the section wrapper for layout and spacing overrides.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/header/AppFooter",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
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
      </DocsWrapper>
    </div>
  );
}

export default ProcessBlock;
