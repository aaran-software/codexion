
interface PromotionSectionProps{
  image:string;
}

function PromotionSection({image}:PromotionSectionProps) {
  return (
    <div className="w-full h-max">
        <img src={image} alt="" className="object-scale-down" />
    </div>
  )
}

export default PromotionSection