import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface DocViewerProps {
  slug: string | null;
}

export default function DocViewer({ slug }: DocViewerProps) {
  const [content, setContent] = useState<string>("");

  useEffect(() => {
    if (!slug) {
      setContent("");
      return;
    }

    fetch(`http://localhost:5001/api/docs/${slug}`)
      .then(res => res.json())
      .then(data => setContent(data.content))
      .catch(() => setContent("Failed to load document."));
  }, [slug]);

  return (
    <div className="flex-1 overflow-y-auto bg-white p-6">
      {!slug && <p className="text-gray-500">Select a document to view.</p>}
      {slug && (
        <>
          <Breadcrumb slug={slug} />
          <div className="prose prose-sm sm:prose lg:prose-lg max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
          </div>
        </>
      )}
    </div>
  );
}

// Breadcrumb component
interface BreadcrumbProps {
  slug: string;
}

function Breadcrumb({ slug }: BreadcrumbProps) {
  const parts = slug.split("/");

  return (
    <nav className="text-sm text-gray-500 mb-4" aria-label="Breadcrumb">
      {parts.map((part, idx) => {
        const path = parts.slice(0, idx + 1).join("/");
        const isLast = idx === parts.length - 1;
        return (
          <span key={path}>
            {!isLast ? (
              <>
                <button
                  onClick={() => {
                    document.getElementById(path)?.scrollIntoView({ behavior: "smooth" });
                  }}
                  className="hover:underline focus:outline-none"
                >
                  {part}
                </button>
                {" / "}
              </>
            ) : (
              <span className="font-semibold">{part}</span>
            )}
          </span>
        );
      })}
    </nav>
  );
}
