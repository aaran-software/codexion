import React from "react";

type ListingItem = {
  id: string;
  name: string;
  price: number;
  stock: number;
  category: string;
  image?: string;
};

const mockData: ListingItem[] = [
  {
    id: "SKU-001",
    name: "Sample Product Name That Might Be Long",
    price: 15000,
    stock: 10,
    category: "Mobile",
    image: "",
  },
];

export default function ProductListing() {
  return (
    <div className="h-full overflow-y-auto bg-background text-foreground">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3">
        <h1 className="text-xl font-semibold">Listing Management</h1>
        <button
          className="rounded-2xl px-5 py-2 border border-ring/30 bg-foreground text-background hover:opacity-90 transition"
          type="button"
        >
          Add New Item
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 p-5">
        {[
          { label: "Active Item", value: 0 },
          { label: "Blocked Item", value: 0 },
          { label: "Inactive Item", value: 0 },
          { label: "Archived Listing", value: 0 },
        ].map((s) => (
          <div
            key={s.label}
            className="rounded-2xl border border-ring/30 p-4 text-center"
          >
            <p className="text-2xl font-semibold">{s.value}</p>
            <p className="text-sm opacity-80">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Desktop / Large screens: Table */}
      <div className="hidden lg:block px-5 pb-8">
        <table className="w-full border border-ring/30 border-collapse rounded-2xl overflow-hidden">
          <thead className="bg-background">
            <tr>
              <th className="border-t border-ring/30 p-3 text-center">S.No</th>
              <th className="border-t border-ring/30 p-3 text-center">
                Product
              </th>
              <th className="border-t border-ring/30 p-3 text-center">Price</th>
              <th className="border-t border-ring/30 p-3 text-center">Stock</th>
              <th className="border-t border-ring/30 p-3 text-center">
                Category
              </th>
              <th className="border-t border-ring/30 p-3 text-center">
                Action
              </th>
            </tr>
          </thead>

          <tbody>
            {mockData.map((item, idx) => (
              <tr key={item.id} className="even:bg-background">
                <td className="border-t border-ring/30 p-3 text-center">
                  {idx + 1}
                </td>

                <td className="border-t border-ring/30 p-3">
                  <div className="grid grid-cols-[60px_1fr] gap-3 items-center">
                    <img
                      src={item.image || ""}
                      alt="Product"
                      className="mx-auto block h-[60px] w-[50px] object-contain"
                    />
                    <div className="min-w-0">
                      <p className="truncate font-medium" title={item.name}>
                        {item.name}
                      </p>
                      <p className="text-sm opacity-70">{item.id}</p>
                    </div>
                  </div>
                </td>

                <td className="border-t border-ring/30 p-3 text-center">
                  ₹{item.price.toLocaleString("en-IN")}
                </td>

                <td className="border-t border-ring/30 p-3 text-center">
                  {item.stock}
                </td>

                <td className="border-t border-ring/30 p-3 text-center">
                  {item.category}
                </td>

                <td className="border-t border-ring/30 p-3 text-center">
                  <button
                    type="button"
                    className="underline underline-offset-2 hover:opacity-80"
                  >
                    Edit Item
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile / Tablet message */}
      <div className="lg:hidden flex h-screen items-center justify-center bg-background px-5">
        <div className="rounded-2xl border border-ring/30 p-5 max-w-xl">
          <p className="leading-relaxed">
            This page is optimized for larger screens. Please use a desktop or
            enlarge your window to manage listings.
          </p>
        </div>
      </div>
    </div>
  );
}
