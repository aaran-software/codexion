import React from "react";
import DocsWrapper from "../DocsWrapper";
import BlogCarouselCard from "../../../../../resources/UIBlocks/carousel/BlogCarouselCard";
import { LinkAgroBlogs } from "../../../../../resources/global/helpers/blog";
import { Slide } from "../../../../../resources/UIBlocks/carousel/HeroCarousel";
import HeroCarousel from "../../../../../resources/UIBlocks/carousel/HeroCarousel";
import ProjectCarousel from "../../../../../resources/UIBlocks/carousel/ProjectCarousel";
import BannerCarousel from "../../../../../resources/UIBlocks/BannerCarousel";
import ImageCarousel from "../../../../../resources/UIBlocks/carousel/ImageCarousel";

function CarouselBlock() {
  const blogs = [...LinkAgroBlogs];

  const slidesData: Slide[] = [
    {
      id: 1,
      title1: "Sustainable Coco Peat.",
      title2: "Trusted Worldwide.",
      description:
        "Link Agro Exports manufactures and exports premium coco peat products, trusted by growers and horticulturists across the globe.",
      image: "/assets/h1.png",
      bgClass: "",
      backdrop: "",
      backdropposition:
        "-top-65 md:-top-55 md:-right-20 lg:-top-20 lg:-right-120",
    },
    {
      id: 2,
      title1: "Made in Tamil Nadu.",
      title2: "Quality from Source.",
      description:
        "Our plant in Uchipuli, Tamil Nadu, is surrounded by abundant coconut farms and excellent groundwater, ensuring high-quality raw material.",
      image: "/assets/h1.png",
      bgClass: "",
      backdrop: "",
      backdropposition:
        "-top-75 -left-5 md:-left-70 md:-top-40 lg:-left-170 lg:top-0",
    },
    {
      id: 3,
      title1: "Eco-Friendly Process.",
      title2: "Natural & Reliable.",
      description:
        "We produce coir and coco peat products using sustainable methods that preserve natural resources and support green farming.",
      image: "/assets/h1.png",
      bgClass: "",
      backdrop: "",
      backdropposition: "-top-80 right-0 md:-top-80 lg:-top-20",
    },
    {
      id: 4,
      title1: "Perfect for Cultivation.",
      title2: "Proven Growth Medium.",
      description:
        "Our coco peat ensures optimal water retention, aeration, and root development—ideal for nurseries, greenhouses, and hydroponics.",
      image: "/assets/h1.png",
      bgClass: "",
      backdrop: "",
      backdropposition:
        "-top-70 -left-30 md:-top-60 md:-left-80 lg:-left-150 lg:-top-30",
    },
  ];

  const product = [
    {
      id: 1,
      title: "Linkagro Exports Portfolio",
      description: "A modern personal portfolio site.",
      category: "website",
      image: "/assets/product/linkagro.jpg",
      link: "https://linkagro.in/",
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
      link: "https://grand-florentine-b254ee.netlify.app/",
    },
    {
      id: 5,
      title: "ERPNext",
      description: "Corporate business website.",
      category: "app",
      image: "/assets/product/linkagro.png",
      link: "https://example.com/company",
    },
  ];
  return (
    <div className="w-[100wh]">
      <DocsWrapper
        title="AnimatedCard"
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
          file: "/resources/UIBlocks/carousel/BlogCarouselCard",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <BlogCarouselCard blogs={blogs} title={"Latest Posts & Articles"} />
      </DocsWrapper>

      <DocsWrapper
        title="AnimatedCard"
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
          file: "/resources/UIBlocks/carousel/BlogCarouselCard",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <HeroCarousel
          slides={slidesData}
          autoSlide={true}
          autoSlideInterval={7000}
        />
      </DocsWrapper>

      <DocsWrapper
        title="AnimatedCard"
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
          file: "/resources/UIBlocks/carousel/BlogCarouselCard",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <ProjectCarousel
          products={product}
          autoSlide={true}
          autoSlideInterval={4000}
        />
      </DocsWrapper>

      <DocsWrapper
        title="AnimatedCard"
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
          file: "/resources/UIBlocks/carousel/BlogCarouselCard",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <BannerCarousel
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_slider", "=", 1]]`}
          delay={6000}
        />
      </DocsWrapper>

      <DocsWrapper
        title="ImageCarousel"
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
          file: "/resources/UIBlocks/carousel/BlogCarouselCard",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <ImageCarousel
          images={[
            { id: "1", image: "/assets/bg.jpg" },
            { id: "2", image: "/assets/bg.jpg" },
            { id: "3", image: "/assets/bg.jpg" },
          ]}
          interval={6000}
        />
      </DocsWrapper>

      {/*<DocsWrapper*/}
      {/*    title="ImageCarousel"*/}
      {/*    propDocs={[*/}
      {/*        {name: "title", description: "Main heading for the section"},*/}
      {/*        {name: "description", description: "Subheading below the title"},*/}
      {/*        {*/}
      {/*            name: "cards",*/}
      {/*            description:*/}
      {/*                "Array of card objects with `title`, `description`, `image`, and `hoverColor`",*/}
      {/*        },*/}
      {/*    ]}*/}
      {/*    paths={{*/}
      {/*        file: "/resources/UIBlocks/carousel/BlogCarouselCard",*/}
      {/*        usedIn: ["/pages/Home.tsx"],*/}
      {/*        reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],*/}
      {/*    }}*/}
      {/*>*/}
      {/*    <ImageCarousel*/}
      {/*        images={[*/}
      {/*            {id: "1", image: "/assets/bg.jpg"},*/}
      {/*            {id: "2", image: "/assets/bg.jpg"},*/}
      {/*            {id: "3", image: "/assets/bg.jpg"},*/}
      {/*        ]}*/}
      {/*        interval={6000}*/}
      {/*    />*/}
      {/*</DocsWrapper>*/}
    </div>
  );
}

export default CarouselBlock;
