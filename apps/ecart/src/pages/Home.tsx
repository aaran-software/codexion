import ProductCard from "../../../../resources/UIBlocks/ProductCard";
import BannerCarousel from "../../../../resources/UIBlocks/BannerCarousel";
import GroupProductCard from "../../../../resources/UIBlocks/GroupProductCard";
import ProductCard2 from "../../../../resources/UIBlocks/ProductCard2";
import AdverthismentBanner from "../../../../resources/UIBlocks/Promotion/AdverthismentBanner";
import PromotionSection from "../../../../resources/UIBlocks/Promotion/PromotionSection";
import ScrollAdverthisment from "../../../../resources/UIBlocks/Promotion/ScrollAdverthisment";
import Mainmenu from "../../../../resources/UIBlocks/Mainmenu";

function Home() {
  return (
    <div>
      <Mainmenu />
      <BannerCarousel
        api={`api/resource/Product?fields=["name"]&filters=[["is_slider", "=", 1]]`}
        delay={6000}
      />
      <div className="px-[5%]">
        <ProductCard
          title="Popular Items"
          api={`api/resource/Product?fields=["name"]&filters=[["is_popular", "=", 1]]`}
          ribbon={true}
        />
      </div>

      <div className="flex flex-col md:flex-row gap-5 px-[5%]">
        <GroupProductCard
          title={"Hot Gadgets Today"}
          api={`api/resource/Product?fields=["name"]&filters=[["top_rated", "=", 1]]`}
        />
        <GroupProductCard
          title="Discount for you"
          api={`api/resource/Product?fields=["name"]&filters=[["is_discount", "=", 1]]`}
        />
      </div>
      <div className="px-[5%] py-5">
        <AdverthismentBanner
          api={`api/resource/Product?fields=["name"]&filters=[["is_slider", "=", 1]]`}
          delay={6000}
        />
      </div>

      <div className="px-[5%]">
        <ProductCard
          title="Laptops"
          api={`api/resource/Product?fields=["name"]&filters=[["is_popular", "=", 1]]`}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 px-[5%]">
        <GroupProductCard
          title={"Top Rated"}
          api={`api/resource/Product?fields=["name"]&filters=[["top_rated", "=", 1]]`}
        />
        <GroupProductCard
          title="Best Sellers"
          api={`api/resource/Product?fields=["name"]&filters=[["is_discount", "=", 1]]`}
        />
        <div className="lg:flex items-center h-full border border-ring/30 rounded-md p-1 hidden">
          <PromotionSection />
        </div>
      </div>
      <ScrollAdverthisment
        title="Featured Brands"
        api={`api/resource/Product?fields=["name"]&filters=[["is_popular", "=", 1]]`}
      />
      <ProductCard2
        title="Popular Items"
        api={`api/resource/Product?fields=["name"]&filters=[["is_popular", "=", 1]]`}
      />
    </div>
  );
}

export default Home;
