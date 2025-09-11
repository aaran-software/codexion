import DocsWrapper from "../DocsWrapper";
import Roadmap from "../../../../../resources/UIBlocks/Roadmap/Roadmap";
import Roadmap2 from "../../../../../resources/UIBlocks/Roadmap/Roadmap2";
import { Rocket, Target, Users } from "lucide-react";
function RoadMapBlock() {
  const roadmapData = [
    {
      year: "2015",
      title: "Founded the Company",
      description: "Started with a small team of passionate developers.",
      icon: <Users className="w-5 h-5 text-white" />,
      color: "#F59E0B", // amber
    },
    {
      year: "2018",
      title: "First Enterprise Client",
      description: "Delivered scalable ERP solution for a global manufacturer.",
      icon: <Target className="w-5 h-5 text-white" />,
      color: "#10B981", // green
    },
    {
      year: "2023",
      title: "AI & Cloud Innovation",
      description: "Launched SaaS products leveraging AI and cloud computing.",
      icon: <Rocket className="w-5 h-5 text-white" />,
      color: "#3B82F6", // blue
    },
  ];

  const roadmapData2 = [
    {
      year: "2015",
      title: "Founded the Company",
      description: "Started with a small team of passionate developers.",
      icon: <Users className="w-5 h-5 text-white" />,
      color: "#F59E0B", // amber
      image:"/assets/bg.jpg"
    },
    {
      year: "2018",
      title: "First Enterprise Client",
      description: "Delivered scalable ERP solution for a global manufacturer.",
      icon: <Target className="w-5 h-5 text-white" />,
      color: "#10B981", // green
      image:"/assets/bg.jpg"
    },
    {
      year: "2023",
      title: "AI & Cloud Innovation",
      description: "Launched SaaS products leveraging AI and cloud computing.",
      icon: <Rocket className="w-5 h-5 text-white" />,
      color: "#3B82F6", // blue
      image:"/assets/bg.jpg"
    },
  ];
  return (
    <div>
      <DocsWrapper
        title="1. Roadmap"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/Roadmap/Roadmap",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <Roadmap
          items={roadmapData}
          RoadmapHeading={"Our Journey & Future Roadmap"}
        />
      </DocsWrapper>

       <DocsWrapper
        title="2. Roadmap with image"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/Roadmap/Roadmap",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <Roadmap2
          items={roadmapData2}
          RoadmapHeading={"Our Journey & Future Roadmap"}
        />
      </DocsWrapper>
    </div>
  );
}

export default RoadMapBlock;
