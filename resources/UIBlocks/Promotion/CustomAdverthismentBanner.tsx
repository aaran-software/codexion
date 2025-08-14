import React, { useState, useEffect, useRef } from "react";
import apiClient from "../../../resources/global/api/apiClients";
import { useAppContext } from "../../../apps/global/AppContaxt";
import Button from "../../../resources/components/button/Button";

interface SlideContent {
  image: string;
  bg_image: string;
  title: string;
  description?: string;
  price?: number;
  slogan?: string;
  discount?: string;
  layout?: string;
  theme: string;
}

interface CustomBannerCarouselProps {
  api: string;
  autoPlay?: boolean;
  delay?: number; // milliseconds
}

const CustomBannerCarousel: React.FC<CustomBannerCarouselProps> = ({
  api,
  autoPlay = true,
  delay = 6000,
}) => {
  const { API_URL } = useAppContext();

  const [activeIndex, setActiveIndex] = useState(0);

  const requestRef = useRef<number | null>(null);
  const startTimeRef = useRef<number | null>(null);
  //  Add swipe handler functions:
  const touchStartX = useRef<number | null>(null);
  const touchEndX = useRef<number | null>(null);

  const handleTouchStart = (e: React.TouchEvent<HTMLDivElement>) => {
    touchStartX.current = e.touches[0].clientX;
  };

  const handleTouchMove = (e: React.TouchEvent<HTMLDivElement>) => {
    touchEndX.current = e.touches[0].clientX;
  };

  const handleTouchEnd = () => {
    if (!touchStartX.current || !touchEndX.current) return;

    const distance = touchStartX.current - touchEndX.current;
    const threshold = 50; // Minimum swipe distance

    if (distance > threshold) {
      // Swiped left
      goToSlide((activeIndex + 1) % slides.length);
    } else if (distance < -threshold) {
      // Swiped right
      goToSlide(activeIndex === 0 ? slides.length - 1 : activeIndex - 1);
    }

    // Reset
    touchStartX.current = null;
    touchEndX.current = null;
  };

  const [slides, setSlides] = useState<SlideContent[]>([]);
  const fetchProducts = async () => {
    try {
      // Step 1: Fetch all item names
      const response = await apiClient.get(`${api}`);

      const items = response.data.data || [];
      const baseApi = api.split("?")[0];

      // Step 2: Fetch full details for each item
      const detailPromises = items.map((item: any) => {
        const itemName = encodeURIComponent(item.name);
        const detailUrl = `${baseApi}/${itemName}`;
        return apiClient
          .get(detailUrl)
          .then((res) => res.data.data)
          .catch((err) => {
            console.warn(`Item not found: ${item.name}`, err);
            return null;
          });
      });

      const detailResponses = await Promise.all(detailPromises);
      const validItems = detailResponses.filter(Boolean);

      const formatted: SlideContent[] = validItems.map((item: any) => {
        return {
          id: item.name,
          title: item.title, // or item.item_name if you want full name
          image: `${API_URL}/${item.product_image}`,
          bg_image: `${API_URL}/${item.background}`,
          description: item.describtion,
          discount: item.stock_qty,
          price: item.price,
          slogan: item.slogan,
          layout: item.layout,
          theme: item.theme,
        };
      });

      setSlides(formatted);
    } catch (error) {
      console.error("Failed to fetch products:", error);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);
  const goToSlide = (index: number) => {
    setActiveIndex(index);
    startTimeRef.current = null;
  };

  const goToNext = () => {
    goToSlide((activeIndex + 1) % slides.length);
  };

  const animate = (timestamp: number) => {
    if (!startTimeRef.current) {
      startTimeRef.current = timestamp;
    }

    const elapsed = timestamp - startTimeRef.current;
    const progress = Math.min(elapsed / delay, 3);

    if (progress < 1) {
      requestRef.current = requestAnimationFrame(animate);
    } else {
      goToNext();
    }
  };

  useEffect(() => {
    if (!autoPlay || slides.length === 0) return;

    let animationFrameId: number;
    let startTime: number | null = null;

    const step = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const elapsed = timestamp - startTime;

      if (elapsed < delay) {
        animationFrameId = requestAnimationFrame(step);
      } else {
        goToNext();
      }
    };

    animationFrameId = requestAnimationFrame(step);

    return () => {
      cancelAnimationFrame(animationFrameId);
      startTime = null;
    };
  }, [activeIndex, slides.length, autoPlay, delay]);

  return (
    <div className="relative w-full h-[350px] md:h-[350px] bg-background overflow-hidden">
      {/* 🔹 Slides */}
      <div
        className="w-full h-full relative flex transition-transform duration-700 ease-in-out"
        style={{ transform: `translateX(-${activeIndex * 100}%)` }}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {slides.map((slide, index) => (
          <div
            key={index}
            className="w-full h-full flex border-y border-ring/30 flex-shrink-0"
          >
            {slide.layout === "Option - 1" ? (
              <div
                className={`w-full h-[350px] flex items-center justify-center relative ${slide.theme === "dark" ? "text-black" : "text-white"}`}
              >
                {/* Background Image */}
                <img
                  src={slide.bg_image}
                  alt={`Slide ${index}`}
                  className="h-full w-full object-cover"
                />
                <div className="absolute inset-0 bg-black/20"></div>
                <div className="absolute left-10 sm:left-25 lg:left-60 flex flex-col gap-3 right-1/2 pr-2 top-1/2 -translate-y-1/2 text-white">
                  {slide.title && (
                    <p className="text-lg sm:text-2xl md:text-2xl lg:text-4xl font-bold">
                      {slide.title}
                    </p>
                  )}

                  {slide.description && (
                    <p className="mt-2 text-xs sm:text-sm md:text-lg lg:text-lg">
                      {slide.description}
                    </p>
                  )}

                  {slide.price !== undefined && (
                    <p className="mt-2 text-xl lg:text-5xl font-bold text-right">
                      ₹ {slide.price}
                    </p>
                  )}

                  <Button
                    label="Shop Now"
                    className="border border-primary w-max text-primary hover:text-white hover:bg-hover"
                  />
                </div>

                {/* Foreground Product Image */}
                <img
                  src={slide.image}
                  alt={`Slide ${index} product`}
                  className="absolute right-1 sm:right-1/18 md:right-1/15 lg:right-1/8 top-1/2 -translate-y-1/2 max-h-[50%] sm:max-h-[60%] lg:max-h-[80%] object-scale-down"
                />

                {/* Centered Blockquote at Bottom */}
                {slide.slogan && (
                  <blockquote className="absolute bottom-8 left-1/2 -translate-x-1/2 italic text-sm md:text-lg lg:text-xl font-bold text-center whitespace-nowrap">
                    {slide.slogan}
                  </blockquote>
                )}
              </div>
            ) : slide.layout === "Option - 2" ? (
              <div
                className={`w-full h-[350px] flex items-center justify-center relative ${slide.theme === "dark" ? "text-black" : "text-white"}`}
              >
                {/* Background Image */}
                <img
                  src={slide.bg_image}
                  alt={`Slide ${index}`}
                  className="h-full w-full object-fit lg:object-cover"
                />

                {/* Bottom Content Section with dimmed background */}
                <div className="absolute bottom-0 left-0 w-full bg-black/60 px-[10%] py-4 flex flex-row gap-6 items-center text-white">
                  {/* Left Column */}
                  <div className="flex-1">
                    {slide.title && (
                      <p className="text-lg sm:text-2xl font-bold text-background">
                        {slide.title}
                      </p>
                    )}

                    {slide.description && (
                      <p className="mt-2 text-xs sm:text-sm md:text-md text-background">
                        {slide.description}
                      </p>
                    )}

                    {slide.price !== undefined && (
                      <p className="mt-2 text-xl font-bold text-background">
                        ₹ {slide.price}
                      </p>
                    )}
                  </div>

                  {/* Right Column */}
                  <div className="flex-1">
                    {slide.slogan && (
                      <blockquote className="italic text-sm md:text-lg lg:text-xl font-bold text-background text-right">
                        {slide.slogan}
                      </blockquote>
                    )}
                  </div>
                </div>
              </div>
            ) : slide.layout === "Option - 3" ? (
              <div
                className={`w-full h-[350px] flex items-center justify-center relative ${slide.theme === "dark" ? "text-black" : "text-white"}`}
              >
                {/* Background Image */}
                <img
                  src={slide.bg_image}
                  alt={`Slide ${index}`}
                  className="h-full w-full object-cover"
                />

                {/* Overlay Dark Layer */}
                <div className="absolute inset-0 bg-black/10"></div>
                {/* Foreground Image */}

                <img
                  src={slide.image}
                  alt={`Slide ${index} product`}
                  className="absolute left-5 sm:left-1/6 lg:left-1/5 top-1/2 -translate-y-1/2 max-h-[30%] sm:max-h-[40%] lg:max-h-[80%] object-contain"
                />

                <div className="absolute lg:right-40 flex flex-col gap-3 left-1/2 pr-2 top-1/2 -translate-y-1/2 text-white">
                  {slide.title && (
                    <p className="text-lg sm:text-2xl md:text-2xl lg:text-4xl font-bold text-foreground">
                      {slide.title}
                    </p>
                  )}

                  {slide.description && (
                    <p className="mt-2 text-xs sm:text-sm md:text-lg lg:text-lg text-purple-500">
                      {slide.description}
                    </p>
                  )}

                  {slide.price && (
                    <p className="mt-2 text-xl font-bold text-foreground">
                      ₹ {slide.price}
                    </p>
                  )}

                  {slide.slogan && (
                    <blockquote className="mt-4 italic text-sm md:text-lg lg:text-xl font-bold text-foreground">
                      {slide.slogan}
                    </blockquote>
                  )}

                  <Button
                    label="Shop Now"
                    className="border border-ring/30 w-max text-primary hover:text-white hover:bg-hover"
                  />
                </div>
              </div>
            ) : slide.layout === "Option - 4" ? (
              <div
                className={`w-full h-[350px] flex items-center justify-center relative ${slide.theme === "dark" ? "text-black" : "text-white"}`}
              >
                {/* Background Image */}
                <img
                  src={slide.bg_image}
                  alt={`Slide ${index}`}
                  className="h-full w-full object-cover"
                />

                {/* Overlay Dark Layer */}
                <div className="absolute inset-0 bg-black/10"></div>

                {/* Left Side Content */}
                <div className="absolute left-10 sm:left-25 lg:left-60 flex flex-col gap-3 right-1/2 pr-2 top-1/2 -translate-y-1/2 text-white">
                  {slide.title && (
                    <p className="text-lg sm:text-2xl md:text-2xl lg:text-4xl font-bold text-foreground">
                      {slide.title}
                    </p>
                  )}

                  {slide.description && (
                    <p className="mt-5 text-xs sm:text-sm md:text-lg lg:text-lg text-purple-500">
                      {slide.description}
                    </p>
                  )}

                  {slide.price !== undefined && (
                    <p className="mt-2 text-xl lg:text-5xl font-bold text-foreground">
                      ₹ {slide.price}
                    </p>
                  )}

                  <Button
                    label="Shop Now"
                    className="border border-ring/30 w-max text-primary hover:text-white hover:bg-hover"
                  />
                </div>

                {/* Foreground Product Image */}
                <img
                  src={slide.image}
                  alt={`Slide ${index} product`}
                  className="absolute right-1 sm:right-1/18 md:right-1/15 lg:right-1/8 top-1/2 -translate-y-1/2 max-h-[50%] sm:max-h-[60%] lg:max-h-[80%] object-scale-down"
                />

                {/* Centered Blockquote at Bottom */}
                {slide.slogan && (
                  <blockquote className="absolute bottom-8 left-1/2 -translate-x-1/2 italic text-sm md:text-lg lg:text-xl font-bold text-foreground text-center whitespace-nowrap">
                    {slide.slogan}
                  </blockquote>
                )}
              </div>
            ) : (
              <div
                className={`w-full h-[350px] flex items-center justify-center relative ${slide.theme === "dark" ? "text-black" : "text-white"}`}
              >
                {/* Background Image */}
                <img
                  src={slide.bg_image}
                  alt={`Slide ${index}`}
                  className="h-full w-full object-cover"
                />
                <div className="absolute inset-0 bg-black/10"></div>

                {/* Foreground Product Image - positioned inside relative container */}
                <img
                  src={slide.image}
                  alt={`Slide ${index} product`}
                  className="absolute left-5 sm:left-1/6 lg:left-1/5 top-1/2 -translate-y-1/2 max-h-[30%] sm:max-h-[40%] lg:max-h-[80%] object-contain"
                />
                {/* Optional Right Side Content */}
                <div className="absolute lg:right-40 flex flex-col gap-3 left-1/2 pr-2 top-1/2 -translate-y-1/2">
                  {slide.title && (
                    <p className="text-lg sm:text-2xl md:text-2xl lg:text-4xl font-bold text-center">
                      {slide.title}
                    </p>
                  )}

                  {slide.description && (
                    <p className="mt-2 text-xs sm:text-sm md:text-lg lg:text-lg text-center">
                      {slide.description}
                    </p>
                  )}

                  {slide.price !== undefined && (
                    <p className="mt-2 text-xl md:text-4xl font-bold text-center">
                      ₹ {slide.price}
                    </p>
                  )}

                  {slide.slogan && (
                    <blockquote className="mt-4 italic text-sm md:text-lg lg:text-xl font-bold text-center">
                      {slide.slogan}
                    </blockquote>
                  )}

                  <Button
                    label="Shop Now"
                    className="border border-ring/30 w-max block mx-auto text-primary hover:text-white hover:bg-hover"
                  />
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Indicators */}
      <div className="absolute bottom-3 left-1/2 transform -translate-x-1/2 flex gap-2 z-20">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={() => goToSlide(index)}
            className={`w-3 h-3 rounded-full ${
              index === activeIndex
                ? "bg-primary"
                : "bg-white border border-ring/50"
            }`}
          />
        ))}
      </div>

      {/* Navigation Buttons */}

      {/* <ImageButton
        onClick={() =>
          goToSlide(activeIndex === 0 ? slides.length - 1 : activeIndex - 1)
        }
        className="absolute top-1/2 left-5 lg:left-10 -translate-y-1/2 bg-black/30 text-white p-2 sm:p-4 !rounded-full hover:bg-black/30 z-20 hidden md:block"
        icon={"left"}
      />
      <ImageButton
        onClick={() => goToSlide((activeIndex + 1) % slides.length)}
        className="absolute top-1/2 right-5 lg:right-10 -translate-y-1/2 bg-black/30 text-white p-2 sm:p-4 !rounded-full hover:bg-black/30 z-20 hidden md:block"
        icon={"right"}
      /> */}
    </div>
  );
};

export default CustomBannerCarousel;
