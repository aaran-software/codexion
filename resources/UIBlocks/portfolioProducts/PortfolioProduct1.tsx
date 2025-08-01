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
  return (
    <div className="">
      <div
        className={`flex flex-col md:flex-row ${
          reverse ? 'md:flex-row-reverse' : ''
        } items-center gap-6`}
      >
        {/* Image */}
        <div className="w-full md:w-1/2">
          <img
            src={item.image}
            alt={item.title}
            className="w-full h-96 m-2 object-scale-down rounded-lg"
          />
        </div>

        {/* Text */}
        <div className="w-full md:w-1/2 text-center md:text-left">
          <h1 className="text-2xl font-bold mb-2">{item.title}</h1>
          <h3 className="text-lg text-gray-600">{item.description}</h3>
        </div>
      </div>
    </div>
  );
}

export default PortfolioProduct1;
