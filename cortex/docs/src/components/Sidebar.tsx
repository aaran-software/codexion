import { useEffect, useState } from "react";

interface DocItem {
  slug: string;
  order: number;
  desc: string;
  children?: DocItem[];
  parentSlug?: string; // added to build full path
}

interface SidebarProps {
  onSelect: (slug: string) => void;
}

export default function Sidebar({ onSelect }: SidebarProps) {
  const [docs, setDocs] = useState<DocItem[]>([]);
  const [openItems, setOpenItems] = useState<Record<string, boolean>>({});

  useEffect(() => {
    fetch("http://localhost:5001/api/docs")
      .then(res => res.json())
      .then((data: DocItem[]) => {
        const sortTree = (items: DocItem[], parentSlug = ""): DocItem[] =>
          items
            .sort((a, b) => a.order - b.order)
            .map(item => {
              const fullSlug = parentSlug ? `${parentSlug}/${item.slug}` : item.slug;
              return {
                ...item,
                slug: fullSlug,
                children: item.children ? sortTree(item.children, fullSlug) : [],
              };
            });
        setDocs(sortTree(data));
      });
  }, []);

  const toggleOpen = (slug: string) => {
    setOpenItems(prev => ({ ...prev, [slug]: !prev[slug] }));
  };

  const renderDocs = (items: DocItem[], level = 0) => {
    return (
      <ul className="space-y-1">
        {items.map(item => {
          const hasChildren = item.children && item.children.length > 0;
          const isOpen = openItems[item.slug] ?? false;

          return (
            <li key={item.slug} className={`ml-${level * 4}`}>
              <div className="flex items-center space-x-1 group">
                {hasChildren && (
                  <button
                    onClick={() => toggleOpen(item.slug)}
                    className="text-sm focus:outline-none transition-transform duration-200 group-hover:text-blue-600"
                  >
                    {isOpen ? "▼" : "▶"}
                  </button>
                )}
                <button
                  onClick={() => onSelect(item.slug)}
                  className="text-left text-gray-700 hover:bg-gray-200 rounded px-2 py-1 transition-all duration-200 w-full text-sm"
                >
                  {item.desc}
                </button>
              </div>
              {hasChildren && isOpen && renderDocs(item.children!, level + 1)}
            </li>
          );
        })}
      </ul>
    );
  };

  return (
    <aside className="w-64 border-r border-gray-300 overflow-y-auto h-screen p-4 bg-gray-50">
      <h3 className="text-lg font-semibold mb-2">Docs</h3>
      {renderDocs(docs)}
    </aside>
  );
}
