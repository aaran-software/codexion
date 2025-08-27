import { useState } from "react";
import PasswordInput from "../../../../../resources/components/input/password-input"; // adjust the path as necessary

export default function PasswordComponent() {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = () => {
    if (!password || password.length < 8) {
      setError("Password must be at least 8 characters");
    } else {
      setError("");
      console.log("Submitted Password:", password);
      // further logic
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10  border border-ring/80 p-4 rounded-md shadow">
      <PasswordInput
        id="password"
        label="Enter your password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        error={error}
      />

      <button
        onClick={handleSubmit}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
      >
        Login
      </button>
    </div>
  );
}
