// Filter.tsx
import React from "react";
import { TextInput } from "../SecondaryInput/TextInput";

interface FilterProps {
  head: string[];
  filters: Record<string, string>;
  onFilterChange: (key: string, value: string) => void;
}

const Filter: React.FC<FilterProps> = ({ head, filters, onFilterChange }) => {
  const filterableColumns = head.filter((column) => column.toLowerCase() !== "action");

  return (
    <div className="flex flex-col md:flex-row gap-4 mb-4">
      {filterableColumns.map((column, i) => {
        const key = column.toLowerCase();
        return (
          <div key={i} className="flex  text-sm w-full md:w-1/2">
            <TextInput
              type="text"
              placeholder={`Filter ${column}`}
              value={filters[key] || ""}
              onChange={(e) => onFilterChange(key, e.target.value)}
              className="p-2 border border-ring rounded-md text-sm bg-background text-foreground"
              id=""
              label=""
              err=""
            />
          </div>
        );
      })}
    </div>
  );
};

export default Filter;
