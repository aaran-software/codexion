import ImageButton from "../../../resources/components/button/ImageBtn";
import { FiltersType } from "../CategoryPage";

type DropdownType = {
  id: string;
  label: string;
  options: string[];
};

type FilterProps = {
  dropdowns: DropdownType[];
   selectedFilters: FiltersType;
  setSelectedFilters: React.Dispatch<React.SetStateAction<FiltersType>>;
  selectedPrice: number | null;
  setSelectedPrice: React.Dispatch<React.SetStateAction<number | null>>;
  maxPrice: number;
  invoice: boolean;
  setInvoice: React.Dispatch<React.SetStateAction<boolean>>;
  availability: boolean;
  setAvailability: React.Dispatch<React.SetStateAction<boolean>>;
  onClose: () => void;
};


const MobileFilter = ({
  dropdowns,
  selectedFilters,
  setSelectedFilters,
  selectedPrice,
  setSelectedPrice,
  maxPrice,
  invoice,
  setInvoice,
  availability,
  setAvailability,
  onClose // new prop to close the modal
}:FilterProps) => {
  return (
    <div className="md:hidden fixed inset-0 bg-white z-50 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        <h6 className="font-semibold text-lg">Filters</h6>
        <ImageButton
          className="text-xl font-bold"
          onClick={onClose} icon={"close"} />
      </div>

      {/* Content area - scrollable */}
      <div className="flex-1 overflow-y-auto p-4">
        {/* Dropdowns */}
        <div className="flex flex-col gap-4">
          {dropdowns.map((dropdown) => (
            <div key={dropdown.id} className="w-full">
              <label className="block text-sm font-medium mb-1">
                {dropdown.label}
              </label>
              <select
                value={selectedFilters[dropdown.id as keyof FiltersType]}
                onChange={(e) =>
                  setSelectedFilters((prev) => ({
                    ...prev,
                    [dropdown.id]: e.target.value,
                  }))
                }
                className="border border-ring/30 rounded p-2 w-full"
              >
                <option value="">All {dropdown.label}</option>
                {dropdown.options.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
              {selectedFilters[dropdown.id as keyof FiltersType] && (
                <button
                  className="text-xs text-blue-600 underline mt-1"
                  onClick={() =>
                    setSelectedFilters((prev) => ({
                      ...prev,
                      [dropdown.id]: "",
                    }))
                  }
                >
                  Clear
                </button>
              )}
            </div>
          ))}
        </div>

        {/* Price filter */}
        <div className="mt-6">
          <label className="text-md font-semibold">Price</label>
          <input
            type="range"
            min={0}
            max={maxPrice}
            value={selectedPrice ?? maxPrice}
            onChange={(e) => setSelectedPrice(Number(e.target.value))}
            className="w-full mt-2"
          />
          <div className="text-sm">Up to ₹{selectedPrice}</div>
        </div>

        {/* Other filters */}
        <div className="flex flex-col gap-3 mt-6">
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={invoice}
              onChange={() => setInvoice(!invoice)}
            />
            GST Invoice
          </label>
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={availability}
              onChange={() => setAvailability(!availability)}
            />
            Include Out of Stock
          </label>
        </div>
      </div>

      {/* Footer with Apply button */}
      <div className="p-4 border-t">
        <button
          className="w-full bg-orange-500 text-white p-2 rounded"
          onClick={onClose}
        >
          Apply
        </button>
      </div>
    </div>
  );
};

export default MobileFilter;
