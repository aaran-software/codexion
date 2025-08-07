import React, { useRef, useState } from "react";

interface ZoomImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  src: string;
}

const ZoomImage: React.FC<ZoomImageProps> = ({ src, alt, className = "" }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [zoomStyles, setZoomStyles] = useState({
    visible: false,
    backgroundPosition: "0% 0%",
    top: 0,
    left: 0,
  });

  const handleMouseMove = (e: React.MouseEvent) => {
    const { top, left, width, height } =
      containerRef.current?.getBoundingClientRect() ?? {
        top: 0,
        left: 0,
        width: 0,
        height: 0,
      };

    const x = ((e.clientX - left) / width) * 100;
    const y = ((e.clientY - top) / height) * 100;

    // Show zoom image where cursor is centered
    setZoomStyles({
      visible: true,
      backgroundPosition: `${x}% ${y}%`,
      top: e.clientY - 150, // Adjust offset to center
      left: e.clientX + 20,
    });
  };

  const handleMouseLeave = () => {
    setZoomStyles((prev) => ({ ...prev, visible: false }));
  };

  return (
    <>
      <div
        ref={containerRef}
        className="relative w-full h-full"
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
      >
        <img
          src={src}
          alt={alt}
          className={`w-full h-full object-contain rounded transition duration-300 ease-in-out ${className}`}
          loading="lazy"
        />
      </div>

      {/* Zoom Preview */}
      {zoomStyles.visible && (
        <div
          className="fixed w-[500px] h-[500px] border-2 border-gray-300 shadow-lg rounded-lg bg-no-repeat bg-contain z-50 pointer-events-none"
          style={{
            top: zoomStyles.top,
            left: zoomStyles.left,
            backgroundImage: `url(${src})`,
            backgroundPosition: zoomStyles.backgroundPosition,
            backgroundSize: "150%",
          }}
        />
      )}
    </>
  );
};

export default ZoomImage;
