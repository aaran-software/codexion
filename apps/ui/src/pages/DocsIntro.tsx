import React from "react";

const DocsIntro: React.FC = () => {
  return (
    <div className="px-[10%] py-16">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold mb-6">
          📘 Project Documentation
        </h1>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          Welcome to the documentation hub. This site provides everything you need 
          to understand and use our <strong>Components</strong>, <strong>Layouts</strong>, 
          and <strong>Design Blocks</strong>.  
          Each section includes code usage and a live preview to help you integrate faster.
        </p>
      </div>

      {/* Quick Sections Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
        <div className="p-6 border rounded-2xl shadow-sm hover:shadow-md transition">
          <h2 className="text-2xl font-semibold mb-2">⚛️ Components</h2>
          <p className="text-gray-600 mb-4">
            Explore reusable UI components like buttons, cards, inputs, and more.
          </p>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            View Components →
          </button>
        </div>

        <div className="p-6 border rounded-2xl shadow-sm hover:shadow-md transition">
          <h2 className="text-2xl font-semibold mb-2">📐 Layouts</h2>
          <p className="text-gray-600 mb-4">
            Predefined layouts for dashboards, landing pages, and grids.
          </p>
          <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
            View Layouts →
          </button>
        </div>

        <div className="p-6 border rounded-2xl shadow-sm hover:shadow-md transition">
          <h2 className="text-2xl font-semibold mb-2">🎨 Design Blocks</h2>
          <p className="text-gray-600 mb-4">
            Ready-to-use blocks like pricing sections, testimonials, and headers.
          </p>
          <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
            View Blocks →
          </button>
        </div>
      </div>

      {/* Getting Started */}
      <div className="mt-20 text-center">
        <h2 className="text-3xl font-bold mb-4">🚀 Getting Started</h2>
        <p className="text-gray-600 mb-6">
          Install and start using components with just a few lines of code:
        </p>
        <pre className="bg-gray-900 text-green-400 p-6 rounded-lg text-sm max-w-2xl mx-auto text-left">
{`npm install your-design-system

import { Button } from "your-design-system";

export default function App() {
  return <Button variant="primary">Click Me</Button>;
}`}
        </pre>
      </div>
    </div>
  );
};

export default DocsIntro;
