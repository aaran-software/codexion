import ImageButton from "../../components/button/ImageBtn";
import React, { useState, useEffect, useRef } from "react";
import apiClient from "../../../resources/global/api/apiClients";
import { useAppContext } from "../../../apps/global/AppContaxt";

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
    <div className="relative w-full h-[250px] md:h-[400px] bg-background overflow-hidden">
      {/* 🔹 Slides */}
      <div
        className="w-full h-full relative"
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {slides.map((slide, index) => (
          <div
            key={index}
            className={`absolute inset-0 w-full h-[250px] md:h-[400px] flex transition-opacity duration-300 ${
              index === activeIndex ? "opacity-100 z-10" : "opacity-0 z-0"
            }`}
          >
            {/* Left: Image */}
            <div className="w-full h-[250px] md:h-[400px] flex items-center justify-center">
              <img
                // src={`${API_URL}/${slide.image}`}
                src={"/assets/Promotion/banner4.jpg"}
                alt={`Slide ${index} ${slide}`}
                className={`h-full w-full object-fill`}
              />
            </div>
            
          </div>
        ))}
      </div>

     
    </div>
  );
};

export default BannerCarousel;
