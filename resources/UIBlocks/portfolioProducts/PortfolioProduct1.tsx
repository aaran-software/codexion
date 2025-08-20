import { useInView } from "react-intersection-observer";

type PortfolioItem = {
  image: string;
  title: string;
  description: string;
};

type PortfolioProduct1Props = {
  item: PortfolioItem;
  reverse?: boolean;
};

function PortfolioProduct1({ item, reverse = false }: PortfolioProduct1Props) {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.2 });

  const animationClass = inView
    ? reverse
      ? "animate__fadeInLeft"
      : "animate__fadeInRight"
    : "";
  const animationClass2 = inView
    ? reverse
      ? "animate__fadeInRight"
      : "animate__fadeInLeft"
    : "";

  return (
    <div>
      <div
        className={`flex flex-col md:flex-row ${
          reverse ? "md:flex-row-reverse" : ""
        } items-center gap-6`}
        ref={ref}
        style={{ animationDelay: `${0.5}s` }}
      >
        {/* Image */}
        <div className={`w-full md:w-1/2 animate__animated ${animationClass2}`}>
          <img
            src={item.image}
            alt={item.title}
            className="w-full h-96 m-2 object-scale-down rounded-lg"
          />
        </div>

        {/* Text */}
        <div
          className={`w-full md:w-1/2 text-center md:text-left animate__animated ${animationClass}`}
        >
          <h1 className="text-2xl font-bold mb-2">{item.title}</h1>
          <h3 className="text-lg text-gray-600 text-justify">
            {item.description}
          </h3>
        </div>
      </div>
    </div>
  );
}

export default PortfolioProduct1;
