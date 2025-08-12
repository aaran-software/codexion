interface PromotionSectionProps {
  image: string;
}

function PromotionSection({ image }: PromotionSectionProps) {
  return (
    <img
      src="/assets/Promotion/ads3.png"
      alt=""
      className="w-full h-full object-cover rounded-md"
    />
  );
}

export default PromotionSection;
