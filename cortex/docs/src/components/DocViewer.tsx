import { useEffect, useState } from "react";

interface DocResponse {
  slug: string;
  content: string;
}

interface DocViewerProps {
  slug: string | null;
}

export default function DocViewer({ slug }: DocViewerProps) {
  const [content, setContent] = useState<string>("");

  useEffect(() => {
    if (!slug) return;
    fetch(`http://localhost:5001/api/docs/${slug}`)
      .then(res => res.json())
      .then((data: DocResponse) => setContent(data.content));
  }, [slug]);

  return (
    <div style={{ padding: "1rem" }} dangerouslySetInnerHTML={{ __html: content }} />
  );
}
