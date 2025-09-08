import { useEffect, useState } from "react";
import { Play, X } from "lucide-react";

interface BannerImage {
  id: string;
  image: string;
}

interface HomeBannerProps {
  images: BannerImage[];
  interval?: number;
  title: string;
  description: string;
  videoPath: string; // YouTube embed link or mp4
}

const HeroBanner2: React.FC<HomeBannerProps> = ({
  images,
  interval = 5000,
  title,
  description,
  videoPath,
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showVideo, setShowVideo] = useState(false);

  useEffect(() => {
    if (images.length <= 1) return;
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % images.length);
    }, interval);
    return () => clearInterval(timer);
  }, [images.length, interval]);

  return (
    <div className="relative w-full h-[90vh] overflow-hidden">
      {/* Background Images (crossfade + zoom per slide) */}
      {images.map((img, i) => (
        <img
          key={img.id}
          src={img.image}
          alt={img.id}
          className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-1000 ease-in-out 
            ${i === currentIndex ? "opacity-100 animate-zoom" : "opacity-0"}`}
        />
      ))}

      {/* ✅ Permanent 40% Black Overlay */}
      <div className="absolute inset-0 bg-black/70" />

      {/* Content Layer */}
      <div className="absolute inset-0 flex items-center px-8 md:px-20">
        <div className="max-w-xl text-white space-y-4">
          <p className="text-lg font-medium">Since 2005</p>
          <h1 className="text-4xl md:text-6xl font-bold leading-tight">
            {title}
          </h1>
          <p className="text-base md:text-lg text-gray-200">{description}</p>

          <button
            onClick={() => setShowVideo(true)}
            className="mt-6 flex items-center gap-3 bg-white/10 hover:bg-white/20 text-white px-5 py-3 rounded-full backdrop-blur-md transition cursor-pointer"
          >
            <span className="flex items-center justify-center w-10 h-10 bg-green-500 rounded-full">
              <Play className="w-5 h-5" />
            </span>
            <span className="font-semibold">Watch Video</span>
          </button>
        </div>
      </div>

      {/* Video Modal */}
      {showVideo && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
          <div className="relative w-full max-w-4xl mx-4">
            {/* Close Button */}
            <button
              onClick={() => setShowVideo(false)}
              className="absolute -top-12 right-0 text-white hover:text-gray-300"
            >
              <X className="w-8 h-8" />
            </button>

            {/* Video Player */}
            <div className="aspect-video w-full bg-black rounded-lg overflow-hidden shadow-lg">
              <iframe
                src={videoPath}
                title="Video Player"
                allow="autoplay; fullscreen"
                className="w-full h-full"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HeroBanner2;
