import { useEffect, useState } from "react";

function ScrollToTopButton() {
  const [showButton, setShowButton] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setShowButton(window.scrollY > window.innerHeight);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    showButton && (
      <div
        className="fixed right-5 bottom-5 z-50 cursor-pointer bg-foreground  p-1 rounded-full shadow-lg hover:scale-105 transition-transform"
        onClick={scrollToTop}
      >
        <svg
          viewBox="-0.5 0 25 25"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-8 h-8"
        >
          <g id="SVGRepo_iconCarrier">
            <path
              d="M8 13.8599L10.87 10.8C11.0125 10.6416 11.1868 10.5149 11.3815 10.4282C11.5761 10.3415 11.7869 10.2966 12 10.2966C12.2131 10.2966 12.4239 10.3415 12.6185 10.4282C12.8132 10.5149 12.9875 10.6416 13.13 10.8L16 13.8599"
              className="stroke-background"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </g>
        </svg>
      </div>
    )
  );
}

export default ScrollToTopButton;

