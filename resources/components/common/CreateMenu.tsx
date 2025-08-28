import { useEffect, useRef, useState } from "react";
import Button from "../../../resources/components/button/Button";
import FloatingInput from "../input/floating-input";
import { Field } from "../common/commonform";

type CreateMenuProps = {
  onClose: () => void;
  onAdd: (item: string | Record<string, any>) => void;
  fields?: Field[]; // optional multiple fields
  defaultValue?: string; // fallback for single input
  label: string;
};

function CreateMenu({
  onClose,
  onAdd,
  defaultValue = "",
  label,
  fields,
}: CreateMenuProps) {
const initialData: Record<string, any> = fields
  ? fields.reduce((acc, f) => ({
      ...acc,
      [f.id]: f.id === (fields[0]?.id) ? defaultValue : "", // pre-fill dropdown key
    }), {})
  : { name: defaultValue };


  const [formData, setFormData] = useState<Record<string, any>>(initialData);

  const inputRefs = useRef<Record<string, HTMLInputElement | null>>({});

  useEffect(() => {
    const firstKey = Object.keys(inputRefs.current)[0];
    if (firstKey) inputRefs.current[firstKey]?.focus();
  }, []);

  const handleChange = (id: string, value: string) => {
    setFormData((prev) => ({ ...prev, [id]: value }));
  };

  const handleAdd = () => {
    // Validate required fields
    const emptyField = Object.entries(formData).find(
      ([_, v]) => v.trim() === ""
    );
    if (emptyField) {
      alert(`Please enter a value for "${emptyField[0]}"`);
      return;
    }

    // Call parent handler
    if (fields && fields.length > 0) {
      onAdd(formData); // multiple fields
    } else {
      onAdd(formData.name); // single input
    }
    onClose();
  };

  const handleKeyDown = (
    e: React.KeyboardEvent<HTMLInputElement>,
    idx: number
  ) => {
    const keys = Object.keys(formData);
    if (e.key === "Enter") {
      e.preventDefault();
      const nextKey = keys[idx + 1];
      if (nextKey) inputRefs.current[nextKey]?.focus();
      else handleAdd();
    }
  };

  return (
    <div className="bg-black/80 w-full h-full fixed top-0 left-0 z-50 flex items-center justify-center">
      <div className="w-[50%] bg-background text-foreground p-5 rounded-md shadow-md border border-ring flex flex-col gap-5">
        {(fields && fields.length > 0
          ? fields
          : [{ id: "name", label, type: "textinput", className: "" }]
        ).map((f, idx) => (
          <FloatingInput
            key={f.id}
            id={f.id}
            label={f.label}
            ref={(el) => {
              inputRefs.current[f.id] = el;
            }}
            type="text"
            placeholder={`Enter ${f.label}`}
           value={formData[f.id]}
            err=""
            className="p-2 border border-gray-500 rounded-md"
            onChange={(e) => handleChange(f.id, e.target.value)}
            onKeyDown={(e) => handleKeyDown(e, idx)}
          />
        ))}

        <div className="flex justify-end gap-5">
          <Button
            label="Cancel"
            onClick={onClose}
            className="bg-red-600 w-max text-white"
          />
          <Button
            label="Submit"
            onClick={handleAdd}
            className="bg-green-600 w-max text-white"
          />
        </div>
      </div>
    </div>
  );
}

export default CreateMenu;
