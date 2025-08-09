import { useState, useRef, useEffect } from "react";
import { cn } from "../../../resources/global/library/utils";
import type { Product } from "../header/Header";
import apiClient from "../../../resources/global/api/apiClients";
import { useAppContext } from "../../../apps/global/AppContaxt";

interface GlobalSearchProps {
  className?: string;
  onSearchApi: string;
  onNavigate: (path: string) => void;
}

export default function GlobalSearch({
  className = "",
  onSearchApi,
  onNavigate,
}: GlobalSearchProps) {
  const { API_URL } = useAppContext();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Product[]>([]);
  const [recentSearches, setRecentSearches] = useState<Product[]>([]);
  const [showResults, setShowResults] = useState(false);
  const debounceTimeout = useRef<NodeJS.Timeout | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  // Load recent searches from localStorage
  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem("recentSearches") || "[]");
    setRecentSearches(stored);
  }, []);

  // Close results when clicking outside
  // Close results when clicking outside or scrolling
  useEffect(() => {
   
    const closeSearch = (e: Event) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setShowResults(false);
        inputRef.current?.blur(); // remove focus from search input
      }
    };

    document.addEventListener("mousedown", closeSearch);
    document.addEventListener("scroll", closeSearch, true); // use capture to detect in bubbling parents

    return () => {
      document.removeEventListener("mousedown", closeSearch);
      document.removeEventListener("scroll", closeSearch, true);
    };
  }, []);

  const handleSearch = (value: string) => {
    setQuery(value);
    setShowResults(true);
    if (debounceTimeout.current) clearTimeout(debounceTimeout.current);

    debounceTimeout.current = setTimeout(async () => {
      if (!value.trim()) {
        setResults([]);
        return;
      }

      try {
        const searchFilter = ["name", "like", `%${value}%`];
        const filtersParam = `filters=${encodeURIComponent(
          JSON.stringify([searchFilter])
        )}`;

        const url = `${onSearchApi}${
          onSearchApi.includes("?") ? "&" : "?"
        }${filtersParam}`;

        const res = await apiClient.get(url);

        setResults(
          (res.data?.data || []).map((item: any) => ({
            id: item.name,
            name: item.name,
            imageUrl: item.image,
            price: item.price || item.standard_rate || 0,
          }))
        );
      } catch (err) {
        console.error("Search error:", err);
        setResults([]);
      }
    }, 300);
  };

  const handleSelect = (product: Product) => {
    // Save to recent searches (avoid duplicates by id)
    let updated = [
      product,
      ...recentSearches.filter((p) => p.id !== product.id),
    ].slice(0, 5);

    setRecentSearches(updated);
    localStorage.setItem("recentSearches", JSON.stringify(updated));

    onNavigate(`/productpage/${product.id}`);
    setQuery("");
    setShowResults(false);
  };

  return (
    <div className="relative w-full" ref={containerRef}>
      {/* Search Bar */}
      <div className="relative">
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

        <input
          ref={inputRef}
          type="text"
          placeholder="Search..."
          value={query}
          onFocus={() => setShowResults(true)}
          onChange={(e) => handleSearch(e.target.value)}
          className={cn(
            "py-2.5 ps-10 pe-4 block w-full rounded-lg border border-ring/30 sm:text-sm",
            "focus:ring-2 focus:ring-ring/30 focus:outline-none focus:border-transparent",
            "transition duration-300",
            className
          )}
        />
      </div>

      {/* Dropdown */}
      {showResults && (
        <div className="absolute bg-white border border-ring/30 rounded w-full mt-1 max-h-[450px] overflow-y-auto shadow-lg z-50">
          {/* Recent Searches */}
          {!query.trim() && recentSearches.length > 0 && (
            <div>
              <div className="px-2 py-1 text-xs text-gray-500">
                Recent Searches
              </div>
              {recentSearches.map((product, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-2 p-2 hover:bg-gray-100 cursor-pointer border-b border-ring/30 last:border-0"
                  onClick={() => handleSelect(product)}
                >
                  {product.imageUrl && (
                    <img
                      src={`${API_URL}/${product.imageUrl}`}
                      alt={product.name}
                      className="w-12 lg:w-18 h-12 lg:h-18 object-cover rounded"
                    />
                  )}
                  <span className="text-foreground/50">{product.name}</span>
                 
                </div>
              ))}
            </div>
          )}

          {/* Search Results */}
          {query.trim() && results.length > 0 && (
            <div>
              {results.map((product) => (
                <div
                  key={product.id}
                  className="flex items-center gap-2 p-2 hover:bg-gray-100 cursor-pointer border-b border-ring/30 last:border-0"
                  onClick={() => handleSelect(product)}
                >
                  {product.imageUrl && (
                    <img
                      src={`${API_URL}/${product.imageUrl}`}
                      alt={product.name}
                      className="w-12 lg:w-18 h-12 lg:h-18 object-cover rounded"
                    />
                  )}
                  <span className="text-foreground/70">{product.name}</span>
                  {product.price !== undefined && (
                    <span className="ml-auto font-medium">
                      ₹{product.price}
                    </span>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* No results */}
          {query.trim() && results.length === 0 && (
            <div className="p-2 text-sm text-gray-500">
              No matching products found.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
