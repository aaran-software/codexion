import FloatingInput from "../../resources/components/input/FloatingInput";
import Button from "../../resources/components/button/Button";
import React, {useState, useRef, useEffect} from "react";
import ImageBtn from "../components/button/ImageBtn";
import Tooltipcomp from "../components/Tooltip/tooltipcomp";
import apiClient from "../../resources/global/api/apiClients";


export default function Editor({apiPath}: { apiPath: string }) {
    const [title, setTitle] = useState("");
    const [rawMessage, setRawMessage] = useState("");
    const [formattedMessage, setFormattedMessage] = useState("");
    const textAreaRef = useRef<HTMLTextAreaElement>(null);
    const selectionStartRef = useRef<number | null>(null);
    const selectionEndRef = useRef<number | null>(null);
    const [fontSizeInput, setFontSizeInput] = useState("");
    const inputRef = useRef<HTMLInputElement>(null);
    const handleBold = () => styleSelectedText("font-weight: bold");
    const handleItalic = () => styleSelectedText("font-style: italic");
    const handleUnderline = () => styleSelectedText("text-decoration: underline");
    const [isPreviewMode, setIsPreviewMode] = useState(false);
    const [hasSelection, setHasSelection] = useState(false);
    const isFormattingInputClick = useRef(false);

    function styleSelectedText(newStyle: string) {
        if (!textAreaRef.current) return;

        const textarea = textAreaRef.current;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;

        if (start === end) return;

        const before = rawMessage.slice(0, start);
        const selectedRaw = rawMessage.slice(start, end);
        const after = rawMessage.slice(end);

        // Step 1: Remove any surrounding span and inline styles
        let content = selectedRaw
            .replace(/<\/?(b|strong|i|u)>/gi, "")
            .replace(/<span style="[^"]*">/gi, "")
            .replace(/<\/span>/gi, "")
            .trim();

        // Step 2: Extract existing inline styles
        const styleMap: Record<string, string> = {};
        const styleMatch = selectedRaw.match(/<span style="([^"]*)">/i);

        if (styleMatch) {
            const styleString = styleMatch[1];
            styleString.split(";").forEach((pair) => {
                const [key, value] = pair.split(":").map((s) => s.trim());
                if (key && value) styleMap[key] = value;
            });
        }

        // Step 3: Toggle the new style
        const [newKey, newValue] = newStyle.split(":").map((s) => s.trim());

        if (styleMap[newKey] === newValue) {
            delete styleMap[newKey]; // Toggle OFF
        } else {
            styleMap[newKey] = newValue; // Toggle ON
        }

        // Step 4: Compose updated style string
        const mergedStyle = Object.entries(styleMap)
            .map(([k, v]) => `${k}: ${v}`)
            .join("; ");

        const wrapped = `<span style="${mergedStyle}">${content}</span>`;
        const updated = before + wrapped + after;

        setRawMessage(updated);
        setFormattedMessage(updated);

        // Restore focus and selection
        textarea.focus();
        textarea.setSelectionRange(start, start + wrapped.length);
    }


    const [textColor, setTextColor] = useState("#000000");
    const [bgColor, setBgColor] = useState("#ffffff");
    const selectionRef = useRef<Range | null>(null);

    const saveSelection = () => {
        const selection = window.getSelection();
        if (selection && selection.rangeCount > 0) {
            selectionRef.current = selection.getRangeAt(0).cloneRange();
        }
    };
    const restoreSelection = () => {
        const selection = window.getSelection();
        if (selection && selectionRef.current) {
            selection.removeAllRanges();
            selection.addRange(selectionRef.current);
        }
    };

    const handleTextColorInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        const color = e.target.value;
        setTextColor(color);
        restoreSelection(); // <-- important
        styleSelectedText(`color: ${color}`);
    };

    const handleBgColorInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        const color = e.target.value;
        setBgColor(color);
        restoreSelection(); // <-- important
        styleSelectedText(`background-color: ${color}`);
    };

    useEffect(() => {
        const handleSelectionChange = () => {
            const textarea = textAreaRef.current;
            if (!textarea) return;

            const selectionStart = textarea.selectionStart;
            const selectionEnd = textarea.selectionEnd;

            selectionStartRef.current = selectionStart;
            selectionEndRef.current = selectionEnd;

            // 🛑 Prevent clearing selection if input is clicked
            if (!isFormattingInputClick.current) {
                setHasSelection(selectionStart !== selectionEnd);
            }

            // reset the flag
            isFormattingInputClick.current = false;
        };


        document.addEventListener("selectionchange", handleSelectionChange);
        return () =>
            document.removeEventListener("selectionchange", handleSelectionChange);
    }, []);

    useEffect(() => {
        const checkSelection = () => {
            const selection = window.getSelection();
            const text = selection?.toString();
            setHasSelection(!!text);
        };

        document.addEventListener("mouseup", checkSelection);
        document.addEventListener("keyup", checkSelection);

        return () => {
            document.removeEventListener("mouseup", checkSelection);
            document.removeEventListener("keyup", checkSelection);
        };
    }, []);


    // const [message] = useState([
    //     {
    //         date: "2025-07-22T09:30:00Z",
    //         title: "New Comment on Task",
    //         description: "Alice commented on the task 'Design Review'.",
    //         user: {
    //             name: "Alice Johnson",
    //             avatar: "/avatars/alice.png",
    //         },
    //         icon: <i className="text-blue-500 ri-message-3-line"/>,
    //     },
    //     // ... (keep the rest as-is)
    // ]);

    const saveTextareaSelection = () => {
        const textarea = textAreaRef.current;
        if (textarea) {
            selectionStartRef.current = textarea.selectionStart;
            selectionEndRef.current = textarea.selectionEnd;
        }
    };

    const applyLinkToSelection = () => {
        const url = prompt("Enter the URL:");
        if (!url || !textAreaRef.current) return;

        const textarea = textAreaRef.current;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;

        if (start === end) return;

        const before = rawMessage.slice(0, start);
        const selected = rawMessage.slice(start, end);
        const after = rawMessage.slice(end);

        const clean = selected.replace(/<a [^>]*>|<\/a>/gi, "");

        const wrapped = `<a href="${url}" target="_blank" rel="noopener noreferrer" style="color: blue; text-decoration: underline; cursor: pointer;">${clean}</a>`;

        const updated = before + wrapped + after;

        setRawMessage(updated);
        setFormattedMessage(updated);

        textarea.focus();
        textarea.setSelectionRange(start, start + wrapped.length);
    };

    function toggleList(type: "ul" | "ol") {
        const textarea = textAreaRef.current;
        if (!textarea) return;

        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;

        const before = rawMessage.slice(0, start);
        const selected = rawMessage.slice(start, end);
        const after = rawMessage.slice(end);

        const lines = selected.split("\n").map((line) => line.trim());

        const isAlreadyList =
            selected.trim().startsWith(`<${type}`) &&
            selected.trim().endsWith(`</${type}>`);

        let wrapped;
        if (isAlreadyList) {
            // Remove list tags and <li> elements
            wrapped = selected
                .replace(new RegExp(`<${type}[^>]*>`, "g"), "")
                .replace(new RegExp(`</${type}>`, "g"), "")
                .replace(/<li>/g, "")
                .replace(/<\/li>/g, "")
                .trim();
        } else {
            const style =
                type === "ul"
                    ? ' style="list-style-type: disc; padding-left: 1.5rem;"'
                    : ' style="list-style-type: decimal; padding-left: 1.5rem;"';
            const listItems = lines.map((line) => `<li>${line}</li>`).join("\n");
            wrapped = `<${type}${style}>\n${listItems}\n</${type}>`;
        }

        const updated = before + wrapped + after;
        setRawMessage(updated);
        setFormattedMessage(updated);

        setTimeout(() => {
            textarea.focus();
            textarea.setSelectionRange(start, start + wrapped.length);
        }, 0);
    }


    const handleSubmit = async () => {
        try {
            const response = await apiClient.post(apiPath, {
                task_title: title,
                task_description: formattedMessage,
                user_id: 1,
            });

            console.log(response)
            alert("Task submitted successfully!");

            // Clear the form
            setTitle("");
            setRawMessage("");
            setFormattedMessage("");
        } catch (error: any) {
            console.error(error);
            alert("Error: " + (error.response?.data?.detail || "Failed to submit task"));
        }
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
                                        onClick={() => styleSelectedText("text-transform: uppercase")}
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
                                        onClick={() => styleSelectedText("text-transform: lowercase")}
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
                                        onMouseDown={saveSelection}
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
                                        onMouseDown={saveSelection}
                                        onInput={handleBgColorInput}
                                        className="w-6"
                                        disabled={!hasSelection}
                                    />
                                }
                            />
                            <input
                                ref={inputRef}
                                type="number"
                                placeholder="8"
                                min={8}
                                max={72}
                                value={fontSizeInput}
                                onMouseDown={() => {
                                    isFormattingInputClick.current = true;
                                    saveTextareaSelection();
                                }}
                                onFocus={() => {
                                    saveTextareaSelection();
                                }}
                                onBlur={() => {
                                    const size = parseInt(fontSizeInput.trim());
                                    if (!size || isNaN(size)) return;

                                    styleSelectedText(`font-size: ${size}px`);
                                    setFontSizeInput("");

                                    // Restore focus to textarea after applying
                                    setTimeout(() => {
                                        textAreaRef.current?.focus();
                                    }, 50);
                                }}
                                onKeyDown={(e) => {
                                    if (e.key === "Enter") {
                                        e.preventDefault();
                                        const size = parseInt(fontSizeInput.trim());
                                        if (!size || isNaN(size)) return;

                                        styleSelectedText(`font-size: ${size}px`);
                                        setFontSizeInput("");

                                        // Restore focus to textarea after applying
                                        setTimeout(() => {
                                            textAreaRef.current?.focus();
                                        }, 50);
                                    }
                                }}
                                onChange={(e) => setFontSizeInput(e.target.value)}
                                className="w-16 text-md border rounded-md px-2"
                            />

                            <Tooltipcomp
                                tip={"Align Left"}
                                content={
                                    <ImageBtn
                                        onClick={() => styleSelectedText("text-align: left")}
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
                                        onClick={() => styleSelectedText("text-align: center")}
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
                                        onClick={() => styleSelectedText("text-align: right")}
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
                                        onClick={() => styleSelectedText("text-align: justify")}
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
                            label="Edit"
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
                    <textarea
                        ref={textAreaRef}
                        value={rawMessage}
                        onSelect={(e) => {
                            selectionStartRef.current = e.currentTarget.selectionStart;
                            selectionEndRef.current = e.currentTarget.selectionEnd;
                        }}
                        onMouseDown={saveTextareaSelection}
                        onChange={(e) => {
                            setRawMessage(e.target.value);
                            setFormattedMessage(e.target.value);
                        }}
                        onKeyDown={(e) => {
                            if (e.key === "Enter") {
                                e.preventDefault();
                                const textarea = textAreaRef.current;
                                if (!textarea) return;

                                const start = textarea.selectionStart;
                                const end = textarea.selectionEnd;

                                const before = rawMessage.slice(0, start);
                                const after = rawMessage.slice(end);
                                const updated = `${before}<br>${after}`;

                                setRawMessage(updated);
                                setFormattedMessage(updated);

                                // move cursor after <br>
                                setTimeout(() => {
                                    textarea.focus();
                                    textarea.setSelectionRange(start + 4, start + 4);
                                }, 0);
                            }
                        }}

                        placeholder="Write your message here..."
                        className="flex-1 min-h-[300px] p-3 border border-ring/30 rounded"
                    />
                )}
                {isPreviewMode && (
                    <div className="mt-6">
                        <h2 className="font-bold mb-2">Preview:</h2>
                        <div
                            className="p-4 border border-ring/30 rounded bg-gray-50 prose prose-sm max-w-none"
                            dangerouslySetInnerHTML={{__html: formattedMessage}}
                        ></div>
                    </div>
                )}

                <Button
                    label={"Submit"}
                    onClick={handleSubmit}
                    className="border border-ring/40 w-max ml-auto bg-green-500 text-white rounded-md"
                />
            </div>

            <div>
                {/* show message with timeline */}
                {/*<div className="w-full mt-10">*/}
                {/*    <NotificationCard items={message}/>*/}
                {/*</div>*/}

                {/* reply section */}
                {/*<div className="flex flex-col mt-5 gap-5 pb-20">*/}
                {/*    <FloatingInput id={"title"} label={"reply"} err={""}/>*/}
                {/*    <Button*/}
                {/*        label={"Reply"}*/}
                {/*        className="border border-ring/40 w-max ml-auto bg-update text-white rounded-md"*/}
                {/*    />*/}
                {/*</div>*/}
            </div>
        </div>
    );
}
