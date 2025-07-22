import ImageButton from "../../../Components/Button/ImageBtn";
import React, { useState, useEffect, useRef } from "react";
import Adbanner from "../../../../public/assets/adverthisment.png"
import apiClient from "../../../pages/app/ecart/api/apiClients";
interface SlideContent {
  image: string;
  title: string;
  description: string;
  price: number;
  discount?: string;
}

interface BannerCarouselProps {
  api: string;
  autoPlay?: boolean;
  delay?: number; // milliseconds
}

const BannerCarousel: React.FC<BannerCarouselProps> = ({
  api,
  autoPlay = true,
  delay = 6000,
}) => {
  const [activeIndex, setActiveIndex] = useState(0);
  const [remainingTime, setRemainingTime] = useState(delay / 1000);

  const requestRef = useRef<number | null>(null);
  const startTimeRef = useRef<number | null>(null);

  const radius = 20;
  const circumference = 2 * Math.PI * radius;

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
          title: item.display_name, // or item.item_name if you want full name
          image: `${item.image}`,
          description: item.short_describe,
          discount: item.stock_qty,
          price: item.price || item.standard_rate || 0,
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
    setRemainingTime(delay / 1000);
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
    const remaining = Math.max((delay - elapsed) / 1000, 0);
    setRemainingTime(remaining);

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
      const remaining = Math.max((delay - elapsed) / 1000, 0);

      setRemainingTime(remaining);

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

  const progressPercent = (1 - remainingTime / (delay / 1000)) * 100;
  const strokeDashoffset =
    circumference - (progressPercent / 100) * circumference;

  return (
    <div className="relative w-full h-[300px] md:h-[350px] bg-background overflow-hidden">

      {/* 🔹 Slides */}
      <div className="w-full h-full relative">
        {slides.map((slide, index) => (
          <div
            key={index}
            className={`absolute inset-0 w-full h-[350px] flex transition-opacity duration-300 ${
              index === activeIndex ? "opacity-100 z-10" : "opacity-0 z-0"
            }`}
          >
            {/* Left: Image */}
            <div className="w-full h-[350px] flex items-center justify-center">
              <img
                // src={`https://dev.aaranerp.com/${slide.image}`}
                src={Adbanner}
                alt={`Slide ${index} ${slide}`}
                className={`h-full w-full object-fit`}
              />
            </div>

            {/* Right: Text Content */}
              {/* Circular Timer */}
              <div className="absolute bottom-4 right-4">
                <svg width="50" height="50" className="text-black">
                  <circle
                    cx="25"
                    cy="25"
                    r={radius}
                    stroke="#e5e7eb"
                    strokeWidth="4"
                    fill="none"
                  />
                  <circle
                    cx="25"
                    cy="25"
                    r={radius}
                    stroke="#3b82f6"
                    strokeWidth="4"
                    fill="none"
                    strokeDasharray={circumference}
                    strokeDashoffset={strokeDashoffset}
                    strokeLinecap="round"
                    style={{ transition: "stroke-dashoffset 0.05s linear" }}
                  />
                  <text
                    x="50%"
                    y="50%"
                    textAnchor="middle"
                    dominantBaseline="central"
                    fontSize="12"
                    fill="currentColor"
                    fontWeight="bold"
                  >
                    {Math.ceil(remainingTime)}s
                  </text>
                </svg>
              </div>
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
              index === activeIndex ? "bg-white" : "bg-white/40"
            }`}
          />
        ))}
      </div>

      {/* Navigation Buttons */}
      <ImageButton
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
      />
    </div>
  );
};

export default BannerCarousel;
