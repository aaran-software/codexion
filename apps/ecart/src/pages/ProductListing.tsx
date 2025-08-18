import React, { useState } from "react";
import {
  ApiList,
  Field,
} from "../../../../resources/components/common/commonform";
import vendor from "../../js/vendor.json";
import FormLayout from "../../../../resources/components/common/FormLayout";

export default function ProductListing() {
  const fieldSection = vendor.vendor.productlisting;
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
    <div className="h-full overflow-y-auto bg-dashboard-background text-dashboard-foreground">
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
}
