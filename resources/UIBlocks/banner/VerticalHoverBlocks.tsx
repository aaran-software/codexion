import React, { useState } from "react";
import { ArrowRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

type Section = {
  label: string;
  title: string;
  description: string;
  image: string;
  date?: string;
  ctaText?: string;
};

type Props = {
  sections: Section[];
};

const VerticalHoverBlocks: React.FC<Props> = ({ sections }) => {
  const [activeIndex, setActiveIndex] = useState(0);

  const activeItem = sections[activeIndex];
  const leftItems = sections.slice(0, activeIndex);
  const rightItems = sections.slice(activeIndex + 1);

  return (
    <motion.div
      layout
      className="flex flex-col md:flex-row items-center justify-center p-6 gap-6"
    >
      <motion.div layout className="flex flex-col md:flex-row items-stretch gap-6 w-full">
        {/* LEFT BAR */}
        <motion.div
          layout
          className="hidden md:flex flex-row items-center justify-center px-4 rounded-2xl h-[450px] gap-3"
        >
          <AnimatePresence initial={false}>
            {leftItems.map((item) => {
              const index = sections.indexOf(item);
              return (
                <motion.div
                  key={item.label}
                  layout
                  initial={{ x: -40, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: -40, opacity: 0 }}
                  transition={{ duration: 0.75 }}
                  onMouseEnter={() => setActiveIndex(index)}
                  className="cursor-pointer w-28 h-full text-4xl rounded-xl flex items-center justify-center shadow-md bg-primary text-primary-foreground"
                >
                  <span className="md:-rotate-90 font-extrabold whitespace-nowrap">
                    {item.label}
                  </span>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </motion.div>

        {/* ACTIVE CARD */}
        <motion.div
          layout
          transition={{ duration: 0.45, ease: "easeInOut" }}
          className="flex-1 flex flex-col md:flex-row w-full bg-white border border-ring/30 rounded-2xl shadow-xl overflow-hidden h-[450px]"
        >
          <div className="flex-1 flex flex-col md:flex-row items-center justify-between px-6 py-8 md:px-12 relative">
            {/* Text */}
            <motion.div
              layout
              className="max-w-2xl text-center md:text-left"
            >
                 <h2 className="text-2xl md:text-xl text-primary font-extrabold leading-snug mb-5">
                {activeItem.label}
              </h2>
              {activeItem.date && (
                <p className="text-sm font-semibold text-gray-500 mb-4">
                  {activeItem.date}
                </p>
              )}
              <h2 className="text-2xl md:text-4xl font-extrabold leading-snug mb-5 line-clamp-2">
                {activeItem.title}
              </h2>
              <p className="text-gray-600 text-base md:text-lg leading-7 mb-8 line-clamp-3">
                {activeItem.description}
              </p>
              <button className="inline-flex items-center gap-2 bg-blue-600 text-white px-5 py-3 rounded-md hover:bg-blue-700 transition">
                {activeItem.ctaText ?? "Read More"} <ArrowRight size={18} />
              </button>
            </motion.div>

            {/* Image */}
            <motion.div
              layout
              className="mt-6 md:mt-0 md:pr-6 flex-shrink-0"
            >
              <img
                src={activeItem.image}
                alt={activeItem.title}
                className="w-[350px] h-[350px] object-cover rounded-xl shadow-md"
              />
            </motion.div>
          </div>
        </motion.div>

        {/* RIGHT BAR */}
        <motion.div
          layout
          className="flex md:flex-row justify-center gap-3 mt-4 md:mt-0"
        >
          <AnimatePresence initial={false}>
            {rightItems.map((item) => {
              const index = sections.indexOf(item);
              return (
                <motion.div
                  key={item.label}
                  layout
                  initial={{ x: 40, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: 40, opacity: 0 }}
                  transition={{ duration: 0.35 }}
                  onMouseEnter={() => setActiveIndex(index)}
                  className="cursor-pointer w-28 h-full rounded-xl bg-primary text-white flex items-center justify-center shadow-md"
                >
                  <span className="md:-rotate-90 font-extrabold whitespace-nowrap text-4xl">
                    {item.label}
                  </span>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </motion.div>
      </motion.div>
    </motion.div>
  );
};

export default VerticalHoverBlocks;
