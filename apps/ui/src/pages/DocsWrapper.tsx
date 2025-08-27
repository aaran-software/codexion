// components/blocks/BlockWrapper.tsx
import React from "react";

type PropDoc = {
  name: string;
  description: string;
};

type DocsWrapperProps = {
  title: string;
  propDocs: PropDoc[];
  paths: {
    file: string;
    usedIn: string[];
    reusableIn: string[];
  };
  children: React.ReactNode; // the actual component demo
};

const DocsWrapper: React.FC<DocsWrapperProps> = ({
  title,
  propDocs,
  paths,
  children,
}) => {
  return (
    <div className="space-y-8">
      {/* Docs Section */}
      <div className="p-6 bg-gray-900 rounded-xl text-white">
        <h2 className="text-2xl font-bold mb-4">{title} Props</h2>
        <ul className="space-y-2 text-gray-300">
          {propDocs.map((p) => (
            <li key={p.name}>
              <strong>{p.name}</strong> → {p.description}
            </li>
          ))}
        </ul>

        <div className="mt-6 text-sm text-gray-400 space-y-1">
          <p>Path: <code>{paths.file}</code></p>
          <p>Used in: {paths.usedIn.map((u, i) => (
            <code key={i} className="mr-2">{u}</code>
          ))}</p>
          <p>Reusable in: {paths.reusableIn.join(", ")}</p>
        </div>
      </div>

      {/* Demo Preview */}
      <div>{children}</div>
    </div>
  );
};

export default DocsWrapper;
