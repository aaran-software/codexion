import HeroBanner from "../../../../../resources/UIBlocks/banner/HeroBanner";
import HeroBanner2 from "../../../../../resources/UIBlocks/banner/HeroBanner2";
import HighlightedBanner from "../../../../../resources/UIBlocks/banner/HighlightedBanner";
import VerticalHoverBlocks from "../../../../../resources/UIBlocks/banner/VerticalHoverBlocks";
import SimpleBanner from "../../../../../resources/UIBlocks/banner/SimpleBanner";
import DocsWrapper from "../DocsWrapper";
const BannerBlock = () => {
  const highlightSections = [
    {
      image: "/assets/bg.jpg",
      title: "Seamless Experience",
      description: "Enjoy a responsive design across all devices.",
      buttonLabel: "Learn More",
    },
    {
      image: "/assets/bg2.jpg",
      title: "Scalable Solutions",
      description: "From startups to enterprises, we grow with you.",
      buttonLabel: "Get Started",
    },
    {
      image: "/assets/bg.jpg",
      title: "Global Reach",
      description: "Expand your business worldwide with ease.",
      buttonLabel: "Explore",
    },
  ];

  const verticalSections = [
    {
      label: "Innovation",
      title: "Driving the Future",
      description: "We create cutting-edge solutions to push boundaries.",
      image: "/assets/bg.jpg",
      date: "Aug 2025",
      ctaText: "Discover",
    },
    {
      label: "Sustainability",
      title: "Green & Clean",
      description: "Our tech reduces carbon footprint for businesses.",
      image: "/assets/bg2.jpg",
      date: "Jul 2025",
      ctaText: "Learn More",
    },
    {
      label: "Community",
      title: "Building Together",
      description: "Collaboration is at the heart of what we do.",
      image: "/assets/bg.jpg",
      date: "Jun 2025",
      ctaText: "Join Us",
    },
  ];

  return (
    <div className="space-y-16">
      {/* ---------------- HeroBanner Section ---------------- */}

      <DocsWrapper
        title="HeroBanner"
        propDocs={[
          { name: "badgeText", description: "Small badge label" },
          { name: "title", description: "Main heading text" },
          { name: "subtitle", description: "Supporting description" },
          { name: "buttonText", description: "CTA button label" },
          { name: "buttonLink", description: "Path or external link" },
        ]}
        paths={{
          file: "/resources/UIBlocks/banner/HeroBanner",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["About", "Services", "Landing", "Contact"],
        }}
      >
        <HeroBanner
          badgeText="🚀 Featured"
          title="Next-Gen Digital Solutions"
          subtitle="Delivering performance and scalability for every business size."
          buttonText="Start Now"
          buttonLink="#"
        />
      </DocsWrapper>

      {/* ---------------- HeroBanner Section ---------------- */}

      <DocsWrapper
        title="HighlightedBanner Props"
        propDocs={[
          { name: "sections", description: "Array of section objects" },
          { name: "image", description: " Banner image path" },
          { name: "title", description: " Section title" },
          { name: "description", description: "Section description" },
          { name: "buttonLabel?", description: "Optional CTA label" },
        ]}
        paths={{
          file: "/resources/UIBlocks/banner/HighlightedBanner",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["About", "Services", "Landing", "Contact"],
        }}
      >
        <HighlightedBanner sections={highlightSections} />
      </DocsWrapper>

      <DocsWrapper
        title="VerticalHoverBlocks Props"
        propDocs={[
          { name: "sections", description: "Array of section objects" },
          { name: "label", description: "Sidebar label text" },
          { name: "image", description: "Preview/illustration image" },
          { name: "title", description: " Main title of section" },
          { name: "description", description: "Supporting description text" },
          { name: "date?", description: " Optional date shown" },
          { name: "ctaText?", description: "Optional CTA button label" },
        ]}
        paths={{
          file: "/resources/UIBlocks/banner/VerticalHoverBlocks",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["About", "Services", "Landing", "Contact"],
        }}
      >
        <VerticalHoverBlocks sections={verticalSections} />
      </DocsWrapper>

      <DocsWrapper
        title="SimpleBanner Props"
        propDocs={[
          { name: "title", description: "Main title text of the banner" },
          { name: "buttonLabel", description: "Label text for the button" },
          { name: "imgPath", description: "Path or URL for the banner image" },
          {
            name: "routePath?",
            description: "Optional route path for navigation",
          },
          { name: "className?", description: "Optional custom CSS classes" },
          {
            name: "path?",
            description: "Optional link path if different from routePath",
          },
          {
            name: "buttonStyle?",
            description: "Optional custom styles for the button",
          },
          {
            name: "textStyle?",
            description: "Optional custom styles for the text",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/banner/SimpleBanner",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["About", "Services", "Landing", "Contact"],
        }}
      >
        <SimpleBanner
          title={"Turning Complexity into Simplicity"}
          imgPath={"/assets/h1.png"}
          path={"contact"}
          buttonLabel={"Start Now"}
          className="bg-purple-800"
          buttonStyle="bg-foreground text-background "
          textStyle="text-background"
        />
      </DocsWrapper>

      <DocsWrapper
        title="HomeBanner Props"
        propDocs={[
          { name: "images", description: "Array of banner images (id, image)" },
          {
            name: "interval?",
            description:
              "Time interval (ms) for auto image change, default 5000",
          },
          {
            name: "title",
            description: "Fixed title text displayed on the banner",
          },
          {
            name: "description",
            description: "Fixed description text displayed under the title",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/banner/HomeBanner",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Landing", "About", "Services", "Contact"],
        }}
      >
        <HeroBanner2
          images={[
            { id: "1", image: "/assets/bg.jpg" },
            { id: "2", image: "/assets/bg2.jpg" },
            { id: "3", image: "/assets/bg.jpg" },
          ]}
          interval={5000}
          title="Welcome to Codexion"
          description="We build smart solutions that accelerate your business growth."
          videoPath={"/assets/banner/bannervideo.mp4"}
        />
      </DocsWrapper>
    </div>
  );
};

export default BannerBlock;
