import {useState} from "react";
import Sidebar from "./components/Sidebar";
import DocViewer from "./components/DocViewer";

export default function App() {
    const [selectedSlug, setSelectedSlug] = useState<string | null>(null);

    return (
        <div className="flex h-screen">
            <Sidebar onSelect={setSelectedSlug}/>
            <DocViewer slug={selectedSlug}/>
        </div>

    );
}
