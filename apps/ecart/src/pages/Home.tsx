import { Suspense, lazy } from "react";
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

  return (
    <Suspense fallback={<LoadingScreen image={"/assets/svg/logo.svg"} />}>
      <Mainmenu />

      <BannerCarousel
        api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_slider", "=", 1]]`}
        delay={6000}
      />

      <div className="px-[5%] mt-15">
        <ProductCard
          title="Popular Items"
          id={"is_popular"}
          filterValue={1}
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_popular", "=", 1]]`}
          ribbon={false}
        />
      </div>

      <div className="px-[5%] mt-15">
        <ProductCard
          title="Laptops"
          id={"category"}
          filterValue={"Laptop"}
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_popular", "=", 1]]`}
          ribbon={false}
        />
      </div>
      <div className=" py-5 mt-20">
        <AdverthismentBanner
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_slider", "=", 1]]`}
          delay={6000}
        />
      </div>

      <div className="flex flex-col md:flex-row gap-15 md:gap-5 mt-15 px-[5%]">
        <GroupProductCard
          title={"Hot Gadgets Today"}
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["top_rated", "=", 1]]`}
          id={"top_rated"}
        />

        <GroupProductCard
          title="Discount for you"
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_discount", "=", 1]]`}
          id={"is_discount"}
        />
      </div>

      <div className=" py-5 mt-20">
        <CustomAdverthismentBanner
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_slider", "=", 1]]`}
          delay={6000}
        />
      </div>

      <div className="px-[5%] mt-5">
        <ProductCard
          title="Laptops"
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["category", "=", "Laptop"]]&limit_page_length=0`}
          filterValue={1}
          id={"Laptop"}
        />
      </div>

      <div className="my-10 py-10 md:py-15 bg-primary/5 ">
        <BrandMarquee type="logo" brands={brands} speed={90} height={20} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-15 md:gap-5 px-[5%] items-stretch">
        <GroupProductCard
          title="Top Rated"
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["top_rated", "=", 1]]`}
          id="top_rated"
        />

        <GroupProductCard
          title="Best Sellers"
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_discount", "=", 1]]`}
          id="is_discount"
        />

        <div className="h-full  bg-background/80 border border-ring/30 shadow rounded-md flex md:hidden lg:flex">
          <PromotionSection image={"/assets/Promotion/ads3.png"} />
        </div>
      </div>

      <div className="my-15">
        <ScrollAdverthisment2
          title="Featured Brands"
          api={`api/resource/Catalog Details?fields=["name"]&filters=[["is_popular", "=", 1]]`}
        />
      </div>

      <FloatContact
        contacts={[
          {
            id: "whatsapp",
            contact: "919543439311", // no '+' symbol, just country code + number
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
            contact: "info@techmedia.in", // just the username, no @
            imgPath: "/assets/svg/mail.svg",
            defaultMessage: "Hello, I’m interested in your product.",
          },
        ]}
        className="fixed bottom-28 right-5 z-[100000]"
      />
    </Suspense>
  );
}

export default Home;
