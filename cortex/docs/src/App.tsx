import { useState } from "react";
import Sidebar from "./components/Sidebar";
import DocViewer from "./components/DocViewer";

export default function App() {
  const [selectedSlug, setSelectedSlug] = useState<string | null>(null);

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <Sidebar onSelect={setSelectedSlug} />
      <DocViewer slug={selectedSlug} />
    </div>
  );
}
