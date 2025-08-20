import React, { useState, useEffect } from "react";
import ImageButton from "../../components/button/ImageBtn";
type Testimonial = {
  id: number;
  company: string;
  logo: string;
  feedback: string;
  client: string;
};

const sampleTestimonials: Testimonial[] = [
  {
    id: 1,
    company: "TechCorp",
    logo: "/logos/techcorp.png",
    feedback:
      "The software streamlined our operations and improved efficiency across departments. The software streamlined our operations and improved efficiency across departments. The software streamlined our operations and improved efficiency across departments.",
    client: "John Doe, CTO",
  },
  {
    id: 2,
    company: "HealthPlus",
    logo: "/logos/healthplus.png",
    feedback:
      "We reduced costs by 25% after implementing the ERP system. Highly recommended!",
    client: "Sarah Lee, Operations Head",
  },
  {
    id: 3,
    company: "EduSmart",
    logo: "/logos/edusmart.png",
    feedback:
      "Very user-friendly and adaptable to our unique needs in the education sector.",
    client: "Michael Tan, Director",
  },
  {
    id: 4,
    company: "BuildMax",
    logo: "/logos/buildmax.png",
    feedback:
      "The support team was fantastic, and the transition was smoother than expected.",
    client: "Priya Sharma, Project Manager",
  },
];

export default function TestimonialCarousel() {
  const [testimonials, setTestimonials] = useState<Testimonial[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [numVisible, setNumVisible] = useState(2);

  useEffect(() => {
    setTestimonials(sampleTestimonials);
  }, []);

  // Responsive layout
  useEffect(() => {
    const updateVisible = () => {
      if (window.innerWidth < 640) setNumVisible(1);
      else setNumVisible(2);
    };
    updateVisible();
    window.addEventListener("resize", updateVisible);
    return () => window.removeEventListener("resize", updateVisible);
  }, []);

  const nextSlide = () => {
    if (currentIndex < testimonials.length - numVisible) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const prevSlide = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-6 relative">
      <div className="overflow-hidden">
        <div
          className="flex transition-transform duration-500"
          style={{
            transform: `translateX(-${currentIndex * (100 / numVisible)}%)`,
          }}
        >
          {testimonials.map((t) => (
            <div
              key={t.id}
              className="p-4 flex-shrink-0"
              style={{ width: `${100 / numVisible}%` }}
            >
              <div className="bg-white rounded-xl border border-ring/30 shadow-lg p-6 h-full flex flex-col justify-between">
                {/* Logo + Company */}
                <div className="flex items-center gap-3 mb-4">
                  <img
                    src={t.logo}
                    alt={t.company}
                    className="w-12 h-12 object-contain"
                  />
                  <h4 className="font-semibold text-lg">{t.company}</h4>
                </div>

                {/* Feedback */}
                <p className="text-gray-600 italic mb-4">“{t.feedback}”</p>

                {/* Client */}
                <p className="text-sm font-medium text-gray-800">{t.client}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Controls */}
      <ImageButton
        icon="left"
        onClick={prevSlide}
        disabled={currentIndex === 0}
        className="absolute left-2 top-1/2 -translate-y-1/2 bg-gray-800 text-white p-2 rounded-full disabled:opacity-30"
      />
      <ImageButton
        icon="right"
        onClick={nextSlide}
        disabled={currentIndex >= testimonials.length - numVisible}
        className="absolute right-2 top-1/2 -translate-y-1/2 bg-gray-800 text-white p-2 rounded-full disabled:opacity-30"
      />
    </div>
  );
}
