import { useState } from "react";
import DocsWrapper from "../DocsWrapper";
import ProcessHighlightSection from "../../../../../resources/UIBlocks/process/ProcessHighlightSection";
import Stepper from "../../../../../resources/UIBlocks/Stepper";
import { useNavigate } from "react-router-dom";
import OrderSummary from "../../../../../resources/UIBlocks/OrderSummary";
import AddressSection from "../../../../../resources/UIBlocks/AddressSection";
import OrderPayment from "../../../../../resources/UIBlocks/OrderPayment";
import OrderSuccess from "../../../../../resources/UIBlocks/OrderSuccess";

function ProcessBlock() {
  const navigate=useNavigate()
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
    </div>
  );
}

export default ProcessBlock;
