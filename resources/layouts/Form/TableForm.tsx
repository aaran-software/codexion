import { useEffect, useState } from "react";
import FormLayout from "../../../resources/components/common/FormLayout";
import type {
  ApiList,
  Field,
  FieldGroup,
} from "../../../resources/components/common/commonform";
import { Column } from "../../../resources/components/common/commontable"; // Adjust path if needed
import { getNestedValue } from "../../../resources/global/library/utils";

interface TableFormProps {
  jsonPath: string | object;
  formName: string;
  formApi: ApiList;
  fieldPath: string;
  multipleEntry?: boolean;
}

function TableForm({
  formName,
  jsonPath,
  formApi,
  fieldPath,
  multipleEntry = false,
}: TableFormProps) {
  const [groupedFields, setGroupedFields] = useState<FieldGroup[]>([]);
  const [head, setHead] = useState<Column[]>([]);
  const [printableFields, setPrintableFields] = useState<string[]>([]);

  useEffect(() => {
    const fetchInvoiceConfig = async () => {
      try {
        const invoice = getNestedValue(jsonPath, fieldPath);
        // Adjust the path to access the invoice config
        if (!invoice) return;

        const head: Column[] = Object.values(invoice)
          .flatMap((section: any) => section.fields)
          .filter((field: any) => field.inTable);

        const groupedFields: FieldGroup[] = Object.entries(invoice).map(
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

        const printableFields: string[] = Object.values(invoice).flatMap(
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
          multipleEntry={multipleEntry}
          formName={formName}
        />
      )}
    </div>
  );
}

export default TableForm;
