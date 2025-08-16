import React, { useState } from "react";

const VendorOrder: React.FC = () => {
  const [activeButton, setActiveButton] = useState(0);

  const orderViews = [
    "ALL",
    "NEW",
    "CONFIRMED",
    "TO BE PACKED",
    "READY FOR DISPATCH",
  ];

  return (
    <div className="bg-background text-foreground h-full overflow-y-auto">
      {/* Page Title */}
      <h1 className="px-5 pt-4 text-xl font-semibold">My Orders</h1>

      {/* Order Status Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mt-5 px-3">
        {/* Order Processing */}
        <div>
          <p className="font-medium mb-2">Order Processing</p>
          <div className="flex gap-2">
            <div className="flex-1 rounded-lg border border-ring/30 p-3 text-center">
              <p className="text-lg font-semibold">0</p>
              <p className="text-sm opacity-70">Pending Items</p>
            </div>
            <div className="flex-1 rounded-lg border border-ring/30 p-3 text-center">
              <p className="text-lg font-semibold">0</p>
              <p className="text-sm opacity-70">Pending RTD</p>
            </div>
          </div>
        </div>

        {/* Dispatched Orders */}
        <div>
          <p className="font-medium mb-2">Dispatched Orders</p>
          <div className="flex gap-2">
            <div className="flex-1 rounded-lg border border-ring/30 p-3 text-center">
              <p className="text-lg font-semibold">0</p>
              <p className="text-sm opacity-70">Dispatched</p>
            </div>
            <div className="flex-1 rounded-lg border border-ring/30 p-3 text-center">
              <p className="text-lg font-semibold">0</p>
              <p className="text-sm opacity-70">Pending Services</p>
            </div>
          </div>
        </div>

        {/* Completed Orders */}
        <div>
          <p className="font-medium mb-2">Completed Orders</p>
          <div className="rounded-lg border border-ring/30 p-3 text-center">
            <p className="text-lg font-semibold">0</p>
            <p className="text-sm opacity-70">In last 30 Days</p>
          </div>
        </div>
      </div>

      {/* Order View Buttons */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 px-5 mt-6">
        {orderViews.map((label, index) => (
          <p
            key={index}
            onClick={() => setActiveButton(index)}
            className={`cursor-pointer text-center pb-2 transition border-b-4 ${
              activeButton === index
                ? "border-blue-500 font-medium"
                : "border-transparent hover:border-blue-400"
            }`}
          >
            {label}
          </p>
        ))}
      </div>

      {/* Order Managing List (Desktop only) */}
      <div className="hidden lg:grid grid-cols-[30%_20%_20%_20%_10%] gap-2 mt-6 px-5 border border-ring/30 rounded-lg p-4">
        {/* Product Info */}
        <div className="flex gap-3 items-center">
          <img
            src={""}
            alt="product"
            className="h-16 w-16 object-contain rounded-md border border-ring/30"
          />
          <div>
            <p className="font-medium">Name</p>
            <p className="text-sm opacity-70">Quantity</p>
            <p className="text-sm opacity-70">Item Code</p>
          </div>
        </div>

        {/* Price */}
        <div>
          <p className="font-medium">Price</p>
          <p className="text-sm opacity-70">Cash on Delivery</p>
        </div>

        {/* IDs */}
        <div>
          <p className="font-medium">Shipment ID</p>
          <p className="text-sm opacity-70">Order ID</p>
        </div>

        <div>
          <p className="font-medium">AWB</p>
          <p className="text-sm opacity-70">Invoice ID</p>
        </div>

        {/* Actions */}
        <div className="flex flex-col gap-2">
          <button className="rounded-md border border-ring/30 px-3 py-1 text-sm hover:bg-foreground hover:text-background transition">
            Confirm
          </button>
          <button className="rounded-md border border-ring/30 px-3 py-1 text-sm hover:bg-foreground hover:text-background transition">
            Cancel
          </button>
        </div>
      </div>

      {/* Mobile / Tablet Notice */}
      <div className="lg:hidden flex h-screen items-center justify-center px-5">
        <div className="rounded-xl border border-ring/30 bg-background p-6 text-center">
          <p className="leading-relaxed">
            This page is optimized for larger screens. Please use a desktop or
            enlarge your window to manage orders.
          </p>
        </div>
      </div>
    </div>
  );
};

export default VendorOrder;
