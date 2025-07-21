import FormLayout from "../../../../../Components/common/FormLayout";
import type { ApiList, Field } from "../../../../../Components/common/commonform";
import { useState } from "react";
import master from "../../../../../../public/JSON/master.json";
function Styles() {
  const fieldSection = master.master.style;
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
    <div>
      <FormLayout
        groupedFields={groupedFields}
        head={head}
        formApi={formApi}
        printableFields={printableFields}
      />
    </div>
  );
}

export default Styles;
