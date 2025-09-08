// components/blocks/AnimatedCardBlock.tsx
import { Rocket, ShieldCheck, Users } from "lucide-react";
import AnimatedCard from "../../../../../resources/UIBlocks/card/AnimatedCard";
import CardView from "../../../../../resources/UIBlocks/card/CardView";
import ContactCard from "../../../../../resources/UIBlocks/card/ContactCard";
import FlexColCard from "../../../../../resources/UIBlocks/card/FlexColCard";
import HighlighCard from "../../../../../resources/UIBlocks/card/HighlighCard";
import HighlightCardWithIcon from "../../../../../resources/UIBlocks/card/HighlightedCardwithIcon";
import ScrollableCard from "../../../../../resources/UIBlocks/card/ScrollableCard";
import TransparentCard from "../../../../../resources/UIBlocks/card/TransparentCard";
import NexusCard from "../../../../../resources/UIBlocks/card/NexusCard";

import DocsWrapper from "../DocsWrapper";
import GroupProductCard from "../../../../../resources/UIBlocks/GroupProductCard";
import ProductCard from "../../../../../resources/UIBlocks/ProductCard";
import ProductCard2 from "../../../../../resources/UIBlocks/ProductCard2";
const CardBlock = () => {
  const cards = [
    {
      title: "Fast Delivery",
      description: "Get your products delivered within 24 hours.",
      image: "/assets/bg.jpg",
      hoverColor: "from-indigo-500 to-purple-500",
    },
    {
      title: "Secure Payments",
      description: "Your transactions are encrypted and secure.",
      image: "/assets/bg.jpg",
      hoverColor: "from-green-500 to-teal-500",
    },
    {
      title: "24/7 Support",
      description: "Our team is here to help anytime you need.",
      image: "/assets/bg.jpg",
      hoverColor: "from-pink-500 to-red-500",
    },
  ];

  const items = [
    {
      id: 1,
      title: "Web Development",
      description:
        "We build scalable, high-performance websites tailored for your business needs.",
      features: [
        "Responsive design",
        "SEO optimized",
        "Fast loading speed",
        "CMS integration",
      ],
    },
    {
      id: 2,
      title: "Mobile App Development",
      description:
        "Custom mobile applications that deliver seamless user experiences.",
      features: [
        "iOS & Android support",
        "Cross-platform compatibility",
        "User-friendly interface",
        "App Store deployment",
      ],
    },
  ];

  const contactData = {
    address: "123 Main Street, New York, USA",
    phone: ["+1 234 567 890", "+1 987 654 321"],
    email: ["info@example.com", "support@example.com"],
  };

  const demoItems = [
    {
      id: "tab1",
      label: "Strategy",
      title: "Business Strategy",
      description:
        "We craft growth-focused strategies that align with your company’s vision and market opportunities.",
      navLink: "/services/strategy",
      image: "/assets/bg.jpg",
      subImages: ["/assets/bg.jpg", "/assets/bg.jpg"],
    },
    {
      id: "tab2",
      label: "Design",
      title: "Creative Design",
      description:
        "Our design team delivers stunning visuals and smooth user experiences across all platforms.",
      navLink: "/services/design",
      image: "/assets/bg.jpg",
      subImages: ["/assets/bg.jpg", "/assets/bg.jpg"],
    },
    {
      id: "tab3",
      label: "Development",
      title: "Modern Development",
      description:
        "We build scalable web and mobile apps using the latest frameworks, ensuring long-term performance.",
      navLink: "/services/development",
      image: "/assets/bg.jpg",
      subImages: ["/assets/bg.jpg", "/assets/bg.jpg"],
    },
  ];

  const demoItems2 = [
    {
      title: "Fast Delivery",
      text: "We ensure on-time delivery with agile project management.",
    },
    {
      title: "Scalable Solutions",
      text: "Our apps are built to scale seamlessly with your growth.",
    },
    {
      title: "24/7 Support",
      text: "Dedicated team available for continuous support & monitoring.",
    },
    {
      title: "Proven Expertise",
      text: "Over 20+ years of experience across industries.",
    },
  ];

  const demoItems3 = [
    {
      title: "Fast Deployment",
      text: "Quick setup with CI/CD pipelines and automation.",
      icon: <Rocket />,
    },
    {
      title: "Enterprise Security",
      text: "Top-grade security protocols and compliance standards.",
      icon: <ShieldCheck />,
    },
    {
      title: "Customer First",
      text: "Our team is dedicated to providing client-focused solutions.",
      icon: <Users />,
    },
  ];

  return (
    <div className="flex flex-col gap-10">
      <DocsWrapper
        title="1. AnimatedCard"
        propDocs={[
          { name: "title", description: "Main heading for the section" },
          { name: "description", description: "Subheading below the title" },
          {
            name: "cards",
            description:
              "Array of card objects with `title`, `description`, `image`, and `hoverColor`",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/card/AnimatedCard",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <AnimatedCard
          title="Why Choose Us"
          description="We provide high quality services for your business"
          cards={cards}
        />
      </DocsWrapper>

      <DocsWrapper
        title="2. ServicesCard"
        propDocs={[
          {
            name: "items",
            description:
              "An array of objects, each containing `id`, `title`, `description`, and `features` (list of strings).",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/card/CardView",
          usedIn: ["/pages/Services.tsx"],
          reusableIn: ["Service Sections", "Feature Lists", "Pricing Pages"],
        }}
      >
        <CardView items={items} />
      </DocsWrapper>

      <DocsWrapper
        title="3. ContactCard"
        propDocs={[
          {
            name: "contact.address",
            description:
              "Optional string. Displays the office or company address.",
          },
          {
            name: "contact.phone",
            description:
              "Optional array of strings. Each phone number becomes a clickable `tel:` link.",
          },
          {
            name: "contact.email",
            description:
              "Optional array of strings. Each email address becomes a clickable `mailto:` link.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/card/ContactCard",
          usedIn: ["/pages/Contact.tsx"],
          reusableIn: [
            "Portfolio Contact Section",
            "Company Info Footer",
            "Landing Page CTA",
          ],
        }}
      >
        <ContactCard contact={contactData} />
      </DocsWrapper>

      <DocsWrapper
        title="4. FlexColCard"
        propDocs={[
          {
            name: "heading",
            description: "Optional string. Heading above the tab navigation.",
          },
          {
            name: "items",
            description:
              "Array of objects defining each tab’s content (id, label, title, description, navLink, image, subImages[]).",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/card/FlexColCard",
          usedIn: ["/pages/Services.tsx"],
          reusableIn: [
            "Services / Features Section",
            "Case Studies Showcase",
            "Portfolio Detail Page",
          ],
        }}
      >
        <FlexColCard heading="Our Expertise" items={demoItems} />
      </DocsWrapper>

      <DocsWrapper
        title="5. HighlighCard"
        propDocs={[
          {
            name: "sectionTitle",
            description: "String. Heading text for the whole section.",
          },
          {
            name: "items",
            description:
              "Array of { title?: string, text: string } objects to display.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/card/HighlighCard",
          usedIn: ["/pages/About.tsx"],
          reusableIn: [
            "Why Choose Us Section",
            "Key Benefits Section",
            "Feature Highlights Section",
          ],
        }}
      >
        <HighlighCard sectionTitle="Why Choose Us?" items={demoItems2} />
      </DocsWrapper>

      <DocsWrapper
        title="6. HighlightCardWithIcon"
        propDocs={[
          {
            name: "sectionTitle",
            description: "String. Heading text for the section.",
          },
          {
            name: "items",
            description:
              "Array of { title?: string, text: string, icon?: ReactNode, iconImage?: string }.",
          },
          {
            name: "className",
            description:
              "Custom grid class (e.g., 'grid-cols-1 md:grid-cols-3').",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/card/HighlightCardWithIcon",
          usedIn: ["/pages/Services.tsx"],
          reusableIn: [
            "Features Section",
            "Why Choose Us Section",
            "Service Highlights Section",
          ],
        }}
      >
        <HighlightCardWithIcon
          sectionTitle="Our Key Features"
          items={demoItems3}
          className="grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
        />
      </DocsWrapper>

      <DocsWrapper
        title="7. ScrollableCard"
        propDocs={[
          {
            name: "products",
            description:
              "Array of { id, name, price, image, inventoryStatus }.",
          },
          {
            name: "numVisible",
            description:
              "Number of cards visible at once. Auto-adjusts by screen size.",
          },
          {
            name: "currentIndex",
            description: "The index of the current first visible product.",
          },
          {
            name: "ImageButton",
            description: "Navigation button component for prev/next control.",
          },
        ]}
        paths={{
          file: "resources/UIBlocks/card/ScrollableCard",
          usedIn: ["/pages/Shop.tsx"],
          reusableIn: [
            "Product Carousels",
            "Featured Items",
            "Related Products",
            "Shop Landing Page",
          ],
        }}
      >
        <ScrollableCard />
      </DocsWrapper>

      <DocsWrapper
        title="8. TransparentCard"
        propDocs={[
          {
            name: "image",
            description: "The image URL displayed inside the transparent card.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/card/HighlightCardWithIcon",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div className="space-y-20">
          <TransparentCard image="https://picsum.photos/id/1015/800/450" />
          <TransparentCard image="https://picsum.photos/id/1016/800/450" />
          <TransparentCard image="https://picsum.photos/id/1018/800/450" />
        </div>
      </DocsWrapper>

      <DocsWrapper
        title="9. NexusCard"
        propDocs={[
          {
            name: "image",
            description: "The image URL displayed inside the transparent card.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/card/NexusCard",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div className="space-y-20">
          <NexusCard
            sectionTitle="Integrations"
            sectionDescription="Streamline your marketing activities by integrating collected data with the choice of your CRM and campaign integration options."
            leftClassName="text-left"
            rightClassName="grid-rows-3"
            items={[
              {
                logo: "/assets/hp.svg",
                alt: "Stripe",
                title: "Stripe",
                className: "bg-[#3E2F89]",
              },
              {
                logo: "/assets/hp.svg",
                alt: "PayPal",
                title: "PayPal",
                className: "bg-[#c71313]",
              },
              {
                logo: "/assets/hp.svg",
                alt: "Razorpay",
                title: "Razorpay",
                className: "bg-[#67c090] row-span-2",
              },
              {
                logo: "/assets/hp.svg",
                alt: "QuickBooks",
                title: "QuickBooks",
                className: "bg-[#ea2264]",
              },
              {
                logo: "/assets/hp.svg",
                alt: "Xero",
                title: "Xero",
                className: "bg-[#f5babb] row-span-2",
              },
              {
                logo: "/assets/hp.svg",
                alt: "Tally",
                title: "Tally",
                className: "bg-[#b2b0e8]",
              },
            ]}
          />
        </div>
      </DocsWrapper>

      <DocsWrapper
        title="10. GroupProductCard"
        propDocs={[
          {
            name: "image",
            description: "The image URL displayed inside the transparent card.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/card/NexusCard",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div className="space-y-20">
          <GroupProductCard
            title="Discount for you"
            api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_discount", "=", 1]]`}
            id={"is_discount"}
          />
        </div>
      </DocsWrapper>

      <DocsWrapper
        title="11. ProductCard"
        propDocs={[
          {
            name: "image",
            description: "The image URL displayed inside the transparent card.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/card/NexusCard",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div className="space-y-20">
          <ProductCard
            title="Popular Items"
            id={"is_popular"}
            filterValue={1}
            api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_popular", "=", 1]]&limit_page_length=15`}
            ribbon={false}
          />
        </div>
      </DocsWrapper>

       <DocsWrapper
        title="12. ProductCard2"
        propDocs={[
          {
            name: "image",
            description: "The image URL displayed inside the transparent card.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/card/NexusCard",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div className="space-y-20">
          <ProductCard2
            title="Popular Items"
            api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_popular", "=", 1]]&limit_page_length=15`}
            ribbon={false}
          />
        </div>
      </DocsWrapper>
    </div>
  );
};

export default CardBlock;
