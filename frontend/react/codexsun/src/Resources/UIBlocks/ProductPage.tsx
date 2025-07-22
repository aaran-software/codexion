import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import apiClient from "../../pages/app/ecart/api/apiClients";
import ProductCard from "./ProductCard";
// import Tooltipcomp from "../../Components/Tooltip/tooltipcomp";
import RatingReviews from "./RatingReviews";
import Settings from "../../../public/JSON/ecart/ecart.json";
import Button from "../../Components/Input/Button";
import Stepper from "./Stepper";
import OrderSummary from "./OrderSummary";
import AddressSection from "./AddressSection";
import OrderPayment from "./OrderPayment";
import OrderSuccess from "./OrderSuccess";
import VerticalImageList from "./Slider/VerticalImageList";

// Define types
interface Field {
  id: string;
  key: string;
  label: string;
  type: string;
  value: string;
}

interface Group {
  id: string;
  title: string;
  fields?: Field[];
  children?: Record<string, Group>;
}

interface Product {
  id: number;
  name: string;
  price: number;
  count: number;
  description: string;
  category: string;
  offer: number;
  slideOffer: number;
  images?: string[];
}

function ProductPage() {
  const { id } = useParams();
  const [product, setProduct] = useState<Product | null>(null);
  const [selectedImage, setSelectedImage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isPlaceOrder, setIsPlaceOrder] = useState(false);
  const navigate = useNavigate();

  // const [offer] = useState([
  //   {
  //     title: "",
  //     content:
  //       "5% cashback on Flipkart Axis Bank Credit Card upto ₹4,000 per statement quarter",
  //     tooltip: { message: "T&C message..." },
  //   },
  //   {
  //     title: "Bank Offer",
  //     content:
  //       "5% cashback on Flipkart Axis Bank Credit Card upto ₹4,000 per statement quarter",
  //     tooltip: { message: "T&C message..." },
  //   },
  //   {
  //     title: "Bank Offer",
  //     content:
  //       "5% cashback on Flipkart Axis Bank Credit Card upto ₹4,000 per statement quarter",
  //     tooltip: { message: "T&C message..." },
  //   },
  //   {
  //     title: "Bank Offer",
  //     content:
  //       "5% cashback on Flipkart Axis Bank Credit Card upto ₹4,000 per statement quarter",
  //     tooltip: { message: "T&C message..." },
  //   },
  //   {
  //     title: "Bank Offer",
  //     content:
  //       "5% cashback on Flipkart Axis Bank Credit Card upto ₹4,000 per statement quarter",
  //     tooltip: { message: "T&C message..." },
  //   },
  //   {
  //     title: "Bank Offer",
  //     content:
  //       "5% cashback on Flipkart Axis Bank Credit Card upto ₹4,000 per statement quarter",
  //     tooltip: { message: "T&C message..." },
  //   },
  //   {
  //     title: "Bank Offer",
  //     content:
  //       "5% cashback on Flipkart Axis Bank Credit Card upto ₹4,000 per statement quarter",
  //     tooltip: { message: "T&C message..." },
  //   },
  //   {
  //     title: "Bank Offer",
  //     content:
  //       "5% cashback on Flipkart Axis Bank Credit Card upto ₹4,000 per statement quarter",
  //     tooltip: { message: "T&C message..." },
  //   },
  //   {
  //     title: "Bank Offer",
  //     content:
  //       "5% cashback on Flipkart Axis Bank Credit Card upto ₹4,000 per statement quarter",
  //     tooltip: { message: "T&C message..." },
  //   },
  // ]);
  // const [showAllOffers, setShowAllOffers] = useState(false);
  // const visibleOffers = showAllOffers ? offer : offer.slice(0, 5);
  const BASE_URL = "https://dev.aaranerp.com/"; // Replace with actual URL

  useEffect(() => {
    if (!id) return;

    apiClient
      .get(`/api/resource/Product/${id}`)
      .then((res) => {
        const data = res.data.data || res.data;

        // Collect all image fields like image, image1, image2, etc.
        const imageKeys = Object.keys(data).filter(
          (key) => key.startsWith("image") && data[key]
        );
        const imageList = imageKeys.map((key) => BASE_URL + data[key]);

        setProduct({
          ...data,
          name: data.display_name,
          price: data.price,
          offer: data.product_offer,
          slideOffer: data.slider_offer,
          images: imageList,
          description: data.description,
          category: data.category,
          count: data.stock_qty,
        });

        if (imageList.length > 0) {
          setSelectedImage(imageList[0]);
        }
      })
      .catch(() => setError("Product not found"))
      .finally(() => setLoading(false));
  }, [id]);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [id]);

  if (loading) return <div className="text-center mt-10">Loading...</div>;
  if (!product || error)
    return <div className="text-center mt-10 text-red-500">{error}</div>;

  const activeOffer = product.slideOffer ?? product.offer;
  const prePrice = activeOffer
    ? Math.round(product.price / (1 - activeOffer / 100))
    : product.price;

  const steps = [
    {
      title: "Order Summary",
      content: <OrderSummary />,
    },
    {
      title: "Address",
      content: <AddressSection />,
    },
    {
      title: "Payment",
      content: <OrderPayment />,
    },
    {
      title: "Confirmation",
      content: (
        <OrderSuccess
          orderId="ORD12345678"
          paymentId="PAY987654321"
          onContinue={() => navigate("/")}
        />
      ),
    },
  ];
  return (
    <div className="py-10 sm:px-[5%] mx-auto">
      <div className="grid lg:grid-cols-2 gap-5 xl:grid-cols-[35%_65%] items-start">
        {/* Image Section */}
        <div className="lg:sticky top-20 h-fit">
          <div className="flex flex-col border border-ring/20 p-2 lg:flex-row gap-4 items-start">
            <div className="hidden lg:block">
              <VerticalImageList
                images={product.images || []}
                selectedIndex={(product.images || []).findIndex(
                  (img) => img === selectedImage
                )}
                onSelect={(index) => setSelectedImage(product.images![index])}
              />
            </div>
            {/* main image */}
            <div className="block m-auto flex-1">
              <div className="w-full h-full min-w-[310px] min-h-[310px] max-w-[400px] max-h-[400px] mx-auto">
                <img
                  src={selectedImage}
                  alt={product.name}
                  loading="lazy"
                  className="w-full h-full object-contain rounded transition duration-300 ease-in-out"
                />
              </div>
            </div>

            <div className="lg:hidden mt-4 w-[310px] block mx-auto overflow-x-auto">
              <VerticalImageList
                images={product.images || []}
                selectedIndex={(product.images || []).findIndex(
                  (img) => img === selectedImage
                )}
                direction="horizontal"
                onSelect={(index) => setSelectedImage(product.images![index])}
              />
            </div>
          </div>
        </div>

        {/* Product Info */}
        <div className="space-y-4 px-2">
          <h1 className="text-xl text-update font-semibold">{product.name}</h1>
          <h1 className="text-SM text-foreground/80">{product.description}</h1>
          <div className="text-sm text-foreground/50">
            <span className="bg-green-600 text-white text-xs w-max px-2 py-1 rounded">
              4 ★
            </span>{" "}
            <span>76876 rating</span> & <span>7868 Reviews</span>
          </div>
          <p className="text-2xl font-bold flex gap-2">
            ₹{product.price}{" "}
            {product.offer > 0 && (
              <div className="flex items-center">
                <span className="line-through text-sm text-foreground/30">
                  ₹{prePrice}
                </span>
                <span className="text-sm ml-2 text-create">
                  {product.slideOffer ? product.slideOffer : product.offer} %
                  Offer
                </span>
              </div>
            )}
          </p>
          <p className="text-sm text-gray-500">Extra fee</p>

          {/* <p className="text-foreground text-md font-semibold">
            Available Offer
          </p>
          {visibleOffers.map((off, index) => (
            <div key={index}>
              <span className="font-semibold">{off.title}</span> {off.content}{" "}
              <Tooltipcomp
                label={"T&C"}
                tip={off.tooltip.message}
                className={"text-update font-bold"}
              />
            </div>
          ))} */}

          {/* {offer.length > 5 && (
            <button
              className="mt-2 text-sm text-blue-600 underline"
              onClick={() => setShowAllOffers(!showAllOffers)}
            >
              {showAllOffers ? "Show Less" : "Show More"}
            </button>
          )} */}

          <div className="flex justify-between mt-5 gap-4">
            <Button
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
              label={" Add to Cart"}
            />

            <Button
              disabled={product.count < 1}
              onClick={() => setIsPlaceOrder(!isPlaceOrder)}
              className={`flex-1 px-4 py-2 rounded transition 
              ${
                product.count < 1
                  ? "bg-gray-400 cursor-not-allowed text-white"
                  : "bg-green-600 hover:bg-green-700 text-white"
              }
            `}
              label={"Buy Now"}
            />
          </div>
          {/* Specifications */}
          <div className="mt-10 border border-ring/30 rounded-md p-5">
            <h2 className="text-3xl font-bold border-b border-ring/30 pb-3 text-foreground/90 mb-4">
              {Settings.product.specification_read.title}
            </h2>

            {Object.values(Settings.product.specification_read.groups).map(
              (submenuRaw) => {
                const submenu = submenuRaw as Group;

                const hasFields =
                  Array.isArray(submenu.fields) && submenu.fields.length > 0;
                const hasChildren =
                  submenu.children && Object.keys(submenu.children).length > 0;

                if (!hasFields && !hasChildren) return null;

                return (
                  <div
                    key={submenu.id}
                    className="mb-6 border-b border-ring/30 pb-3 last:border-0"
                  >
                    <h3 className="text-lg text-foreground font-bold">
                      {submenu.title}
                    </h3>

                    {hasFields && (
                      <div className="space-y-1 mt-2">
                        {submenu.fields?.map((field) => (
                          <div
                            key={field.id}
                            className="flex justify-between py-1 text-sm"
                          >
                            <span className="text-foreground/70">{field.label}</span>
                            <span className="font-medium text-foreground/70">
                              {field.value}
                            </span>
                          </div>
                        ))}
                      </div>
                    )}

                    {hasChildren &&
                      Object.values(submenu.children!).map((childRaw) => {
                        const child = childRaw as Group;

                        if (
                          !Array.isArray(child.fields) ||
                          child.fields.length === 0
                        )
                          return null;

                        return (
                          <div key={child.id} className="ml-4 mt-3">
                            <h4 className="text-sm font-semibold text-gray-700 mb-1">
                              {child.title}
                            </h4>
                            {child.fields.map((field) => (
                              <div
                                key={field.id}
                                className="flex justify-between py-1 text-sm"
                              >
                                <span className="text-gray-600">
                                  {field.label}
                                </span>
                                <span className="font-medium text-gray-800">
                                  {field.value}
                                </span>
                              </div>
                            ))}
                          </div>
                        );
                      })}
                  </div>
                );
              }
            )}
          </div>

          {/* Buttons */}

          <div className="mt-10">
            <RatingReviews />
          </div>
        </div>
      </div>

      {/* Similar Products */}
      <div className="mt-12">
        <ProductCard
          title="Similar Items"
          api={`api/resource/Product?fields=["name"]&filters=[["is_popular", "=", 1]]`}
          ribbon={true}
        />
      </div>
      {isPlaceOrder && (
        <div className="fixed top-1/2 z-10000 left-1/2 w-full p-2 lg:w-[80%] h-[90vh] transform -translate-x-1/2 -translate-y-1/2 shadow overflow-scroll scrollbar-hide">
          <Stepper
            steps={steps}
            onClose={() => setIsPlaceOrder(!isPlaceOrder)}
            onFinish={() => navigate("/")}
          />
        </div>
      )}
      {isPlaceOrder && (
        <div className="fixed z-1000 top-1/2 left-1/2 w-full h-full bg-black/50 transform -translate-x-1/2 -translate-y-1/2"></div>
      )}
    </div>
  );
}

export default ProductPage;
