import { useState } from "react";
import { TextInput } from "../../../../../resources/components/secondary_input/TextInput"; // Adjust path if needed

function TextInputComponent() {
  const [name, setName] = useState("");
  const [nameError, setNameError] = useState("");

  const handleSubmit = () => {
    if (name.trim() === "") {
      setNameError("Name is required");
    } else {
      setNameError("");
      console.log("Submitted name:", name);
      // your logic here
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <TextInput
        id="name"
        label="Full Name"
        type="text"
        placeholder="Enter your name"
        value={name}
        err={nameError}
        onChange={(e) => setName(e.target.value)}
      />

      <button
        onClick={handleSubmit}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
      >
        Submit
      </button>
    </div>
  );
}

export default TextInputComponent;
