import { useEffect, useState } from "react";
import FormLayout from "../../../../../resources/components/common/FormLayout";
import type {
  ApiList,
  Field,
  FieldGroup,
} from "../../../../../resources/components/common/commonform";
import apiClient from "../../../../../resources/global/api/apiClients";
import { Column } from "../../../../../resources/components/common/commontable"; // Adjust path if needed

// Define type for groupedFields
type GroupedFieldSection = {
  title: string;
  sectionKey: string;
  fields: Column[];
};

function Purchase() {
  const [groupedFields, setGroupedFields] = useState<FieldGroup[]>([]);
  const [head, setHead] = useState<Column[]>([]);
  const [printableFields, setPrintableFields] = useState<string[]>([]);

  const [formApi] = useState<ApiList>({
    create: "/api/purchases",
    read: "/api/purchases",
    update: "/api/purchases",
    delete: "/api/purchases",
  });

  useEffect(() => {
    const fetchInvoiceConfig = async () => {
      try {
        // option:1
        const res = await apiClient.get("/api/config/invoice/purchase");

        // 🔁 Change this to `sales` if needed
        const purchase = res.data;

        // option:2
        // const res = await apiClient.get("/api/config/invoice");
        // const invoice = res.data?.invoice?.sales;

        if (!purchase) return;

        const head: Column[] = Object.values(purchase)
          .flatMap((section: any) => section.fields)
          .filter((field: any) => field.inTable);

        const groupedFields: FieldGroup[] = Object.entries(purchase).map(
          ([sectionKey, section]: [string, any]) => ({
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

        const printableFields: string[] = Object.values(purchase).flatMap(
          (section: any) =>
            section.fields.filter((field: any) => field.isPrint === true)
        );

        setGroupedFields(groupedFields);
        setHead(head);
        setPrintableFields(printableFields);
      } catch (err) {
        console.error("Failed to load invoice config:", err);
      }
    };

    fetchInvoiceConfig();
  }, []);

  return (
    <div>
      {groupedFields.length > 0 && head.length > 0 && (
        <FormLayout
          groupedFields={groupedFields}
          head={head}
          formApi={formApi}
          printableFields={printableFields}
        />
      )}
    </div>
  );
}

export default Purchase;
