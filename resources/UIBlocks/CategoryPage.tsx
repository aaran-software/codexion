import { useLocation, useNavigate, useParams } from "react-router-dom";
import React, { useState, useEffect, Suspense } from "react";
import apiClient from "../../resources/global/api/apiClients";
import ImageButton from "../components/button/ImageBtn";
import DropdownRead from "../components/input/dropdown-read";
import Checkbox from "../components/input/checkbox";
import { useAppContext } from "../../apps/global/AppContaxt";
import MobileFilter from "../UIBlocks/filter/MobileFilter";
import LoadingScreen from "../../resources/components/loading/LoadingScreen";
type ProductType = {
  id: number;
  name: string;
  image: string;
  category: string;
  description: string;
  count: number;
  price: number;
  prod_id: number;
};
export type FiltersType = {
  category: string;
  brand: string;
  rating: string;
  discount: string;
};

const CategoryPage: React.FC = () => {
  const { API_URL } = useAppContext();
  const [products, setProducts] = useState<ProductType[]>([]);
  const [cartStates, setCartStates] = useState<Record<number, string>>({});
  const [, setError] = useState<string | null>(null);
  const [invoice, setInvoice] = useState(false);
  const [availability, setAvailability] = useState(false);
  const { category } = useParams();
  const navigate = useNavigate();
  const [categories, setCategories] = useState<string[]>([]);
  const [brands, setBrands] = useState<string[]>([]);

  const location=useLocation()
  const [selectedFilters, setSelectedFilters] = useState<FiltersType>({
    category: category || "",
    brand: "",
    rating: "",
    discount: "",
  });
  const [listView, setListView] = useState<boolean>(true);
useEffect(()=>{
  setListView(location.state?.listView ?? true);
},[location.state?.listView]);
  // const [selectedPrice, setSelectedPrice] = useState<number | null>(0);

  const [maxPrice, setMaxPrice] = useState<number>(0);
  // New state for price range selection
  const [selectedPriceRange, setSelectedPriceRange] = useState<number | null>(
    null
  );

  const priceRanges = [
    {
      id: 1,
      label: `Up to ₹${Math.round(maxPrice * 0.25)}`,
      min: 0,
      max: maxPrice * 0.25,
    },
    {
      id: 2,
      label: `₹${Math.round(maxPrice * 0.25)} - ₹${Math.round(maxPrice * 0.5)}`,
      min: maxPrice * 0.25,
      max: maxPrice * 0.5,
    },
    {
      id: 3,
      label: `₹${Math.round(maxPrice * 0.5)} - ₹${Math.round(maxPrice * 0.75)}`,
      min: maxPrice * 0.5,
      max: maxPrice * 0.75,
    },
    {
      id: 4,
      label: `₹${Math.round(maxPrice * 0.75)} - ₹${Math.round(maxPrice * 0.9)}`,
      min: maxPrice * 0.75,
      max: maxPrice * 0.9,
    },
    {
      id: 5,
      label: `Above ₹${Math.round(maxPrice * 0.9)}`,
      min: maxPrice * 0.9,
      max: Infinity,
    },
  ];

  // New UI States for mobile modals
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [isSortOpen, setIsSortOpen] = useState(false);
  const [sortOption, setSortOption] = useState("");

  const dropdowns = [
    {
      id: "category",
      label: "Category",
      value: selectedFilters.category,
      options: categories,
    },
    { id: "brand", label: "Brand", options: brands },
    // {
    //   id: "rating",
    //   label: "rating",
    //   options: ["4★ & Above", "3★ & Above", "2★ & Above", "1★ & Above"],
    // },
    // {
    //   id: "discount",
    //   label: "Discount",
    //   options: ["60% Above", "40% & Above", "25% & Above", "10% & Above"],
    // },
  ];

  useEffect(() => {
    const applyFilters = async () => {
      try {
        const res = await apiClient.get(
          "/api/resource/Product?limit_page_length=0"
        );
        const items = res.data.data || [];

        const detailPromises = items.map((item: any) => {
          const itemName = encodeURIComponent(item.name);
          return apiClient
            .get(`/api/resource/Product/${itemName}`)
            .then((r) => r.data.data)
            .catch(() => null);
        });

        const detailResponses = await Promise.all(detailPromises);
        let formatted: ProductType[] = detailResponses
          .filter(Boolean)
          .map((item: any) => ({
            id: item.name,
            prod_id: item.product_code,
            name: item.display_name,
            description: item.description,
            image: `${API_URL}/${item.image}`,
            count: item.stock_qty,
            price: item.price || item.standard_rate || 0,
            category: item.category || "",
          }));

        // Filter by category and brand before price max calculation
        if (selectedFilters.category) {
          formatted = formatted.filter((item) =>
            item.category
              .toLowerCase()
              .includes(selectedFilters.category.toLowerCase())
          );
        }

        if (selectedFilters.brand) {
          formatted = formatted.filter((item) =>
            item.name
              .toLowerCase()
              .includes(selectedFilters.brand.toLowerCase())
          );
        }

        // Calculate the max price of filtered products
        if (formatted.length > 0) {
          const highestPrice = Math.max(...formatted.map((p) => p.price));
          setMaxPrice(highestPrice);

          // Reset selectedPrice if it exceeds the new max price or not set
          // if (!selectedPrice || selectedPrice > highestPrice) {
          //   setSelectedPrice(highestPrice);
          // }
        } else {
          // If no products match, reset maxPrice to a default or zero
          setMaxPrice(0);
          // setSelectedPrice(0);
        }

        // sort products based on selected sort option
        if (sortOption) {
          formatted = [...formatted].sort((a, b) => {
            if (sortOption === "priceLowHigh") return a.price - b.price;
            if (sortOption === "priceHighLow") return b.price - a.price;
            if (sortOption === "nameAZ") return a.name.localeCompare(b.name);
            if (sortOption === "nameZA") return b.name.localeCompare(a.name);
            return 0;
          });
        }
        // Now filter by selectedPrice if it has a value
        if (selectedPriceRange !== null) {
          const range = priceRanges.find((r) => r.id === selectedPriceRange);
          if (range) {
            formatted = formatted.filter(
              (item) => item.price >= range.min && item.price <= range.max
            );
          }
        }

        setProducts(formatted);
      } catch (err) {
        setError("Failed to fetch products");
      }
    };

    applyFilters();
    // Apply sorting after filters
  }, [
    selectedFilters.category,
    selectedFilters.brand,
    selectedPriceRange,
    sortOption,
    API_URL,
  ]);

  // useEffect(() => {
  //   if (products.length > 0 && selectedPrice === null) {
  //     const maxPriceInProducts = Math.max(...products.map((p) => p.price));
  //     setSelectedPrice(maxPriceInProducts);
  //   }
  // }, [products, selectedPrice]);

  const navigateProductPage = (id: number) => {
    navigate(`/productpage/${id}`);
  };

  const changeCart = (id: number) => {
    setCartStates((prev) => ({
      ...prev,
      [id]: prev[id] === "Add to Cart" ? "Added to Cart" : "Add to Cart",
    }));
  };

  useEffect(() => {
    const fetchDropdownData = async () => {
      try {
        const categoryRes = await apiClient.get("/api/resource/Category");
        const brandRes = await apiClient.get("/api/resource/Brand");

        setCategories(categoryRes.data.data.map((item: any) => item.name));
        setBrands(brandRes.data.data.map((item: any) => item.name));
      } catch (err) {
        console.error("Dropdown fetch error:", err);
      }
    };

    fetchDropdownData();
  }, []);

  // if (products.length === 0) {
  //   return <LoadingScreen image={"/assets/svg/logo.svg"} />;
  // }

  const sortOptions = [
    { value: "priceLowHigh", label: "Price: Low to High" },
    { value: "priceHighLow", label: "Price: High to Low" },
    { value: "nameAZ", label: "Name: A to Z" },
    { value: "nameZA", label: "Name: Z to A" },
  ];


  return (
    <Suspense fallback={<LoadingScreen image={"/assets/svg/logo.svg"} />}>
      <div className="md:mt-5 px-[5%] py-5">
        <div className="flex flex-col md:flex-row gap-3">
          {/* Filters */}
          {/* Mobile Top Bar with Sort & Filter buttons */}
          <div className="md:hidden flex justify-between items-center mb-4 sticky top-0 bg-white z-20">
            <ImageButton
              className="flex-1 border flex justify-center rounded border-ring/30 py-2 mx-1 shadow-sm"
              onClick={() => setIsSortOpen(true)}
              icon={"desc"}
            >
              Sort
            </ImageButton>
            <ImageButton
              className="flex-1 border flex justify-center rounded border-ring/30 py-2 mx-1 shadow-sm"
              onClick={() => setIsFilterOpen(true)}
              icon={"filter"}
            >
              Filter
            </ImageButton>
          </div>

          <div className="hidden md:flex flex-row md:flex-col w-full border border-ring/30 rounded-md md:w-72 overflow-x-auto md:overflow-visible gap-4 scrollbar-hide">
            <div className="flex flex-row md:flex-col flex-nowrap md:sticky md:top-24 bg-background  rounded-md  p-4 md:p-6 gap-4 min-w-max md:min-w-0">
              <h6 className="font-semibold text-lg hidden md:block">Filters</h6>

              <div className="flex flex-row md:flex-col gap-4 md:gap-3">
                {dropdowns.map((dropdown) => (
                  <div key={dropdown.id} className="relative">
                    <DropdownRead
                      id={dropdown.id}
                      items={dropdown.options}
                      label={dropdown.label}
                      value={
                        selectedFilters[
                          dropdown.id as keyof typeof selectedFilters
                        ]
                      }
                      err=""
                      placeholder=""
                      onChange={(val) =>
                        setSelectedFilters((prev) => ({
                          ...prev,
                          [dropdown.id]: val,
                        }))
                      }
                    />
                    {selectedFilters[
                      dropdown.id as keyof typeof selectedFilters
                    ] && (
                      <button
                        type="button"
                        onClick={() =>
                          setSelectedFilters((prev) => ({
                            ...prev,
                            [dropdown.id]: "",
                          }))
                        }
                        className="block ml-auto text-sm mt-1 text-primary cursor-pointer"
                      >
                        Clear
                      </button>
                    )}
                  </div>
                ))}
              </div>

              <div className="flex flex-col gap-2 min-w-[180px]">
                <label className="text-md font-semibold hidden md:block">
                  Price
                </label>
                {priceRanges.map((range) => (
                  <Checkbox
                    key={range.id}
                    id={`price-${range.id}`}
                    agreed={selectedPriceRange === range.id}
                    label={range.label}
                    err={""} // or your error message if you have validation
                    className=""
                    onChange={(checked) =>
                      setSelectedPriceRange((prev) =>
                        checked ? range.id : null
                      )
                    }
                  />
                ))}
              </div>

              {/* <div className="flex flex-col gap-2 min-w-[180px]">
                <label className="text-md font-semibold hidden md:block">
                  Invoice
                </label>
                <Checkbox
                  id="invoice"
                  agreed={invoice}
                  label="GST Invoice"
                  err=""
                  className=""
                  onChange={() => setInvoice(!invoice)}
                />
              </div>

              <div className="flex flex-col gap-2 min-w-[180px]">
                <label className="text-md font-semibold hidden md:block">
                  Availability
                </label>
                <Checkbox
                  id="stock"
                  agreed={availability}
                  label="Include Out of Stock"
                  err=""
                  className=""
                  onChange={() => setAvailability(!availability)}
                />
              </div> */}
            </div>
          </div>

          {/* Mobile Filter Full Screen */}
          {isFilterOpen && (
            <div className="fixed inset-0 bg-white z-50 overflow-y-auto">
              <div className="flex justify-between items-center p-4 border-b">
                <h2 className="text-lg font-semibold">Filters</h2>
                <ImageButton
                  onClick={() => setIsFilterOpen(false)}
                  icon={"close"}
                />
              </div>
              <MobileFilter
                dropdowns={dropdowns}
                selectedFilters={selectedFilters}
                setSelectedFilters={setSelectedFilters}
                selectedPriceRange={selectedPriceRange}
                setSelectedPriceRange={setSelectedPriceRange}
                maxPrice={maxPrice}
                invoice={invoice}
                setInvoice={setInvoice}
                availability={availability}
                setAvailability={setAvailability}
                onClose={() => setIsFilterOpen(false)}
              />
            </div>
          )}

          {/* Mobile Sort Full Screen */}
          {isSortOpen && (
            <div className="fixed inset-0 bg-white z-50">
              <div className="flex justify-between items-center p-4 border-b">
                <h2 className="text-lg font-semibold">Sort By</h2>
                <ImageButton
                  onClick={() => setIsSortOpen(false)}
                  icon={"close"}
                />
              </div>
              <div className="p-4 space-y-3">
                {[
                  { value: "priceLowHigh", label: "Price: Low to High" },
                  { value: "priceHighLow", label: "Price: High to Low" },
                  { value: "nameAZ", label: "Name: A to Z" },
                  { value: "nameZA", label: "Name: Z to A" },
                ].map((opt) => (
                  <button
                    key={opt.value}
                    className={`w-full text-left px-3 py-2 border border-ring/30 rounded ${
                      sortOption === opt.value ? "bg-blue-100" : ""
                    }`}
                    onClick={() => {
                      setSortOption(opt.value);
                      setIsSortOpen(false);
                    }}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Product List */}
          <div className="w-full md:w-3/4 space-y-3">
            <div className="hidden md:flex justify-between items-center mb-4">
              <div className="w-max">
                <DropdownRead
                  id="sortBy"
                  label="Sort By"
                  err=""
                  items={sortOptions.map((opt) => opt.label)}
                  value={
                    sortOptions.find((opt) => opt.value === sortOption)
                      ?.label || ""
                  }
                  onChange={(val) => {
                    const selected = sortOptions.find(
                      (opt) => opt.label === val
                    );
                    if (selected) {
                      setSortOption(selected.value); // store internal value
                    }
                  }}
                  className="w-max"
                />
              </div>
              <div className="flex justify-end gap-5 mb-4">
                <ImageButton
                  icon={"list"}
                  onClick={() => {
                    setListView(true);
                  }}
                />
                <ImageButton
                  icon={"grid"}
                  onClick={() => {
                    setListView(false);
                  }}
                />
              </div>
            </div>

            {listView ? (
              // List View (current layout)
              products.map((product) => (
                <div key={product.id} className="border border-ring/30 rounded">
                  <div className="grid grid-cols-[45%_55%] md:grid-cols-[25%_45%_25%] mx-5 gap-4 p-4">
                    {/* Image */}
                    <div
                      onClick={() => navigateProductPage(product.id)}
                      className="w-full h-full aspect-square overflow-hidden rounded-md cursor-pointer"
                    >
                      <img
                        className="w-full h-full object-scale-down rounded-md"
                        src={product.image}
                        alt={product.name}
                      />
                    </div>

                    {/* Details */}
                    <div
                      className="space-y-2 px-2 cursor-pointer"
                      onClick={() => navigateProductPage(product.id)}
                    >
                      <h4 className="text-sm lg:text-lg font-semibold line-clamp-3">
                        {product.name}
                      </h4>
                      <h2 className="text-xl font-bold block md:hidden">
                        ₹{product.price}
                      </h2>
                      <p className="text-sm text-foreground/60 line-clamp-2 lg:line-clamp-3">
                        {product.description}
                      </p>
                      <div className="flex gap-2">
                        <p className="text-sm text-green-600">10% Offer</p>
                      </div>

                      {/* Action buttons */}
                      <div className="my-2 flex flex-row gap-2">
                        <ImageButton
                          onClick={(e) => {
                            e.stopPropagation();
                            changeCart(product.id);
                          }}
                          icon="cart"
                          className={`p-2 rounded-full shadow ${
                            cartStates[product.id] === "Added to Cart"
                              ? "bg-green-600 text-white"
                              : "bg-background text-foreground hover:bg-gray-200"
                          }`}
                        />
                        <ImageButton
                          onClick={(e) => e.stopPropagation()}
                          className="bg-background text-foreground p-2 rounded-full shadow hover:bg-gray-200"
                          icon={"like"}
                        />
                        <ImageButton
                          onClick={(e) => e.stopPropagation()}
                          className="bg-background text-foreground p-2 rounded-full shadow hover:bg-gray-200"
                          icon={"link"}
                        />
                      </div>
                    </div>

                    {/* Price section */}
                    <div className="text-right space-y-2 hidden md:block">
                      <h2 className="text-sm md:text-xl font-bold">
                        ₹{product.price}
                      </h2>
                      <p className="text-sm text-foreground/60">
                        Delivery: 3–5 days
                      </p>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              // Grid View (3 items per row)
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                {products.map((product) => (
                  <div
                    key={product.id}
                    className="border border-ring/30 rounded p-4 cursor-pointer hover:shadow-md transition relative group"
                    onClick={() => navigateProductPage(product.id)}
                  >
                    {/* Image on top */}
                    <div className="w-[60%] block mx-auto sm:w-full aspect-square overflow-hidden rounded-md mb-3">
                      <img
                        className="w-full h-full object-scale-down"
                        src={product.image}
                        alt={product.name}
                      />
                    </div>

                    {/* Title */}
                    <h4 className="text-sm lg:text-lg font-semibold line-clamp-2 mb-1 text-center">
                      {product.name}
                    </h4>

                    {/* Price */}
                    <h2 className="text-lg font-bold mb-2 text-center">₹{product.price}</h2>

                    {/* Actions */}
                    <div className="flex gap-2 flex-col absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-500 z-10">
                      <ImageButton
                        onClick={(e) => {
                          e.stopPropagation();
                          changeCart(product.id);
                        }}
                        icon="cart"
                        className={`p-2 rounded-full shadow ${
                          cartStates[product.id] === "Added to Cart"
                            ? "bg-green-600 text-white"
                            : "bg-background text-foreground hover:bg-gray-200"
                        }`}
                      />
                      <ImageButton
                        onClick={(e) => e.stopPropagation()}
                        className="bg-background text-foreground p-2 rounded-full shadow hover:bg-gray-200"
                        icon={"like"}
                      />
                      <ImageButton
                        onClick={(e) => e.stopPropagation()}
                        className="bg-background text-foreground p-2 rounded-full shadow hover:bg-gray-200"
                        icon={"link"}
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </Suspense>
  );
};

export default CategoryPage;
