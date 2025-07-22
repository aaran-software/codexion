import { useReducer, useState } from "react";
import { useNavigate } from "react-router-dom";
import vehicles from "../../../../public/assets/category/vehicles.png";
import AnimateButton from "../../../Components/Input/animatebutton";
import ImageButton from "../../../Components/Button/ImageBtn";
import Button from "../../../Components/Input/Button";
import Stepper from "../../../Resources/UIBlocks/Stepper";
import OrderSummary from "../../../Resources/UIBlocks/OrderSummary";
import AddressSection from "../../../Resources/UIBlocks/AddressSection";
import OrderPayment from "../../../Resources/UIBlocks/OrderPayment";
import OrderSuccess from "../../../Resources/UIBlocks/OrderSuccess";
import { LucideShoppingCart } from "lucide-react";

interface Product {
  id: number;
  title: string;
  price: number;
  image: string;
  category: string;
  quantity: number;
}

interface State {
  cartItems: Product[];
  savedItems: Product[];
}

type Action =
  | { category: "increase" | "decrease" | "remove"; payload: number }
  | { category: "saveLater"; payload: number }
  | { category: "moveToCart"; payload: number }
  | { category: "removeSaved"; payload: number };

const initialData: Product[] = [
  {
    id: 1,
    title: "Wireless Headphones",
    price: 59.99,
    image: vehicles,
    category: "Electronics",
    quantity: 1,
  },
  {
    id: 2,
    title: "Running Shoes",
    price: 89.49,
    image: vehicles,
    category: "Footwear",
    quantity: 1,
  },
  {
    id: 3,
    title: "Cotton T-shirt",
    price: 19.99,
    image: vehicles,
    category: "Clothing",
    quantity: 1,
  },
];

export default function Cart() {
  const sellerName = "Raja";
  const navigate = useNavigate();

  const [isPlaceOrder, setIsPlaceOrder] = useState(false);
  const [state, dispatch] = useReducer(reducer, {
    cartItems: initialData,
    savedItems: [],
  });

  const count = initialData.length;
  function reducer(state: State, action: Action): State {
    const { cartItems, savedItems } = state;

    switch (action.category) {
      case "increase":
      case "decrease":
        return {
          ...state,
          cartItems: cartItems.map((item) =>
            item.id === action.payload
              ? {
                  ...item,
                  quantity:
                    action.category === "increase"
                      ? item.quantity + 1
                      : Math.max(1, item.quantity - 1),
                }
              : item
          ),
        };

      case "remove":
        return {
          ...state,
          cartItems: cartItems.filter((item) => item.id !== action.payload),
        };

      case "saveLater": {
        const itemToSave = cartItems.find((i) => i.id === action.payload);
        if (!itemToSave) return state;

        return {
          ...state,
          cartItems: cartItems.filter((i) => i.id !== action.payload),
          savedItems: [...savedItems, itemToSave],
        };
      }

      case "moveToCart": {
        const itemToMove = savedItems.find((i) => i.id === action.payload);
        if (!itemToMove) return state;

        return {
          ...state,
          savedItems: savedItems.filter((i) => i.id !== action.payload),
          cartItems: [...cartItems, itemToMove],
        };
      }

      case "removeSaved":
        return {
          ...state,
          savedItems: savedItems.filter((i) => i.id !== action.payload),
        };

      default:
        return state;
    }
  }
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
  const navigateProductPage = (id: number) => {
    navigate(`/productpage/${id}`);
  };

  const totalPrice = state.cartItems.reduce(
    (acc, item) => acc + item.price * item.quantity,
    0
  );

  const renderItemCard = (item: Product, isSaved = false) => (
    <div
      key={item.id}
      className="border-b border-ring/30 pb-4 relative last:border-0"
    >
      <div className="grid grid-cols-3 gap-8 px-5">
        <div
          onClick={() => navigateProductPage(item.id)}
          className="cursor-pointer"
        >
          <img
            src={item.image}
            alt={item.title}
            className="object-contain w-30 mx-auto"
          />
        </div>

        <div
          onClick={() => navigateProductPage(item.id)}
          className="col-span-2 cursor-pointer"
        >
          <h4 className="text-lg font-semibold">{item.title}</h4>
          <p className="text-sm text-gray-500">{item.category}</p>
          <p className="text-xs text-gray-400">
            Seller: <strong>{sellerName}</strong>
          </p>
          <h2 className="text-xl mt-2 font-bold text-create">
            ${Number(item.price * item.quantity).toFixed(2)}
          </h2>
        </div>
      </div>

      <div className="grid grid-cols-3 mt-2 items-center">
        <div className="flex justify-center gap-2">
          {!isSaved && (
            <>
              <ImageButton
                className="bg-create p-2 text-white rounded"
                onClick={() =>
                  dispatch({ category: "decrease", payload: item.id })
                }
                disabled={item.quantity === 1}
                icon="minus"
              />
              <input
                type="number"
                value={item.quantity}
                readOnly
                className="w-12 text-center border rounded"
              />
              <ImageButton
                className="bg-create p-2 text-white rounded"
                onClick={() =>
                  dispatch({ category: "increase", payload: item.id })
                }
                icon="plus"
              />
            </>
          )}
        </div>

        <div className="flex gap-4 col-span-2 justify-end text-sm">
          {isSaved ? (
            <>
              <AnimateButton
                className="bg-create/90"
                onClick={() =>
                  dispatch({ category: "moveToCart", payload: item.id })
                }
                label="Move to cart"
                mode="cart"
              />
              <AnimateButton
                className="bg-update"
                onClick={() =>
                  dispatch({ category: "removeSaved", payload: item.id })
                }
                label="Remove"
                mode="delete"
              />
            </>
          ) : (
            <>
              <Button
                className="text-create cursor-pointer hover:border hover:border-ring/30"
                onClick={() =>
                  dispatch({ category: "saveLater", payload: item.id })
                }
                label="Save for Later"
              />
              <AnimateButton
                className="bg-update"
                onClick={() =>
                  dispatch({ category: "remove", payload: item.id })
                }
                label="Remove"
                mode="delete"
              />
            </>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div>
      <div className="flex gap-2 items-center px-5 lg:px-[10%]  my-10 ">
        <LucideShoppingCart size={25} className="text-create" />
        <h1 className="text-2xl font-bold">
          My Wishlist <span className="font-normal">({count})</span>
        </h1>
      </div>
      <div className="grid lg:grid-cols-[1fr_320px] px-5 lg:px-[10%] gap-10">
        {/* Left: Cart Items */}
        <div className="space-y-8 overflow-auto">
          <div className="space-y-4 p-5 border border-ring/30 rounded-md">
            {state.cartItems.map((item) => renderItemCard(item))}
          </div>

          {state.savedItems.length > 0 && (
            <div className=" border border-ring/30 mt-20 rounded-md p-5">
              <h3 className="text-xl font-semibold mb-4 ">Saved for Later</h3>
              <div className="mt-4 space-y-4 border-b last:border-0 pt-4">
                {state.savedItems.map((item) => renderItemCard(item, true))}
              </div>
            </div>
          )}
        </div>

        {/* Right: Sticky Price Summary */}
        <div className="w-full max-w-sm mx-auto shadow shadow-ring/40 p-5 space-y-4 lg:sticky top-20 self-start h-fit">
          <h4 className="text-lg font-bold text-update">Price Details</h4>
          <hr className="text-ring/30" />
          <div className="grid grid-cols-5">
            <p className="col-span-4">
              Price (
              {state.cartItems.reduce((acc, item) => acc + item.quantity, 0)}{" "}
              items)
            </p>
            <p className="text-right">${totalPrice.toFixed(2)}</p>
          </div>
          <div className="grid grid-cols-5">
            <p className="col-span-4">Discount</p>
            <p className="text-right">$0.00</p>
          </div>
          <div className="grid grid-cols-5">
            <p className="col-span-4">Delivery Charges</p>
            <p className="text-right">Free</p>
          </div>
          <hr className="text-ring/30" />
          <div className="grid grid-cols-5 font-semibold">
            <p className="col-span-4">Total Amount</p>
            <p className="text-right">${totalPrice.toFixed(2)}</p>
          </div>
          <button
            onClick={() => setIsPlaceOrder(!isPlaceOrder)}
            className="bg-update cursor-pointer w-full py-2 text-white font-medium rounded transition"
          >
            Place Order
          </button>
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
    </div>
  );
}
