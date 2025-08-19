import React from "react";

interface CardData {
  title: string;
  description: string;
  image: string;
  hoverColor: string;
}

interface AnimatedCardProps {
  cards: CardData[];
  title: string;
  description: string;
}

const AnimatedCard: React.FC<AnimatedCardProps> = ({
  title,
  description,
  cards,
}) => {
  return (
    <div>
      <h1 className="text-center text-4xl font-bold py-5">{title}</h1>
      <h1 className="text-center pb-5">{description}</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 px-[10%]
      ">
        {cards.map((card, index) => (
          <div
            key={index}
            className={`
            relative group bg-white shadow-lg rounded-2xl overflow-hidden cursor-pointer mt-5
          `}
          >
            {/* Gradient Overlay from bottom */}
            <div
              className={`absolute inset-0 bg-gradient-to-t ${card.hoverColor} opacity-0 group-hover:opacity-90 transition-opacity duration-500`}
            ></div>

            {/* Image/Icon */}
            <div className="flex justify-center p-6">
              <img
                src={card.image}
                alt={card.title}
                loading="lazy"
                className="w-full object-contain transition-transform duration-500 group-hover:scale-110"
              />
            </div>

            <div className="relative px-6 text-center transition-all duration-500 group-hover:-translate-y-6">
              {/* Title */}
              <h3 className="text-2xl font-semibold text-gray-800 group-hover:text-white transition-colors">
                {card.title}
              </h3>

              {/* Description (hidden until hover) */}
              <p className="text-sm text-gray-500 mt-3 opacity-0 group-hover:opacity-100 group-hover:text-white transition-opacity duration-500">
                {card.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AnimatedCard;


// <AnimatedCard
//         cards={cardData}
//         title={"Our Products"}
//         description={
//           "Explore our wide range of products crafted with quality and precision. Designed to meet your needs and deliver the best experience."
//         }
//       />
//       const cardData = [
//     {
//       title: "ERPNext Customization",
//       description:
//         "Tailored ERPNext solutions to streamline your business operations with automation, reporting, and scalability.",
//       image: "assets/svg/animatesvg/dashboard.svg",
//       hoverColor: "from-primary via-primary/0 to-primary/0",
//     },
//     {
//       title: "QBill – Smart Billing",
//       description:
//         "Simplify invoicing, track payments, and manage accounts effortlessly with our secure billing software.",
//       image: "assets/svg/animatesvg/qbilling.svg",
//       hoverColor: "from-primary via-primary/0 to-primary/0",
//     },
//     {
//       title: "eCart Solutions",
//       description:
//         "Custom e-commerce platforms with product management, payment integration, and advanced analytics.",
//       image: "assets/svg/animatesvg/ecart.svg",
//       hoverColor: "from-primary via-primary/0 to-primary/0",
//     },
//   ];