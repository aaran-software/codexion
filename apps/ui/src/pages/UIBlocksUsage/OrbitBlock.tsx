import React from "react";
import DocsWrapper from "../DocsWrapper";
import HalfOrbit from "../../../../../resources/UIBlocks/Orbit/HalfOrbit";
import Orbit from "../../../../../resources/UIBlocks/Orbit/Orbit";
function OrbitBlock() {
  return (
    <div className="flex flex-col gap-20">
      <DocsWrapper
        title="HeaderPortfolio - HalfOrbit"
        propDocs={[
          {
            name: "centerImage",
            description:
              "The image displayed at the center of the orbit (e.g. React logo).",
          },
          {
            name: "items",
            description:
              "Array of objects with `name` and `icon` (string). Each item represents a technology to orbit around the center image.",
          },
          {
            name: "radius?",
            description:
              "Optional — distance of orbit items from the center. Default is 220.",
          },
          {
            name: "size?",
            description:
              "Optional — total size of the orbit container. Default is 500.",
          },
          {
            name: "arcAngle?",
            description:
              "Optional — arc coverage of the orbit in radians. `Math.PI` creates a half circle. Default is Math.PI.",
          },
          {
            name: "autoRotateSpeed?",
            description:
              "Optional — speed of continuous auto-rotation. Default is 0.1.",
          },
          {
            name: "title",
            description:
              "Heading displayed below the center image (e.g. TECH STACK).",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/orbit/HalfOrbit",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <HalfOrbit
          centerImage="/assets/tech/react.png"
          items={[
            { name: "React", icon: "/assets/tech/react.png" },
            { name: "Node.js", icon: "/assets/tech/react.png" },
            { name: "Python", icon: "/assets/tech/react.png" },
            { name: "JavaScript", icon: "/assets/tech/react.png" },
            { name: "Tailwind", icon: "/assets/tech/react.png" },
            { name: "Frappe", icon: "/assets/tech/react.png" },
            { name: "TypeScript", icon: "/assets/tech/react.png" },
          ]}
          arcAngle={Math.PI / 1.0}
          title="TECH STACK"
        />
      </DocsWrapper>

      <DocsWrapper
        title="HeaderPortfolio - Orbit"
        propDocs={[
          {
            name: "centerImage",
            description:
              "The image displayed at the center of the orbit (e.g., a React logo).",
          },
          {
            name: "items",
            description:
              "Array of objects with `title` and `description` (both strings). Each item will be displayed evenly spaced around the orbit.",
          },
          {
            name: "radius?",
            description:
              "Optional — distance of orbit items from the center. Default is 220.",
          },
          {
            name: "size?",
            description:
              "Optional — total size of the orbit container (width/height). Default is 500.",
          },
          {
            name: "autoRotateSpeed?",
            description:
              "Optional — controls the speed of continuous rotation of the orbit. Lower values rotate slower. Default is 0.05.",
          },
          // {
          //   name: "title",
          //   description:
          //     "Optional — heading displayed below the center image. Currently commented out in this version.",
          // },
        ]}
        paths={{
          file: "/resources/UIBlocks/orbit/Orbit",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div className="py-10">
          <Orbit
            centerImage="/assets/process.webp"
            items={[
              { title: "React", description: "A JavaScript library for UI" },
              {
                title: "Node.js",
                description: "Server-side JavaScript runtime",
              },
              {
                title: "Python",
                description: "High-level programming language",
              },
              {
                title: "JavaScript",
                description: "Web’s core scripting language",
              },
              { title: "Tailwind", description: "Utility-first CSS framework" },
              { title: "Frappe", description: "Full-stack web framework" },
              {
                title: "TypeScript",
                description: "Typed superset of JavaScript",
              },
            ]}
          />
        </div>
      </DocsWrapper>
    </div>
  );
}

export default OrbitBlock;
