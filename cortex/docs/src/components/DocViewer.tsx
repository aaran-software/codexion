import { useEffect, useState } from "react";
import ReactMarkdown, { Components, CodeProps } from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { materialLight } from "react-syntax-highlighter/dist/esm/styles/prism";

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

  // Use the correct CodeProps type
  const markdownComponents: Components = {
    code({ node, inline, className, children, ...props }: CodeProps) {
      const match = /language-(\w+)/.exec(className || "");
      return !inline && match ? (
        <SyntaxHighlighter
          style={materialLight}
          language={match[1]}
          PreTag="div"
          {...props}
        >
          {String(children).replace(/\n$/, "")}
        </SyntaxHighlighter>
      ) : (
        <code
          className="bg-gray-100 rounded px-1 py-0.5 text-sm"
          {...props}
        >
          {children}
        </code>
      );
    },
    a({ href, children, ...props }) {
      return (
        <a
          href={href}
          className="text-blue-600 hover:underline"
          target="_blank"
          rel="noopener noreferrer"
          {...props}
        >
          {children}
        </a>
      );
    },
  };

  return (
    <div className="flex-1 overflow-y-auto bg-white p-6">
      {!slug && <p className="text-gray-500">Select a document to view.</p>}
      {slug && (
        <>
          <Breadcrumb slug={slug} />
          <div className="prose prose-sm sm:prose lg:prose-lg max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
              {content}
            </ReactMarkdown>
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
