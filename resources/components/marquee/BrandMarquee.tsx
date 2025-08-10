import React from "react";
import { motion } from "framer-motion";

type Brand = {
  name: string;
  logo?: string;
};

interface BrandMarqueeProps {
  type: "logo" | "label" | "big-text";
  brands: Brand[];
  speed?: number;
}

const BrandMarquee: React.FC<BrandMarqueeProps> = ({
  type,
  brands,
  speed = 30,
}) => {
  // Duplicate items for seamless loop
  const marqueeItems = [...brands, ...brands];

  return (
    <div
      className={`relative w-full overflow-hidden ${
        type === "big-text" ? "bg-black py-6" : "bg-white py-4"
      }`}
    >
      {/* Gradient fade for big-text */}
      {type === "big-text" && (
        <>
          <div className="pointer-events-none absolute top-0 left-0 h-full w-16 bg-gradient-to-r from-black to-transparent z-10"></div>
          <div className="pointer-events-none absolute top-0 right-0 h-full w-16 bg-gradient-to-l from-black to-transparent z-10"></div>
        </>
      )}

      {/* The magic: two identical sets side-by-side */}
      <motion.div
        className={`flex ${
          type === "big-text" || type === "label"
            ? "gap-16 whitespace-nowrap"
            : "gap-8"
        }`}
        animate={{ x: ["0%", "-50%"] }}
        transition={{
          repeat: Infinity,
          ease: "linear",
          duration: speed,
        }}
      >
        {marqueeItems.map((brand, idx) => (
          <div
            key={idx}
            className="flex-shrink-0 flex flex-col gap-15 items-center justify-center"
          >
            {type === "logo" && brand.logo ? (
              <img
                src={brand.logo}
                alt={brand.name}
                className="h-36 w-auto mx-5 object-contain grayscale hover:grayscale-0 transition duration-300"
              />
            ) : type === "big-text" ? (
              <span className="text-white text-6xl md:text-8xl font-extrabold uppercase tracking-wide hover:text-yellow-400 transition-colors duration-300">
                {brand.name}
              </span>
            ) : (
              <span className="text-lg font-semibold text-gray-700 hover:text-black transition duration-300">
                {brand.name}
              </span>
            )}
          </div>
        ))}
      </motion.div>
    </div>
  );
};

export default BrandMarquee;
