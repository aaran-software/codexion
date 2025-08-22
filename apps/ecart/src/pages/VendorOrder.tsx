import React, { useState } from "react";
import {
  ApiList,
  Field,
} from "../../../../resources/components/common/commonform";
import vendor from "../../js/vendor.json";
import FormLayout from "../../../../resources/components/common/FormLayout";

const VendorOrder: React.FC = () => {
  const [activeButton, setActiveButton] = useState(0);

  const orderViews = [
    "ALL",
    "NEW",
    "CONFIRMED",
    "TO BE PACKED",
    "READY FOR DISPATCH",
  ];

  const fieldSection = vendor.vendor.orderproduct;
  const head = Object.values(fieldSection)
    .flatMap((section: any) => section.fields)
    .filter((field: any) => field.inTable);

  const groupedFields = Object.entries(fieldSection).map(
    ([sectionKey, section]) => ({
      title: section.title || sectionKey,
      sectionKey,
      fields: section.fields
        .filter(
          (field: any) =>
            field.key !== "action" &&
            field.key !== "id" &&
            field.isForm === true
        )
        .map((field: any) => ({
          id: field.key,
          label: field.label,
          type: (field.type || "textinput") as Field["type"],
          className: "w-full",
          errMsg: `Enter ${field.label}`,
          ...(field.type?.includes("dropdown") && field.options
            ? { options: field.options }
            : {}),
          readApi: field.readApi,
          updateApi: field.updateApi,
          apiKey: field.apiKey,
          createKey: field.createKey,
        })),
    })
  );
  const printableFields = Object.values(fieldSection).flatMap((section: any) =>
    section.fields.filter((field: any) => field.isPrint === true)
  );
  const [formApi] = useState<ApiList>({
    create: "/api/resource/Customer",
    read: "/api/resource/Customer",
    update: "/api/resource/Customer",
    delete: "/api/resource/Customer",
  });

  return (
    <div className="bg-dashboard-background text-dashboard-foreground h-full">
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

      <div className="mt-5">
        <FormLayout
          groupedFields={groupedFields}
          head={head}
          formApi={formApi}
          printableFields={printableFields}
          multipleEntry={false}
          formName={"Product"}
        />
      </div>
    </div>
  );
};

export default VendorOrder;
