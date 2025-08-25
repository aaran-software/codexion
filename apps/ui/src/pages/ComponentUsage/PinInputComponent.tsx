import { useRef } from "react";
import PinInput, { type PinInputHandle } from "../../../../../resources/components/input/PinInput"; // update path as needed

export default function PinInputComponent() {
  const pinRef = useRef<PinInputHandle>(null);

  const handleSubmit = () => {
    const pin = pinRef.current?.getPinValue();
    if (pin === "1234") {
      alert("PIN validated ✅");
    } else {
      alert("Invalid PIN ❌");
    }
  };

  return (
    <div className="max-w-md mx-auto space-y-6 mt-10">
      <h2 className="text-xl font-semibold">Enter 4-digit PIN</h2>

      <PinInput ref={pinRef} />

      <button
        onClick={handleSubmit}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Verify PIN
      </button>
    </div>
  );
}
