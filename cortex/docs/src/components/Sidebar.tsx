import { useEffect, useState } from "react";

interface DocItem {
  slug: string;
  desc: string;
  order: number;
  tag?: string;
}

interface SidebarProps {
  onSelect: (slug: string) => void;
}

export default function Sidebar({ onSelect }: SidebarProps) {
  const [docs, setDocs] = useState<DocItem[]>([]);

  useEffect(() => {
    fetch("http://localhost:5001/api/docs")
      .then(res => res.json())
      .then((data: DocItem[]) => setDocs(data));
  }, []);

  return (
    <aside style={{ width: "250px", borderRight: "1px solid #ccc" }}>
      <h3>Docs</h3>
      <ul>
        {docs.map(item => (
          <li key={item.slug}>
            <button onClick={() => onSelect(item.slug)}>{item.desc}</button>
          </li>
        ))}
      </ul>
    </aside>
  );
}
