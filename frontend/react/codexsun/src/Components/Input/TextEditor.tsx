"use client"

import { useState } from "react"
import { Editor } from "primereact/editor"

// Optional: PrimeReact styles (if not globally included)
// import "primereact/resources/themes/lara-light-blue/theme.css"
// import "primereact/resources/primereact.min.css"
// import "primeicons/primeicons.css"

export default function TextEditor() {
  const [text, setText] = useState<string>("")

  return (
    <div className="p-6 space-y-6">
      <div className="card">
        <h2 className="text-lg font-semibold mb-2">Rich Text Editor</h2>
        <div className="text-foreground">
            <Editor
            value={text}
            onTextChange={(e) => setText(e.htmlValue ?? "")}
            style={{ height: "200px" }}
            />
        </div>
      </div>

        
      {text.trim() !== "" && (
        <div className="card">
            <h2 className="text-lg font-semibold mb-2">Live Preview</h2>
            <div
            className="border p-4 min-h-[100px] text-foreground rounded"
            dangerouslySetInnerHTML={{ __html: text }}
            />
        </div>
        )}


    </div>
  )
}
