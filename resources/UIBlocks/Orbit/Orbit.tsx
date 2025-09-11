import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";

type TechItem = {
  title: string;
  description: string;
};

interface OrbitProps {
  centerImage: string;
  items: TechItem[];
  radius?: number;
  size?: number;
  autoRotateSpeed?: number;
  // title?: string;
}

const Orbit: React.FC<OrbitProps> = ({
  centerImage,
  items,
  radius = 220,
  size = 500,
  autoRotateSpeed = 0.05,
  // title,
}) => {
  const [autoRotation, setAutoRotation] = useState(0);
  const [responsiveRadius, setResponsiveRadius] = useState(radius);
  const [responsiveSize, setResponsiveSize] = useState(size);

  // ✅ Responsive radius and size
  useEffect(() => {
    const updateRadius = () => {
      if (window.innerWidth < 640) {
        // Mobile
        setResponsiveRadius(radius * 0.4);
        setResponsiveSize(size * 0.6);
      } else if (window.innerWidth < 1024) {
        // Tablet
        setResponsiveRadius(radius * 0.8);
        setResponsiveSize(size * 0.75);
      } else {
        // Desktop
        setResponsiveRadius(radius);
        setResponsiveSize(size);
      }
    };
    updateRadius();
    window.addEventListener("resize", updateRadius);
    return () => window.removeEventListener("resize", updateRadius);
  }, [radius, size]);

  // ✅ Auto-rotate
  useEffect(() => {
    let frame: number;
    const animate = () => {
      setAutoRotation((prev) => prev + autoRotateSpeed);
      frame = requestAnimationFrame(animate);
    };
    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, [autoRotateSpeed]);

  return (
    <div className="relative flex flex-col items-center justify-center py-20 sm:py-40">
      {/* Center image */}
      <div className="relative z-10 flex flex-col items-center">
        <img
          src={centerImage}
          alt="center"
          className="w-20 h-20 sm:w-48 sm:h-48 object-contain"
        />
        {/* <h1 className="text-xl sm:text-3xl font-bold text-center mt-4">{title}</h1> */}
      </div>

      {/* Orbit container */}
      <motion.div
        className="absolute top-1/2 left-1/2"
        style={{
          width: responsiveSize,
          height: responsiveSize,
          x: "-50%",
          y: "-50%",
          rotate: autoRotation,
        }}
      >
        {items.map((item, index) => {
          const angle = (index / items.length) * 2 * Math.PI;
          const x = Math.cos(angle) * responsiveRadius;
          const y = Math.sin(angle) * responsiveRadius;

          return (
            <div
              key={index}
              className="absolute flex flex-col items-center text-center"
              style={{
                left: `calc(50% + ${x}px)`,
                top: `calc(50% - ${y}px)`,
                transform: "translate(-50%, -50%)",
              }}
            >
              <motion.div
                className="p-2"
                style={{ rotate: -autoRotation }}
                whileHover={{ scale: 1.05 }}
                transition={{ type: "spring", stiffness: 200 }}
              >
                <h3 className="text-[8px] md:text-sm text-center block mx-auto font-semibold text-foreground max-w-[100px] sm:max-w-[200px] min-w-[100px] sm:min-w-[200px]">
                  {item.title}
                </h3>
                <p className="text-[6px] md:text-[10px] block mx-auto text-muted-foreground whitespace-normal break-words leading-snug max-w-[100px] sm:max-w-[240px] min-w-[100px] sm:min-w-[240px] mt-1">
                  {item.description}
                </p>
              </motion.div>
            </div>
          );
        })}
      </motion.div>
    </div>
  );
};

export default Orbit;
