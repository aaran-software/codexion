import FloatingInput from "../../resources/components/input/FloatingInput";
import Button from "../../resources/components/button/Button";
import React, {useState, useRef, useEffect, useCallback} from "react";
import ImageBtn from "../components/button/ImageBtn";
import Tooltipcomp from "../components/Tooltip/tooltipcomp";
import apiClient from "../../resources/global/api/apiClients";

export default function Editor({apiPath}: { apiPath: string }) {
    const [title, setTitle] = useState("");
    // rawMessage now holds the HTML content as the source of truth for saving/preview
    const [rawMessage, setRawMessage] = useState("");
    // CORRECTED: editorRef type is HTMLDivElement
    const editorRef = useRef<HTMLDivElement>(null);
    // NEW: Separate ref for the font size input field
    const fontSizeInputRef = useRef<HTMLInputElement>(null);
    const [fontSizeInput, setFontSizeInput] = useState("");
    const [isPreviewMode, setIsPreviewMode] = useState(false);
    const [hasSelection, setHasSelection] = useState(false);

    const [textColor, setTextColor] = useState("#000000");
    const [bgColor, setBgColor] = useState("#ffffff");

    // Function to apply formatting
    const applyFormatting = (command: string, value: string | undefined = undefined) => {
        if (!editorRef.current) return;
        editorRef.current.focus(); // Ensure editor is focused
        document.execCommand(command, false, value);
        // After applying a format, immediately update the state from the DOM
        setRawMessage(editorRef.current.innerHTML);
    };

    const handleBold = () => applyFormatting("bold");
    const handleItalic = () => applyFormatting("italic");
    const handleUnderline = () => applyFormatting("underline");

    // Helper function to transform selected text (for uppercase/lowercase)
    const transformSelectedText = (transformFn: (text: string) => string) => {
        const selection = window.getSelection();
        if (!selection || selection.rangeCount === 0 || !editorRef.current) return;

        const range = selection.getRangeAt(0);
        // Ensure the selection is within our editable div
        if (!editorRef.current.contains(range.commonAncestorContainer)) return;

        if (range.collapsed) return; // no text selected

        const selectedText = range.toString();
        const transformedText = transformFn(selectedText);

        // Replace the selected text. For complex styling, you'd insert a span.
        // For simple text transformation, replacing with a text node is fine.
        range.deleteContents();
        range.insertNode(document.createTextNode(transformedText));

        // After modification, update the rawMessage from the DOM
        setRawMessage(editorRef.current.innerHTML);
    };

    const handleUppercase = () => {
        transformSelectedText((text) => text.toUpperCase());
    };

    const handleLowercase = () => {
        transformSelectedText((text) => text.toLowerCase());
    };

    const handleTextColorInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        const color = e.target.value;
        setTextColor(color);
        applyFormatting("foreColor", color);
    };

    const handleBgColorInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        const color = e.target.value;
        setBgColor(color);
        applyFormatting("backColor", color);
    };

    const applyLinkToSelection = () => {
        const url = prompt("Enter the URL:");
        if (!url || !editorRef.current) return;

        const selection = window.getSelection();
        if (!selection || selection.rangeCount === 0) return;

        const range = selection.getRangeAt(0);
        if (!editorRef.current.contains(range.commonAncestorContainer)) return;

        const selectedText = selection.toString();
        if (!selectedText) return;

        // Clean out any existing <a> tags from the selected text
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = selectedText;
        const clean = tempDiv.textContent || tempDiv.innerText || "";

        const anchor = document.createElement("a");
        anchor.href = url;
        anchor.target = "_blank";
        anchor.rel = "noopener noreferrer";
        anchor.style.color = "blue";
        anchor.style.textDecoration = "underline";
        anchor.style.cursor = "pointer";
        anchor.textContent = clean;

        range.deleteContents();
        range.insertNode(anchor);

        // Move cursor after the inserted anchor
        range.setStartAfter(anchor);
        range.collapse(true);
        selection.removeAllRanges();
        selection.addRange(range);

        setRawMessage(editorRef.current.innerHTML);
    };


    const toggleList = (type: "ul" | "ol") => {
        const selection = window.getSelection();
        if (!selection || selection.rangeCount === 0 || !editorRef.current) return;

        const range = selection.getRangeAt(0);
        if (!editorRef.current.contains(range.commonAncestorContainer)) return;

        // Get the HTML of selected content
        const container = document.createElement("div");
        container.appendChild(range.cloneContents());

        const selectedHTML = container.innerHTML.trim();
        if (!selectedHTML) return;

        const lines = selectedHTML
            .split(/<br\s*\/?>|<\/div>|<\/p>/i)
            .map((line) => line.replace(/<[^>]+>/g, "").trim())
            .filter(Boolean);

        const listItems = lines.map((line) => `<li>${line}</li>`).join("");
        const style =
            type === "ul"
                ? ' style="list-style-type: disc; padding-left: 1.5rem;"'
                : ' style="list-style-type: decimal; padding-left: 1.5rem;"';

        const listHTML = `<${type}${style}>${listItems}</${type}>`;

        // Create list element from HTML
        const wrapper = document.createElement("div");
        wrapper.innerHTML = listHTML;

        // Clear original range and insert the list
        range.deleteContents();
        const fragment = document.createDocumentFragment();
        while (wrapper.firstChild) {
            fragment.appendChild(wrapper.firstChild);
        }
        range.insertNode(fragment);

        // Move cursor after list
        range.collapse(false);
        selection.removeAllRanges();
        selection.addRange(range);

        // Sync content
        setRawMessage(editorRef.current.innerHTML);
    };


    // This callback is crucial for capturing the content when the user types
    const handleContentChange = useCallback(() => {
        if (editorRef.current) {
            // Update rawMessage whenever the contentEditable div's innerHTML changes
            setRawMessage(editorRef.current.innerHTML);
        }
    }, []);

    useEffect(() => {
        const checkSelection = () => {
            const selection = window.getSelection();
            const editor = editorRef.current;
            if (!selection || !editor) {
                setHasSelection(false);
                return;
            }

            // Check if selection is within the editor
            let node = selection.anchorNode;
            let insideEditor = false;
            while (node) {
                if (node === editor) {
                    insideEditor = true;
                    break;
                }
                node = node.parentNode;
            }

            setHasSelection(!selection.isCollapsed && insideEditor);
        };

        // Listen to selection changes for enabling/disabling buttons
        document.addEventListener("selectionchange", checkSelection);
        // Also listen to keyup and mouseup for more reliable selection detection
        // when the selection changes but 'selectionchange' might not fire immediately.
        document.addEventListener("keyup", checkSelection);
        document.addEventListener("mouseup", checkSelection);

        return () => {
            document.removeEventListener("selectionchange", checkSelection);
            document.removeEventListener("keyup", checkSelection);
            document.removeEventListener("mouseup", checkSelection);
        };
    }, []);


    useEffect(() => {
        if (!isPreviewMode && editorRef.current) {
            editorRef.current.innerHTML = rawMessage;

            // Move caret to the end after rehydrating
            const range = document.createRange();
            const selection = window.getSelection();
            range.selectNodeContents(editorRef.current);
            range.collapse(false); // false = end of the node
            selection?.removeAllRanges();
            selection?.addRange(range);
        }
    }, [isPreviewMode, rawMessage]);


    const handleSubmit = async () => {
        try {
            const response = await apiClient.post(apiPath, {
                task_title: title,
                task_description: rawMessage, // rawMessage is now the HTML content
                user_id: 1, // Ensure you have a valid user_id or remove if not needed
            });

            console.log(response);
            alert("Task submitted successfully!");

            // Clear the form
            setTitle("");
            setRawMessage(""); // This will also clear the editorRef.current.innerHTML due to useEffect
            if (editorRef.current) {
                editorRef.current.innerHTML = ""; // Explicitly clear in case useEffect hasn't fired yet
            }
        } catch (error: any) {
            console.error(error);
            alert("Error: " + (error.response?.data?.detail || "Failed to submit task"));
        }
    };

    const insertHtmlAtCursor = (html: string, resetStyle: boolean = true) => {
        const selection = window.getSelection();
        if (!selection || !editorRef.current) return;

        editorRef.current.focus();

        let range: Range;
        if (selection.rangeCount === 0 || !editorRef.current.contains(selection.getRangeAt(0).commonAncestorContainer)) {
            range = document.createRange();
            range.selectNodeContents(editorRef.current);
            range.collapse(false);
        } else {
            range = selection.getRangeAt(0);
        }

        range.deleteContents();

        const fragment = range.createContextualFragment(html);
        let lastNode = fragment.lastChild;
        range.insertNode(fragment);

        // 🧼 Insert a span with "all: unset" to reset inherited styles
        if (resetStyle) {
            const resetSpan = document.createElement("span");
            resetSpan.innerHTML = "\u200B"; // Zero-width space
            resetSpan.style.all = "unset";
            range.setStartAfter(lastNode as Node);
            range.insertNode(resetSpan);
            range.setStartAfter(resetSpan);
        } else {
            range.setStartAfter(lastNode as Node);
        }

        range.collapse(true);
        selection.removeAllRanges();
        selection.addRange(range);

        setRawMessage(editorRef.current.innerHTML);
    };

    const applyFontSize = (pxSize: number) => {
        const selection = window.getSelection();
        if (!selection || selection.rangeCount === 0 || !editorRef.current) return;

        const range = selection.getRangeAt(0);
        if (!editorRef.current.contains(range.commonAncestorContainer)) return;

        const selectedText = range.extractContents();
        const span = document.createElement("span");
        span.style.fontSize = `${pxSize}px`;
        span.appendChild(selectedText);

        range.insertNode(span);

        // Move cursor after the inserted span
        range.setStartAfter(span);
        range.collapse(true);
        selection.removeAllRanges();
        selection.addRange(range);

        // Sync with state
        setRawMessage(editorRef.current.innerHTML);
    };

    return (
        <div className="h-screen p-10 flex flex-col text-xl gap-5">
            <div className="flex flex-col gap-3 w-full mx-auto flex-1">

                {!isPreviewMode && (
                    <FloatingInput
                        id="title"
                        label="Title"
                        err=""
                        value={title}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                            setTitle(e.target.value)
                        }
                    />
                )}

                <div className="flex justify-between mt-4 gap-5">
                    {!isPreviewMode && (
                        <div className="flex items-center gap-2 flex-wrap">
                            <Tooltipcomp
                                tip="Bold"
                                content={
                                    <ImageBtn
                                        onClick={handleBold}
                                        icon="bold"
                                        disabled={!hasSelection}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                    />
                                }
                            />

                            <Tooltipcomp
                                tip={"Italic"}
                                content={
                                    <ImageBtn
                                        onClick={handleItalic}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                        disabled={!hasSelection}
                                        icon={"italic"}
                                    />
                                }
                            />
                            <Tooltipcomp
                                tip={"Underline"}
                                content={
                                    <ImageBtn
                                        onClick={handleUnderline}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                        disabled={!hasSelection}
                                        icon={"underline"}
                                    />
                                }
                            />

                            <Tooltipcomp
                                tip={"Uppercase"}
                                content={
                                    <ImageBtn
                                        onClick={handleUppercase}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                        disabled={!hasSelection}
                                        icon={"uppercase"}
                                    />
                                }
                            />

                            <Tooltipcomp
                                tip={"Lowercase"}
                                content={
                                    <ImageBtn
                                        onClick={handleLowercase}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                        disabled={!hasSelection}
                                        icon={"lowercase"}
                                    />
                                }
                            />


                            <Tooltipcomp
                                tip={"text color"}
                                content={
                                    <input
                                        type="color"
                                        value={textColor}
                                        onInput={handleTextColorInput}
                                        className="w-6"
                                        disabled={!hasSelection}
                                    />
                                }
                            />
                            <Tooltipcomp
                                tip={"bg color"}
                                content={
                                    <input
                                        type="color"
                                        value={bgColor}
                                        onInput={handleBgColorInput}
                                        className="w-6"
                                        disabled={!hasSelection}
                                    />
                                }
                            />
                            <select
                                onChange={(e) => {
                                    const size = parseInt(e.target.value);
                                    if (!isNaN(size)) {
                                        applyFontSize(size);
                                        editorRef.current?.focus();
                                    }
                                }}
                                defaultValue=""
                                className={`text-sm border rounded-md px-2 py-1 bg-white ${!hasSelection ? "opacity-30 pointer-events-none" : ""}`}
                                disabled={!hasSelection}
                            >
                                <option value="" disabled>
                                    Size
                                </option>
                                <option value="8">8</option>
                                <option value="12">12</option>
                                <option value="16">16</option>
                                <option value="20">20</option>
                                <option value="24">24</option>
                                <option value="28">28</option>
                                <option value="36">36</option>
                                <option value="48">48</option>
                                <option value="72">72</option>
                            </select>


                            <Tooltipcomp
                                tip={"Align Left"}
                                content={
                                    <ImageBtn
                                        onClick={() => applyFormatting("justifyLeft")}
                                        icon={"alignleft"}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                        disabled={!hasSelection}
                                    />
                                }
                            />
                            <Tooltipcomp
                                tip={"Align Center"}
                                content={
                                    <ImageBtn
                                        onClick={() => applyFormatting("justifyCenter")}
                                        icon={"aligncenter"}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                        disabled={!hasSelection}
                                    />
                                }
                            />
                            <Tooltipcomp
                                tip={"Align Right"}
                                content={
                                    <ImageBtn
                                        onClick={() => applyFormatting("justifyRight")}
                                        icon={"alignright"}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                        disabled={!hasSelection}
                                    />
                                }
                            />
                            <Tooltipcomp
                                tip={"Align Justify"}
                                content={
                                    <ImageBtn
                                        onClick={() => applyFormatting("justifyFull")}
                                        icon={"alignjustify"}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                        disabled={!hasSelection}
                                    />
                                }
                            />
                            <Tooltipcomp
                                tip={"External Link"}
                                content={
                                    <ImageBtn
                                        onClick={applyLinkToSelection}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                        icon={"link"}
                                        disabled={!hasSelection}
                                    />
                                }
                            />

                            <Tooltipcomp
                                tip={"Bullet List"}
                                content={
                                    <ImageBtn
                                        onClick={() => toggleList("ul")}
                                        icon={"listul"}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                        disabled={!hasSelection}
                                    />
                                }
                            />

                            <Tooltipcomp
                                tip={"Numbered List"}
                                content={
                                    <ImageBtn
                                        onClick={() => toggleList("ol")}
                                        icon={"listol"}
                                        className={`p-2 bg-gray-200 hover:bg-gray-300 rounded-md ${
                                            !hasSelection ? "opacity-50 pointer-events-none" : ""
                                        }`}
                                        disabled={!hasSelection}
                                    />
                                }
                            />
                        </div>
                    )}

                    {isPreviewMode && (
                        <div></div>
                    )}

                    <div className="flex gap-4 flex-wrap">
                        <ImageBtn
                            icon="edit"
                            label="Write"
                            onClick={() => setIsPreviewMode(false)}
                            className={`px-4 p-1 text-sm font-medium transition-colors ${
                                !isPreviewMode
                                    ? "bg-black text-white"
                                    : "bg-white text-black hover:bg-gray-100"
                            }`}
                        />
                        <ImageBtn
                            icon="view"
                            label="Preview"
                            onClick={() => setIsPreviewMode(true)}
                            className={`px-4 p-1 text-sm font-medium transition-colors ${
                                isPreviewMode
                                    ? "bg-black text-white"
                                    : "bg-white text-black hover:bg-gray-100"
                            }`}
                        />
                    </div>
                </div>

                {!isPreviewMode && (
                    <div
                        ref={editorRef} // This ref should now correctly point to the div
                        contentEditable="true"
                        onInput={handleContentChange} // Listen for content changes
                        className="min-h-[300px] p-3 border border-ring/30 rounded overflow-auto focus:outline-none"
                        style={{whiteSpace: 'pre-wrap'}}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" && !e.shiftKey) {
                                e.preventDefault();
                                insertHtmlAtCursor("<br>"); // Shift+Enter = soft line break
                            } else if (e.key === "Enter" && e.shiftKey) {
                                e.preventDefault();
                                insertHtmlAtCursor("<br><br>");  // Single line break, then move to next line
                            }
                        }}


                    />
                )}
                {isPreviewMode && (
                    <div className="mt-6">
                        <h2 className="font-bold mb-2">Preview:</h2>
                        <div
                            className="p-4 border border-ring/30 rounded bg-gray-50 prose prose-sm max-w-none"
                            dangerouslySetInnerHTML={{__html: rawMessage}}
                        ></div>
                    </div>
                )}

                <Button
                    label={"Submit"}
                    onClick={handleSubmit}
                    className="border border-ring/40 w-max ml-auto bg-green-500 text-white rounded-md"
                />
            </div>
        </div>
    );
}