import { useEffect, useState } from "react";

interface CounterProps {
  target: number;      // Final value to reach
  duration?: number;   // Duration in ms (default 2000)
  className?: string;  // Optional styling
}

const Counter: React.FC<CounterProps> = ({ target, duration = 2000, className }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
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
  }, [target, duration]);

  return <span className={className}>{count}</span>;
};

export default Counter;
