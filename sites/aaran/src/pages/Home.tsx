import { lazy } from "react";
import TransparentCard from "../../../../resources/UIBlocks/card/TransparentCard";
import AnimatedCard from "../../../../resources/UIBlocks/card/animatedCard";
import Pricing from "../../../../resources/UIBlocks/pricingcard/Pricing";
import PortfolioContact from "../../../../resources/UIBlocks/contact/PortfolioContact";
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

  return (
    <div>
      <div className="relative min-h-screen flex flex-col items-center justify-center text-center px-4">
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold text-gray-900 mb-4">
          Streamline Your
          <span className="emoji">💼</span> Business,
          <br />
          Unlock
          <span className="emoji">🔓</span> Your Growth!
        </h1>

        <p className="text-gray-600 text-base md:text-lg max-w-xl mb-8">
          Manage your budget, track expenses, invest wisely, and achieve your
          financial goals— all in one intuitive app with savings goals and
          investment tracking.
        </p>

        <button className="bg-gradient-to-r from-primary to-primary/40 text-white px-8 py-3 rounded-full shadow-[0_8px_15px_rgba(0,0,0,0.2)] hover:scale-105 transition-transform duration-300 cursor-pointer">
          Get Started
        </button>

        {/* Optional Background Blocks */}
        <div className="absolute bottom-0 left-1/4 w-24 h-24 bg-white/30 rounded-lg blur-2xl"></div>
        <div className="absolute bottom-0 right-1/4 w-32 h-32 bg-white/20 rounded-lg blur-3xl"></div>
      </div>

      <TransparentCard image="assets/dashboard.png" />

      <div className="mt-24"></div>
      <AnimatedCard
        cards={cardData}
        title={"Our Products"}
        description={
          "Explore our wide range of products crafted with quality and precision. Designed to meet your needs and deliver the best experience."
        }
      />
      <div className="mt-20">
        <Pricing plans={plans} />
      </div>

      <div className="my-10 py-10 md:py-10 ">
        <BrandMarquee type="big-text" brands={brands} speed={30} height={16} />
      </div>

      <PortfolioContact
        contact={{
          address: "Mahavishnu Nagar, Tiruppur, Tamil Nadu",
          phone: ["+91 98765 43210", "+91 91234 56789"], // multiple numbers
          email: ["hello@example.com", "support@example.com"], // multiple emails
        }}
      />
    </div>
  );
}

export default Home;
