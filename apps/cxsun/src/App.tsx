import React from "react";
import Accordion from "../../../resources/components/accordion/Accordion";


export default function App() {
    return (
        <div className="p-10 text-xl text-blue-600">
            <div>🚀 Hello from <b>cxsun</b> — React + Vite + Tailwind 4</div>

            <Accordion items={[{"question": "src", "answer": "src"}, {"question": "src", "answer": "src"}]}/>

        </div>
    );
}
