import React from "react";
import { motion } from "framer-motion";

type Roadmap2Item = {
  year?: string; // ✅ made optional
  title: string;
  description: string;
  icon?: React.ReactNode;
  color?: string;
  image?: string;
};

interface Roadmap2Props {
  items: Roadmap2Item[];
  RoadmapHeading: string;
}

const Roadmap2: React.FC<Roadmap2Props> = ({ items, RoadmapHeading }) => {
  return (
    <section className="overflow-x-hidden py-10">
      <h2 className="text-4xl font-bold text-center mb-15">{RoadmapHeading}</h2>

      <div className="relative max-w-6xl mx-auto">
        {/* Desktop line (center) */}
        <div className="absolute left-1/2 top-0 h-full w-1 bg-primary -translate-x-1/2 hidden sm:block" />
        {/* Mobile line (left) */}
        <div className="absolute left-5.5 top-0 h-full w-1 bg-primary sm:hidden" />

        <div className="space-y-20">
          {items.map((item, index) => {
            const isLeft = index % 2 === 0;

            return (
              <div key={index} className="relative flex w-full">
                {/* Desktop layout (zigzag with image) */}
                <div className="hidden sm:flex w-full">
                  {isLeft ? (
                    <>
                      {/* Content Left */}
                      <motion.div
                        initial={{ opacity: 0, x: -200 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: false, amount: 0.3 }}
                        transition={{
                          type: "spring",
                          stiffness: 60,
                          damping: 12,
                        }}
                        className="w-1/2 pr-10 text-right flex justify-end"
                      >
                        <div className="rounded-2xl p-6 relative max-w-md">
                          {item.year && (
                            <h3 className="text-xl font-semibold">{item.year}</h3>
                          )}
                          <p className="text-lg font-medium text-gray-700 mt-1">
                            {item.title}
                          </p>
                          <p className="text-gray-500 mt-2">
                            {item.description}
                          </p>
                        </div>
                      </motion.div>

                      {/* Image Right */}
                      <motion.div
                        initial={{ opacity: 0, x: 200 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: false, amount: 0.3 }}
                        transition={{
                          type: "spring",
                          stiffness: 60,
                          damping: 12,
                        }}
                        className="w-1/2 pl-10 flex justify-start items-center"
                      >
                        {item.image && (
                          <img
                            src={item.image}
                            alt={item.title}
                            className="rounded-xl shadow-lg max-h-64 object-cover"
                          />
                        )}
                      </motion.div>
                    </>
                  ) : (
                    <>
                      {/* Image Left */}
                      <motion.div
                        initial={{ opacity: 0, x: -200 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: false, amount: 0.3 }}
                        transition={{
                          type: "spring",
                          stiffness: 60,
                          damping: 12,
                        }}
                        className="w-1/2 pr-10 flex justify-end items-center"
                      >
                        {item.image && (
                          <img
                            src={item.image}
                            alt={item.title}
                            className="rounded-xl shadow-lg max-h-64 object-cover"
                          />
                        )}
                      </motion.div>

                      {/* Content Right */}
                      <motion.div
                        initial={{ opacity: 0, x: 200 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: false, amount: 0.3 }}
                        transition={{
                          type: "spring",
                          stiffness: 60,
                          damping: 12,
                        }}
                        className="w-1/2 pl-10 text-left flex justify-start"
                      >
                        <div className="rounded-2xl p-6 relative max-w-md">
                          {item.year && (
                            <h3 className="text-xl font-semibold">{item.year}</h3>
                          )}
                          <p className="text-lg font-medium text-gray-700 mt-1">
                            {item.title}
                          </p>
                          <p className="text-gray-500 mt-2">
                            {item.description}
                          </p>
                        </div>
                      </motion.div>
                    </>
                  )}
                </div>

                {/* Mobile layout (< md) */}
                <div className="flex sm:hidden w-full relative">
                  {/* Pin marker + connector */}
                  <div className="absolute left-0 w-12 flex flex-col items-center">
                    <PinMarker
                      year={item.year}
                      color={item.color}
                      icon={item.icon}
                    />

                    {index !== items.length - 1 && (
                      <div
                        className="flex-1 w-[2px]"
                        style={{ backgroundColor: item.color || "#d1d5db" }}
                      />
                    )}
                  </div>

                  {/* Image + Content */}
                  <div className="ml-16 flex-1 flex flex-col space-y-4">
                    {item.image && (
                      <motion.img
                        src={item.image}
                        alt={item.title}
                        initial={{ opacity: 0, y: 40 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: false, amount: 0.2 }}
                        transition={{
                          type: "spring",
                          stiffness: 60,
                          damping: 12,
                        }}
                        className="rounded-xl shadow-lg max-h-60 object-cover w-full"
                      />
                    )}

                    <motion.div
                      initial={{ opacity: 0, y: 40 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: false, amount: 0.2 }}
                      transition={{
                        type: "spring",
                        stiffness: 60,
                        damping: 12,
                      }}
                      className="flex-1 w-full"
                    >
                      <div className="rounded-xl border-b-3 border-ring/40 p-4">
                        {item.year && (
                          <h3 className="text-lg font-semibold">{item.year}</h3>
                        )}
                        <p className="text-md font-medium text-gray-700 mt-1">
                          {item.title}
                        </p>
                        <p className="text-gray-500 mt-1 text-sm">
                          {item.description}
                        </p>
                      </div>
                    </motion.div>
                  </div>
                </div>

                {/* Desktop Pin Marker */}
                <div className="absolute left-1/2 -translate-x-1/2 hidden sm:flex items-center justify-center">
                  <PinMarker
                    year={item.year}
                    color={item.color}
                    icon={item.icon}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Roadmap2;

/* 📍 Pin Marker */
const PinMarker: React.FC<{
  year?: string; // ✅ optional now
  color?: string;
  icon?: React.ReactNode;
}> = ({ year, color, icon }) => {
  return (
    <div className="relative flex flex-col items-center">
      <div
        className="w-12 h-12 rounded-full flex items-center justify-center shadow-md relative z-10"
        style={{ backgroundColor: color || "#2563eb" }}
      >
        {icon ||
          (year ? (
            <span className="text-white font-bold text-sm">
              {year.slice(-2)}
            </span>
          ) : null)}
      </div>
      {/* Tail */}
      <div
        className="w-0 h-0 border-l-[10px] border-r-[10px] border-t-[16px] -mt-1"
        style={{
          borderLeftColor: "transparent",
          borderRightColor: "transparent",
          borderTopColor: color || "#2563eb",
        }}
      />
    </div>
  );
};
