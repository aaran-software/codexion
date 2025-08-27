import { useState } from "react";
import { TextArea } from "../../../../../resources/components/input/text-area"; // adjust path if needed

function TextAreaComponent() {
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = () => {
    if (description.trim() === "") {
      setError("Description is required.");
    } else {
      setError("");
      console.log("Submitted description:", description);
      // Do your submit logic here
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <TextArea
        id="description"
        label="Description"
        placeholder="Enter your description..."
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        err={error}
        className="min-h-[100px]" // optional Tailwind override
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

export default TextAreaComponent;

