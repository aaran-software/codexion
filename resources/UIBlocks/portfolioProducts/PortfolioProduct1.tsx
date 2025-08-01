type PortfolioItem = {
  image: string;
  title: string;
  description: string;
};

type PortfolioProduct1Props = {
  items: PortfolioItem[];
};

function PortfolioProduct1({ items }: PortfolioProduct1Props) {
  return (
    <div className="w-full">
      {items.map((item, index) => {
        const reverse = index % 2 === 0;

        return (
          <div key={index} className="py-8">
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
                  className="w-full h-auto object-cover rounded-lg"
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
      })}
    </div>
  );
}

export default PortfolioProduct1;
