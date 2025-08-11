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
        className="fixed right-5 bottom-11 z-50 cursor-pointer bg-foreground rounded-full shadow-lg hover:scale-105 transition-transform"
        onClick={scrollToTop}
      >
        <img src="/assets/svg/scroll.svg" className="w-12 h-12" alt="" />
      </div>
    )
  );
}

export default ScrollToTopButton;

