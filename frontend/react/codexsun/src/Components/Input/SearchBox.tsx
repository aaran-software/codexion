import { useState } from "react";
import { cn } from "../../library/utils.ts";

interface GlobalSearchProps {
  className?: string;
}

export default function GlobalSearch({ className = "" }: GlobalSearchProps) {
  const [query, setQuery] = useState("");

  return (
    <div className="relative w-full">
      <div className="relative">
        {/* Search Icon */}
        <div className="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none z-10">
          <svg
            className="size-4 text-gray-400 dark:text-white/60"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth={2}
          >
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.3-4.3" />
          </svg>
        </div>

        {/* Input only */}
        <input
          type="text"
          placeholder="Search..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className={cn(
            "py-2.5 ps-10 pe-4 block w-full rounded-lg border border-ring/30 sm:text-sm",
            "focus:ring-2 focus:ring-ring/30 focus:outline-none focus:border-transparent",
            "transition duration-300",
            className
          )}
        />
      </div>
    </div>
  );
}
