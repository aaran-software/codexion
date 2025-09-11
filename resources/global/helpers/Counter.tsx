import { useEffect, useRef, useState } from "react";

interface CounterProps {
  target: number;      // Final value to reach
  duration?: number;   // Duration in ms (default 2000)
  className?: string;  // Optional styling
}

const Counter: React.FC<CounterProps> = ({ target, duration = 2000, className }) => {
  const [count, setCount] = useState(0);
  const [hasStarted, setHasStarted] = useState(false);
  const ref = useRef<HTMLSpanElement | null>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasStarted) {
            setHasStarted(true);
          }
        });
      },
      { threshold: 0.3 } // starts when 30% of element is visible
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) observer.unobserve(ref.current);
    };
  }, [hasStarted]);

  useEffect(() => {
    if (!hasStarted) return;

    let start = 0;
    const increment = target / (duration / 30); // update every ~30ms

    const timer = setInterval(() => {
      start += increment;
      if (start >= target) {
        setCount(target);
        clearInterval(timer);
      } else {
        setCount(Math.floor(start));
      }
    }, 30);

    return () => clearInterval(timer);
  }, [target, duration, hasStarted]);

  return <span ref={ref} className={className}>{count}</span>;
};

export default Counter;
