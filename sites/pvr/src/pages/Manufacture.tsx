import React, { useState } from "react";
import Roadmap2 from "../../../../resources/UIBlocks/Roadmap/RoadMap2";
import { Rocket, Target, Users } from "lucide-react";
import HeroBanner from "../../../../resources/UIBlocks/banner/HeroBanner";
import { useNavigate } from "react-router-dom";
import SpecTable, { TableRow } from "../../../../resources/UIBlocks/table/SpecTable";

function Manufacture() {
  const navigate = useNavigate();

  

  const roadmapData2 = [
    {
      year: "01",
      title: "PRODUCTION DEVELOPMENT",
      description: `Team in charge to aid the process of converting your
design ideas into a final product`,
      icon: <Users className="w-5 h-5 text-white" />,
      color: "#F59E0B", // amber
      image: "/assets/banner/banner1.jpg",
    },
    {
      year: "02",
      title: "KNITTING",
      description: `Our knitting partners help us produce a wide variety
of fabrics using knitting machines imported from
Germany & USA.`,
      icon: <Target className="w-5 h-5 text-white" />,
      color: "#10B981", // green
      image: "/assets/banner/banner1.jpg",
    },
    {
      year: "03",
      title: " DYEING & FINISHING",
      description: `By implementing a Zero Discharge Policy, our dyeing
units recycle and reuse effluent water, thereby
mitigating significant environmental risks and
hazards.`,
      icon: <Rocket className="w-5 h-5 text-white" />,
      color: "#3B82F6", // blue
      image: "/assets/banner/banner1.jpg",
    },
    {
      year: "04",
      title: "CUTTING",
      description: `The fabric is inspected and then spread
using the auto spreader and cut precisely
with our cutting machines.`,
      icon: <Users className="w-5 h-5 text-white" />,
      color: "#F59E0B", // amber
      image: "/assets/banner/banner1.jpg",
    },
    {
      year: "05",
      title: "SEWING",
      description: `Our highly skilled employees are able to
craft a wide variety of garments. Our
unit is also equipped with solar panels
to fulfill our electricity requirements.`,
      icon: <Target className="w-5 h-5 text-white" />,
      color: "#10B981", // green
      image: "/assets/banner/banner1.jpg",
    },
    {
      year: "06",
      title: "SCREENPRINTING",
      description: `We offer a whole range of
screen printing techniques, equipped
with 2 M&R Printing Machines (USA).`,
      icon: <Rocket className="w-5 h-5 text-white" />,
      color: "#3B82F6", // blue
      image: "/assets/banner/banner1.jpg",
    },
    {
      year: "07",
      title: " EMBROIDERY & EMBELLISHMENT",
      description: `Our embroidery division equipped
with 3- Tajima machines, provide
a wide variety of Embroidery,
Applique & Sequins work.`,
      icon: <Users className="w-5 h-5 text-white" />,
      color: "#F59E0B", // amber
      image: "/assets/banner/banner1.jpg",
    },
    {
      year: "08",
      title: "INSPECTION",
      description: `Every garment goes
through a strict Quality
Check Process
`,
      icon: <Target className="w-5 h-5 text-white" />,
      color: "#10B981", // green
      image: "/assets/banner/banner1.jpg",
    },
    {
      year: "09",
      title: "SHIPPING",
      description: `From our facility we ship
to service our
global customers.`,
      icon: <Rocket className="w-5 h-5 text-white" />,
      color: "#3B82F6", // blue
      image: "/assets/banner/banner1.jpg",
    },
  ];

  const [sections] = useState([
    {
      title: "Stitching Unit",
      items: [
        { label: "Production Capacity", value: "8000 PCS / DAY" },
        {
          label: "Sewing Machines",
          value: "200 - Overlock, Flatlock, Single Needle Stitching Machines",
        },
      ],
    },
    {
      title: "Other Supporting",
      items: [
        {
          label: "Machines",
          value: [
            "Auto Spreader",
            "Laser Cutting Machine",
            "Computerized Pattern Making Machine",
            "Fabric Inspection Table",
            "Lab Testing Equipments",
          ],
        },
      ],
    },
  ]);
  return (
    <div>
      <div className="relative h-[40vh] sm:h-[50vh] mt-20 lg:mt-30 w-full">
        <img
          src="/assets/banner/banner1.jpg"
          alt="Sample"
          className="h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-foreground/70" />
        <div className="absolute inset-0 flex justify-center items-center">
          <h1 className="text-6xl font-bold text-background">Manufacture</h1>
        </div>
      </div>

      

      <Roadmap2
        items={roadmapData2}
        RoadmapHeading={"Manufacutering Process"}
      />

      <section className="max-w-5xl mx-auto py-12 px-6">
        {/* Main Heading */}
        <h1 className="text-3xl md:text-4xl font-bold text-center text-gray-800 mb-10">
          PVR INTERNATIONAL – PRODUCTION CAPACITY
        </h1>

        {/* Sections */}
        <div className="space-y-10">
          {sections.map((section, idx) => (
            <div key={idx}>
              {/* Section Title */}
              <h2 className="text-xl md:text-2xl font-semibold text-primary mb-6 border-b-2 border-primary/30 pb-2">
                {section.title}
              </h2>

              {/* Items */}
              <div className="space-y-4">
                {section.items.map((item, i) => (
                  <div
                    key={i}
                    className="grid grid-cols-[40%_60%] items-start gap-3 rounded-lg p-4 transition"
                  >
                    {/* Label */}
                    <div className="flex justify-between pr-4 font-medium text-foreground/90">
                      <p>{item.label}</p>
                    </div>

                    {/* Value */}
                    {Array.isArray(item.value) ? (
                      <ul className="list-disc list-inside text-foreground/80 space-y-1">
                        {item.value.map((val, j) => (
                          <li key={j}>{val}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-gray-600">{item.value}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <div className="px-4 lg:px-[10%] mb-20">
        <HeroBanner
          badgeText="🚀 Featured"
          title="Manufacturing
Capabilities"
          subtitle="We do not envisionatrade-off between profit and people,
or between manufacturing and environmental responsibility.
One of Vertical Knits competitive advantages is the
vertically-integrated business model built over a lean supply
chain and sustainable practices, covering the entire value chain:
product development, manufacturing and distribution."
          buttonText="Start Now"
          buttonHandleClick={() => {
            navigate("/contact");
          }}
        />
      </div>
    </div>
  );
}

export default Manufacture;
