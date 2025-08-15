import { useEffect, useState } from "react";

interface DocItem {
  slug: string;
  order: number;
  desc: string;
  tags?: string[];
  children?: DocItem[];
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

  const renderDocs = (items: DocItem[], level = 0) => {
    return (
      <ul style={{ paddingLeft: level * 15 }}>
        {items.map(item => (
          <li key={item.slug}>
            <button onClick={() => onSelect(item.slug)}>{item.desc}</button>
            {item.children && item.children.length > 0 && renderDocs(item.children, level + 1)}
          </li>
        ))}
      </ul>
    );
  };

  return (
    <aside style={{ width: "250px", borderRight: "1px solid #ccc", overflowY: "auto" }}>
      <h3>Docs</h3>
      {renderDocs(docs)}
    </aside>
  );
}
