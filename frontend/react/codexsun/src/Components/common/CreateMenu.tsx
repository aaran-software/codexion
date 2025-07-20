import { useEffect, useRef, useState } from "react";
import Button from "../Input/Button";
import FloatingInput from "../Input/FloatingInput";

type CreateMenuProps = {
  onClose: () => void;
  onAdd: (item: string) => void;
  defaultValue: string;
};

function CreateMenu({ onClose, onAdd, defaultValue }: CreateMenuProps) {
  const [newItem, setNewItem] = useState<string>(defaultValue);
  const [enterPressedOnce, setEnterPressedOnce] = useState(false);

  const inputRef = useRef<HTMLInputElement>(null);
  const cancelRef = useRef<HTMLButtonElement>(null);
  const submitRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleAdd = () => {
    const trimmed = newItem.trim();
    if (trimmed) {
      onAdd(trimmed);
      onClose();
    } else {
      alert("Please enter a value before submitting.");
    }
  };

  const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      if (!enterPressedOnce) {
        setEnterPressedOnce(true);
        submitRef.current?.focus();
      } else {
        handleAdd();
      }
    } else if (e.key === "ArrowLeft") {
      cancelRef.current?.focus();
    } else if (e.key === "ArrowRight") {
      submitRef.current?.focus();
    }
  };

  return (
    <div className="bg-black/80 w-full h-full fixed top-0 left-0 z-50 flex items-center justify-center">
      <div className="w-[50%] bg-background text-foreground p-5 rounded-md shadow-md border border-ring flex flex-col gap-5">
        <FloatingInput
          id="new-item-input"
          label="Product"
          ref={inputRef}
          type="text"
          placeholder="Enter new item"
          value={newItem}
          err=""
          className="p-2 border border-gray-500 rounded-md"
          onChange={(e) => {
            setNewItem(e.target.value);
            setEnterPressedOnce(false); // reset enter state on change
          }}
          onKeyDown={handleInputKeyDown}
        />

        <div className="flex justify-end gap-5">
          <Button
            ref={cancelRef}
            label="Cancel"
            onClick={onClose}
            className="bg-red-600 w-max text-white"
            onKeyDown={(e) => {
              if (e.key === "ArrowRight") {
                submitRef.current?.focus();
              } else if (e.key === "ArrowLeft") {
                inputRef.current?.focus();
              }
            }}
          />

          <Button
            ref={submitRef}
            label="Submit"
            onClick={handleAdd}
            className="bg-green-600 w-max text-white"
            onKeyDown={(e) => {
              if (e.key === "ArrowLeft") {
                cancelRef.current?.focus();
              } else if (e.key === "ArrowRight") {
                inputRef.current?.focus(); // wrap around
              } else if (e.key === "Enter") {
                handleAdd();
              }
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default CreateMenu;
