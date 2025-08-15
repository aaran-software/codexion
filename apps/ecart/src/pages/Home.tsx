import { Suspense, lazy, useEffect, useState } from "react";
import LoadingScreen from "../../../../resources/components/loading/LoadingScreen";

const AdverthismentBanner = lazy(
  () => import("../../../../resources/UIBlocks/Promotion/AdverthismentBanner")
);

const ProductCard = lazy(
  () => import("../../../../resources/UIBlocks/ProductCard")
);
const BannerCarousel = lazy(
  () => import("../../../../resources/UIBlocks/BannerCarousel")
);
const GroupProductCard = lazy(
  () => import("../../../../resources/UIBlocks/GroupProductCard")
);
const CustomAdverthismentBanner = lazy(
  () =>
    import("../../../../resources/UIBlocks/Promotion/CustomAdverthismentBanner")
);
const PromotionSection = lazy(
  () => import("../../../../resources/UIBlocks/Promotion/PromotionSection")
);
const ScrollAdverthisment2 = lazy(
  () => import("../../../../resources/UIBlocks/Promotion/ScrollAdverthisment2")
);
const Mainmenu = lazy(() => import("../../../../resources/UIBlocks/Mainmenu"));
const BrandMarquee = lazy(
  () => import("../../../../resources/components/marquee/BrandMarquee")
);
const FloatContact = lazy(
  () => import("../../../../resources/UIBlocks/contact/FloatContact")
);

const CrackerAnimation = lazy(
  () => import("../../../../resources/AnimationComponents/CrackerAnimation")
);
function Home() {
  const brands = [
    { name: "DELL", logo: "/assets/brand/dell.svg" },
    { name: "ACER", logo: "/assets/brand/acer.svg" },
    { name: "HP", logo: "/assets/brand/hp.svg" },
    { name: "LENOVO", logo: "/assets/brand/lenovo.svg" },
    { name: "BENQ", logo: "/assets/brand/benq.svg" },
    { name: "SAMSUNG", logo: "/assets/brand/samsung.svg" },
    { name: "APPLE", logo: "/assets/brand/apple.svg" },
  ];

  const [show, setShow] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const isMobile = window.innerWidth <= 768;
      if (isMobile) {
        setShow(window.scrollY > 100); // mobile: show after 100px scroll
      } else {
        setShow(window.scrollY > 250); // desktop: always show
      }
    };

    window.addEventListener("scroll", handleScroll);
    handleScroll(); // run once on mount
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);
  // const [showMain, setShowMain] = useState(false);

  const [showAnimation, setShowAnimation] = useState(false);

  // Check on mount if animation has been shown before
  useEffect(() => {
    const alreadyShown = localStorage.getItem("Independence Day");
    if (!alreadyShown) {
      setShowAnimation(true); // show animation only first time
    }
  }, []);

  const handleAnimationFinish = () => {
    localStorage.setItem("Independence Day", "true"); // mark as shown
    setShowAnimation(false);
  };

  if (showAnimation) {
    return (
      <CrackerAnimation
        quote="Your Shopping Revolution Starts Now!"
        duration={8000}
        onFinish={handleAnimationFinish}
        explosion1={`/assets/mp3/cracker.mp3`}
        explosion2={`/assets/mp3/cracker.mp3`}
        explosion3={`/assets/mp3/cracker.mp3`}
        flag={`/assets/mp4/flag.mp4`}
        logo={`assets/svg/logo.svg`}
      />
    );
  }

  return (
    <Suspense fallback={<LoadingScreen image={"/assets/svg/logo.svg"} />}>
      <Mainmenu />

      {/* main carousel */}
      <BannerCarousel
        api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_slider", "=", 1]]`}
        delay={6000}
      />

      <div className="px-[5%] mt-10">
        <ProductCard
          title="Popular Items"
          id={"is_popular"}
          filterValue={1}
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_popular", "=", 1]]`}
          ribbon={false}
        />
      </div>

      <div className="px-[5%] mt-10">
        <ProductCard
          title="Laptops"
          id={"item_group"}
          filterValue={"Laptop"}
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["item_group", "=", "Laptop"]]`}
          ribbon={false}
        />
      </div>

      <div className=" py-5 mt-15">
        <CustomAdverthismentBanner
          api={`api/resource/Slider 2`}
          delay={6000}
          sliderBase={"Slider - 1"}
        />
      </div>

      <div className="flex flex-col md:flex-row gap-15 md:gap-5 my-15 px-[5%]">
        <GroupProductCard
          title={"Hot Gadgets Today"}
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_top_rated", "=", 1]]`}
          id={"is_top_rated"}
        />

        <GroupProductCard
          title="Discount for you"
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_discount", "=", 1]]`}
          id={"is_discount"}
        />
      </div>

      <div className="my-10 py-10 md:py-10 bg-primary/5 ">
        <BrandMarquee type="logo" brands={brands} speed={30} height={16} />
      </div>

      <div className="px-[5%] mt-10">
        <ProductCard
          title="Laptops"
          id={"item_group"}
          filterValue={"Laptop"}
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["item_group", "=", "Laptop"]]&limit_page_length=15`}
          ribbon={false}
        />
      </div>

      <div className=" py-5 my-15">
        <CustomAdverthismentBanner
          api={`api/resource/Slider 2`}
          delay={6000}
          sliderBase={"Slider - 3"}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-15 md:gap-5 px-[5%] items-stretch">
        <GroupProductCard
          title="Top Rated"
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_top_rated", "=", 1]]`}
          id="is_top_rated"
        />

        <GroupProductCard
          title="Best Sellers"
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_discount", "=", 1]]`}
          id="is_discount"
        />

        <div className="h-full  bg-background/80 border border-ring/30 shadow rounded-md flex md:hidden lg:flex">
          <PromotionSection
            api={`api/resource/Promotional Special?fields=["name"]&filters=[["set_default", "=", 1]]`}
          />
        </div>
      </div>

      <div className="my-15">
        <ScrollAdverthisment2
          title="Featured Brands"
          api={`api/resource/Promotional Image`}
        />
      </div>

  {/* promotion image slider */}
      {/* <div className=" py-5 my-15">
        <AdverthismentBanner api={`api/resource/Slider 3`} delay={6000} />
      </div> */}
      <div
        className={`transition-opacity duration-500 fixed bottom-28 right-5 z-[100000] ${
          show ? "opacity-100" : "opacity-0 pointer-events-none"
        }`}
      >
        <FloatContact
          contacts={[
            {
              id: "whatsapp",
              contact: "919543439311",
              imgPath: "/assets/svg/whatsapp.svg",
              defaultMessage: "Hello! I'm interested in your product.",
            },
            {
              id: "phone",
              contact: "9894244450",
              imgPath: "/assets/svg/Mobile.svg",
            },
            {
              id: "email",
              contact: "info@techmedia.in",
              imgPath: "/assets/svg/mail.svg",
              defaultMessage: "Hello, I’m interested in your product.",
            },
          ]}
        />
      </div>
    </Suspense>
  );
}

export default Home;
