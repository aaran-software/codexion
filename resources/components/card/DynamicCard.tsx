
interface CardList {
  image: string;
  title: string;
}

interface DynamicCardProps {
  Card: CardList[];
  rounded?:boolean
  containerStyle?:string
}

function DynamicCard({ Card, rounded=false,containerStyle }: DynamicCardProps) {
  return (
    <div className={`grid gap-6 ${containerStyle}`}>
      {Card.map((card, index) => (
        <div key={index} className=" p-4 block m-auto">
          <img src={card.image} alt={card.title} className={` object-cover rounded ${rounded ? "w-64 h-64 rounded-full":"w-full h-64 "}`} />
          <h1 className="text-xl text-center font-semibold mt-2">{card.title}</h1>
        </div>
      ))}
    </div>
  );
}

export default DynamicCard;
