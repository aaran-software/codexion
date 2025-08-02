import { useInView } from 'react-intersection-observer';

interface CardList {
  image: string;
  title: string;
  animate: string;
}

interface DynamicCardProps {
  Card: CardList[];
  rounded?: boolean;
  containerStyle?: string;
}

function DynamicCard({ Card, rounded = false, containerStyle }: DynamicCardProps) {
  return (
    <div className={`grid gap-6 ${containerStyle}`}>
      {Card.map((card, index) => {
        const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.2 });

        return (
          <div
            ref={ref}
            key={index}
            className={`p-4 block m-auto transition-all duration-700 ${
              inView ? card.animate : 'opacity-0'
            }`}
          >
            <img
              src={card.image}
              alt={card.title}
              className={`object-cover ${
                rounded ? 'w-64 h-64 rounded-full' : 'w-full h-64 rounded'
              }`}
            />
            <h1 className="text-xl text-center font-semibold mt-2">{card.title}</h1>
          </div>
        );
      })}
    </div>
  );
}

export default DynamicCard;
