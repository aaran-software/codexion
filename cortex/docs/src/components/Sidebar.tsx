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
  const [openItems, setOpenItems] = useState<Record<string, boolean>>({});

  useEffect(() => {
    fetch("http://localhost:5001/api/docs")
      .then(res => res.json())
      .then((data: DocItem[]) => {
        const sortTree = (items: DocItem[]): DocItem[] =>
          items
            .sort((a, b) => a.order - b.order)
            .map(item => ({
              ...item,
              children: item.children ? sortTree(item.children) : []
            }));
        setDocs(sortTree(data));
      });
  }, []);

  const toggleOpen = (slug: string) => {
    setOpenItems(prev => ({ ...prev, [slug]: !prev[slug] }));
  };

  const renderDocs = (items: DocItem[], parentPath = "", level = 0) => {
    return (
      <ul className="space-y-1">
        {items.map(item => {
          const hasChildren = item.children && item.children.length > 0;
          const fullPath = parentPath ? `${parentPath}/${item.slug}` : item.slug;
          const isOpen = openItems[fullPath] ?? false; // collapsed by default

          return (
            <li key={fullPath} className={`ml-${level * 4}`}>
              <div className="flex items-center space-x-1">
                {hasChildren && (
                  <button
                    onClick={() => toggleOpen(fullPath)}
                    className="text-sm focus:outline-none hover:text-blue-500 cursor-pointer"
                  >
                    {isOpen ? "▼" : "▶"}
                  </button>
                )}
                <button
                  onClick={() => {
                    if (hasChildren && !isOpen) {
                      toggleOpen(fullPath); // expand first click
                    }
                    onSelect(fullPath);
                  }}
                  className="text-left text-gray-700 hover:text-blue-600 focus:outline-none truncate cursor-pointer"
                >
                  {item.desc}
                </button>
              </div>

              {hasChildren && isOpen && renderDocs(item.children!, fullPath, level + 1)}
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
