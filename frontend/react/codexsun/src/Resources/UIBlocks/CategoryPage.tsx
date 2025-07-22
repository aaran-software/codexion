import { useNavigate, useParams } from "react-router-dom";
import React, { useState, useEffect } from "react";
import apiClient from "../../pages/app/ecart/api/apiClients";
import ImageButton from "../../Components/Button/ImageBtn";
import RangeSlider from "../../Components/Input/RangeSlider";
import DropdownRead from "../../Components/Input/Dropdown-read";
import Checkbox from "../../Components/Input/checkbox";

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

const CategoryPage: React.FC = () => {
  const [products, setProducts] = useState<ProductType[]>([]);
  const [cartStates, setCartStates] = useState<Record<number, string>>({});
  const [, setError] = useState<string | null>(null);
  const [invoice, setInvoice] = useState(false);
  const [availability, setAvailability] = useState(false);
  const { category } = useParams();
  const navigate = useNavigate();
  const [categories, setCategories] = useState<string[]>([]);
  const [brands, setBrands] = useState<string[]>([]);
  const [selectedFilters, setSelectedFilters] = useState({
    category: category || "",
    brand: "",
    rating: "",
    discount: "",
  });

  const dropdowns = [
    {
      id: "category",
      label: "Category",
      value: selectedFilters.category,
      options: categories,
    },
    { id: "brand", label: "Brand", options: brands },
    {
      id: "rating",
      label: "Rating",
      options: ["4★ & Above", "3★ & Above", "2★ & Above", "1★ & Above"],
    },
    {
      id: "discount",
      label: "Discount",
      options: ["60% Above", "40% & Above", "25% & Above", "10% & Above"],
    },
  ];

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await apiClient.get("/api/resource/Product");
        const items = res.data.data || [];

        const detailPromises = items.map((item: any) => {
          const itemName = encodeURIComponent(item.name);
          return apiClient
            .get(`/api/resource/Product/${itemName}`)
            .then((r) => r.data.data)
            .catch(() => null);
        });

        const detailResponses = await Promise.all(detailPromises);
        const validItems = detailResponses.filter(Boolean);

        let formatted: ProductType[] = validItems.map((item: any) => ({
          id: item.name,
          prod_id: item.product_code,
          name: item.display_name,
          description: item.short_describe,
          image: `https://dev.aaranerp.com/${item.image}`,
          count: item.stock_qty,
          price: item.price || item.standard_rate || 0,
          category: item.category || "",
        }));

        const { category, brand, rating, discount } = selectedFilters;

        if (category) {
          formatted = formatted.filter((item) =>
            item.category.toLowerCase().includes(category.toLowerCase())
          );
        }

        if (brand) {
          formatted = formatted.filter((item) =>
            item.name.toLowerCase().includes(brand.toLowerCase())
          );
        }

        if (rating) {
          // Dummy: Assume all pass
          formatted = formatted.filter(() => true);
        }

        if (discount) {
          // Dummy: Assume all pass
          formatted = formatted.filter(() => true);
        }

        setProducts(formatted);

        const cartInit: Record<number, string> = {};
        formatted.forEach((item) => {
          cartInit[item.id] = "Add to Cart";
        });
        setCartStates(cartInit);
      } catch (err) {
        setError("Failed to fetch products");
      }
    };

    fetchProducts();
  }, [selectedFilters]);

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

  return (
    <div className="mt-5 px-[5%] py-5">
      <div className="flex flex-col md:flex-row gap-6">
        {/* Filters */}
        <div className="hidden md:flex flex-row md:flex-col w-full border border-ring/30 rounded-md md:w-72 overflow-x-auto md:overflow-visible gap-4 scrollbar-hide">
          <div className="flex flex-row md:flex-col flex-nowrap md:sticky md:top-24 bg-background ring ring-gray-300/30 rounded-md shadow-sm p-4 md:p-6 gap-4 min-w-max md:min-w-0">
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
                      className="block ml-auto text-xs text-blue-600 underline"
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
              <RangeSlider
                label=""
                min={7999}
                max={50000}
                defaultValue={9500}
              />
            </div>

            <div className="flex flex-col gap-2 min-w-[180px]">
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
            </div>
          </div>
        </div>

        {/* Product List */}
        <div className="w-full md:w-3/4 space-y-6">
          {products.map((product) => (
            <div key={product.id} className="border border-ring/30">
              <div className="grid grid-cols-[25%_45%_25%] mx-5 gap-4 p-4">
                <div
                  onClick={() => navigateProductPage(product.id)}
                  className="w-full h-full aspect-square overflow-hidden rounded-md cursor-pointer"
                >
                  <img
                    className="w-full h-full object-cover rounded-md"
                    src={product.image}
                    alt={product.name}
                  />
                </div>

                <div
                  className="space-y-2 px-2 cursor-pointer"
                  onClick={() => navigateProductPage(product.id)}
                >
                  <h4 className="text-lg font-semibold text-update/90">
                    {product.name}
                  </h4>
                  <div className="text-sm text-foreground/50">
                    <span className="bg-green-600 text-white text-xs w-max px-2 py-1 rounded">
                      4 ★
                    </span>{" "}
                    <span>76876 Reviews</span>
                  </div>
                  <p className="text-sm text-foreground/60 line-clamp-2">
                    {product.description}
                  </p>
                  <div className="hidden lg:flex flex-col">
                    <div className="text-xs line-clamp-1 ">
                      <span className="font-semibold">Bank Offer</span> 5%
                      cashback on Flipkart Axis Bank Credit Card upto ₹4,000 per
                      statement quarter
                    </div>
                    <div className="text-xs line-clamp-1">
                      <span className="font-semibold">Bank Offer</span> 5%
                      cashback on Flipkart Axis Bank Credit Card upto ₹4,000 per
                      statement quarter
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <p className="text-sm text-green-600">₹ {product.price}</p>
                    <p className="text-sm text-green-600">10% Offer</p>
                  </div>
                  <div className="my-2 flex flex-row gap-2 ">
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

                <div className="text-right space-y-2">
                  <div
                    className={`w-max block ml-auto text-white text-xs px-2 py-1 z-10 ${
                      product.count > 0
                        ? product.count < 3
                          ? `bg-purple-500`
                          : "bg-update"
                        : "bg-delete"
                    }`}
                  >
                    {product.count > 0
                      ? product.count < 3
                        ? `only ${product.count} left`
                        : "10% Offer"
                      : "Out Of Stock"}
                  </div>
                  <h2 className="text-sm md:text-xl font-bold">
                    ₹{product.price}
                  </h2>
                  <p className="text-sm text-foreground/60">
                    Delivery: 3–5 days
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CategoryPage;
