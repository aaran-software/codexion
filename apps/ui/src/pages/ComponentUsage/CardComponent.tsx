import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../../../../../resources/components/chart/card";

import { useState } from "react";

function CardComponent() {
  const [card] = useState([
    {
      title:"Single Card",
      className: "grid grid-cols-1 gap-4",
      content: [
        {
          title: "Dynamic Rendering",
          description:
            "Render UI components based on user interaction or state changes.",
        },
      ],
    },
    {
      title:"Double Card",
      className: "grid grid-cols-2 gap-6",
      content: [
        {
          title: "Component Mapping",
          description: "Use a map object to render the right component dynamically.",
        },
        {
          title: "Cleaner Code",
          description: "Avoid long if-else blocks using configuration-driven rendering.",
        },
      ],
    },
    {
      title:"Multiple Card",
      className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4",
      content: [
        {
          title: "Maintainable",
          description: "Update or add new views easily through a central map.",
        },
        {
          title: "Reusable",
          description: "Structure UI logic for flexibility and reuse.",
        },
        {
          title: "Scalable",
          description: "Handle many components without messy conditional JSX.",
        },
        {
          title: "Declarative",
          description: "Describe what to render in data, not control logic.",
        },
      ],
    },
  ]);

  return (
    <div className="space-y-6 px-5">
      {card.map((section, index) => (
        <div key={index}>
            <div className="my-5 text-xl font-bold">{section.title}</div>
            <div className={section.className}>
            {section.content.map((car, idx) => (
                <Card key={idx}>
                <CardHeader>
                    <CardTitle>{car.title}</CardTitle>
                </CardHeader>
                <CardContent>
                    <CardDescription>{car.description}</CardDescription>
                </CardContent>
                </Card>
            ))}
            </div>
        </div>
      ))}
    </div>
  );
}

export default CardComponent;
