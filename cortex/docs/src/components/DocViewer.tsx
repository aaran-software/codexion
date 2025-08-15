import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm"; // GitHub-style tables, strikethrough, etc.

interface DocViewerProps {
    slug: string | null;
}

export default function DocViewer({ slug }: DocViewerProps) {
    const [content, setContent] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        if (!slug) {
            setContent("");
            return;
        }

        setLoading(true);
        fetch(`http://localhost:5001/api/docs/${slug}`)
            .then(res => res.json())
            .then(data => setContent(data.content))
            .catch(() => setContent("Failed to load document."))
            .finally(() => setLoading(false));
    }, [slug]);

    return (
        <div className="flex-1 p-6 overflow-y-auto bg-white">
            {!slug && (
                <p className="text-gray-500 italic">Select a document to view.</p>
            )}

            {slug && loading && (
                <p className="text-gray-400 italic">Loading...</p>
            )}

            {slug && !loading && (
                <div className="prose prose-sm sm:prose lg:prose-lg max-w-none">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {content}
                    </ReactMarkdown>
                </div>
            )}
        </div>
    );
}
