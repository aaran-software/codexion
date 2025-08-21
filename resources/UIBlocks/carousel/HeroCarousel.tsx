// HeroCarousel.tsx
import React from "react";
import { motion } from "framer-motion";
import Carousel from "../../components/carousel";

export type Slide = {
  id: string | number;
  bgClass?: string;     
  title1: string;
  title2?: string;
  description: string;
  image: string;
};

export type HeroCarouselProps = {
  slides: Slide[];
  autoSlide?: boolean;
  autoSlideInterval?: number;
};

const HeroCarousel: React.FC<HeroCarouselProps> = ({
  slides,
  autoSlide = true,
  autoSlideInterval = 7000,
}) => {
  // Motion variants for staggered animations
  const textVariant = (delay: number) => ({
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.8, delay } },
  });

  const imageVariant = (delay: number) => ({
    hidden: { opacity: 0, scale: 0.95 },
    visible: { opacity: 1, scale: 1, transition: { duration: 0.8, delay } },
  });

  return (
    <Carousel autoSlide={autoSlide} autoSlideInterval={autoSlideInterval}>
      {slides.map((slide, index) => (
        <div
          key={slide.id}
          className={`lg:px-[12%] py-10 ${slide.bgClass}`}
        >
          <div
            className={`flex ${
              index % 2 === 0
                ? "md:flex-row gap-5 flex-col"
                : "md:flex-row-reverse gap-5 flex-col-reverse"
            } w-full lg:py-20 ${slide.bgClass}`}
          >
            {/* Text Section */}
            <div
              className={`md:w-[50%] flex flex-col md:px-5 justify-center items-center md:items-start md:py-10 ${
                index % 2 === 0 ? "" : "lg:pl-20"
              } lg:py-0 gap-4 md:gap-8`}
            >
              <motion.div
                initial="hidden"
                whileInView="visible"
                viewport={{ once: false }}
              >
                <motion.h1
                  variants={textVariant(0.2)}
                  className="text-2xl lg:text-4xl xl:text-5xl font-bold text-center md:text-start"
                >
                  {slide.title1}
                </motion.h1>
                {slide.title2 && (
                  <motion.h1
                    variants={textVariant(0.4)}
                    className="text-2xl lg:text-4xl xl:text-5xl font-bold text-center mt-2 md:text-start"
                  >
                    {slide.title2}
                  </motion.h1>
                )}
              </motion.div>
              <motion.h4
                variants={textVariant(0.6)}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: false }}
                className="text-lg text-center md:text-left px-5 md:px-0 leading-tight line-clamp-2 md:leading-snug max-w-xl"
              >
                {slide.description}
              </motion.h4>
            </div>

            {/* Image Section */}
            <motion.div
              className="sm:w-[50%] w-[70%] block mx-auto"
              variants={imageVariant(0.8)}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: false }}
            >
              <img
                src={slide.image}
                alt="Hero Slide"
                className="block mx-auto"
                loading="lazy"
              />
            </motion.div>
          </div>
        </div>
      ))}
    </Carousel>
  );
};

export default HeroCarousel;
