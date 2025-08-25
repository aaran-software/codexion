import DocsWrapper from "../DocsWrapper";
import AdverthismentBanner from "../../../../../resources/UIBlocks/Promotion/AdverthismentBanner";
import CustomAdverthismentBanner from "../../../../../resources/UIBlocks/Promotion/CustomAdverthismentBanner";
import AdvertisementBanner2 from "../../../../../resources/UIBlocks/Promotion/AdvertisementBanner2";
import PromotionSection from "../../../../../resources/UIBlocks/Promotion/PromotionSection";
import ScrollAdverthisment2 from "../../../../../resources/UIBlocks/Promotion/ScrollAdverthisment2";
import ScrollAdverthisment from "../../../../../resources/UIBlocks/Promotion/ScrollAdverthisment";

function PromotionBlock() {
  return (
    <div className="flex flex-col gap-10">
      <DocsWrapper
        title="AdverthismentBanner"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/Promotion/AdverthismentBanner",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <AdverthismentBanner
          api="/api/products?limit=5" // 👈 Your backend API
          autoPlay={true} // default true
          delay={4000} // slide delay in ms (default 6000)
        />
      </DocsWrapper>

      <DocsWrapper
        title="CustomAdverthismentBanner"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/Promotion/CustomAdverthismentBanner",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <CustomAdverthismentBanner
          api={`api/resource/Slider 2`}
          delay={6000}
          sliderBase={"Slider - 1"}
        />
      </DocsWrapper>

      <DocsWrapper
        title="AdvertisementBanner2"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/Promotion/AdvertisementBanner2",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <AdvertisementBanner2 />
      </DocsWrapper>

      <DocsWrapper
        title="PromotionSection"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/Promotion/PromotionSection",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <PromotionSection
          api={`api/resource/Promotional Special?fields=["name"]&filters=[["set_default", "=", 1]]`}
        />
      </DocsWrapper>

      <DocsWrapper
        title="ScrollAdverthisment"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/Promotion/ScrollAdverthisment",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <ScrollAdverthisment
          title="Trending Products"
          api="/api/resource/Item?filters=%5B%5D&fields=%5B%22name%22%5D"
        />
      </DocsWrapper>

      <DocsWrapper
        title="ScrollAdverthisment2"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/Promotion/ScrollAdverthisment2",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <ScrollAdverthisment2
          title="Featured Brands"
          api={`api/resource/Promotional Image`}
        />
      </DocsWrapper>
    </div>
  );
}

export default PromotionBlock;
