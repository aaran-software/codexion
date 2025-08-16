import {useState} from "react";
import Sidebar from "../../../resources/components/sidebar/SecondSidebar";
import DocViewer from "../../../resources/UIBlocks/docs/DocViewer";

export default function Docs() {
    const [selectedSlug, setSelectedSlug] = useState<string | null>(null);

    return (
        <div className="flex h-screen pr-5 mb-3">
            <Sidebar onSelect={setSelectedSlug}/>
            <DocViewer slug={selectedSlug}/>
        </div>

    );
}
