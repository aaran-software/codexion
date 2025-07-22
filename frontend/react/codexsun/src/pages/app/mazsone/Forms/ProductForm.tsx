import { useState } from "react";
import settings from "../../../../../public/JSON/mazsone/mazsone.json";
import CommonForm, {
  type Field,
  type ApiList,
} from "../../../../Components/common/commonform";

function ProductForm() {
  const productSection = settings.product;
  const [formOpen, setFormOpen] = useState(true);

  // ✅ Get editable fields from "specification" section
  const editableFields =
    productSection?.specification?.editable?.map((field: any) => ({
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
    })) || [];

  // ✅ Grouped fields from all sections except "specification"
  const groupedFields = Object.entries(productSection)
  .filter(
    ([, section]) =>
      typeof section === "object" &&
      section !== null &&
      "fields" in section &&
      Array.isArray((section as any).fields)
  )
  .map(([sectionKey, section]) => {
    const fields = (section as any).fields;

    return {
      title: section.title || sectionKey,
      sectionKey,
      fields: fields
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
    };
  });


  const productApi: ApiList = {
    create: "http://127.0.0.1:8000/api/products",
    read: "http://127.0.0.1:8000/api/products",
    update: "http://127.0.0.1:8000/api/products",
    delete: "http://127.0.0.1:8000/api/products",
  };

  const handleFormSubmit = (formData: any) => {
    console.log("Form submitted:", formData);
    setFormOpen(false);
  };

  return (
    <div className="w-full p-2 lg:pr-5">
      {formOpen && (
        <CommonForm
          groupedFields={groupedFields}
          editableFields={editableFields}
          isPopUp={false}
          formOpen={formOpen}
          setFormOpen={setFormOpen}
          formName="Product"
          successMsg="Form submitted successfully"
          faildMsg="Form submission failed"
          initialData={{}}
          onSubmit={handleFormSubmit}
          editableTable={true}
          api={productApi}
          
        />
      )}
    </div>
  );
}

export default ProductForm;
