import React from "react";
import DocsWrapper from "../DocsWrapper";
import HighlightSection1 from "../../../../../resources/UIBlocks/HighlightSection/HighlightSection1";

function HighlightSectionBlock() {
  return (
    <div>
      <DocsWrapper
        title="1. HighlightSection1"
        propDocs={[
          {
            name: "subtitle",
            description:
              "Small text displayed above the main heading (e.g., OUR MISSION).",
          },
          {
            name: "title",
            description: "First line of the main heading (e.g., TO END).",
          },
          {
            name: "title2",
            description: "Second line of the main heading (e.g., CYBER RISK).",
          },
          {
            name: "description",
            description: "Main descriptive paragraph about the section.",
          },
          {
            name: "statValue",
            description:
              "Numerical value displayed with animated Counter (e.g., 9).",
          },
          {
            name: "statUnit",
            description:
              "Unit label displayed under statValue (e.g., TRILLION).",
          },
          {
            name: "statDescription",
            description: "Additional description under the stat section.",
          },
          {
            name: "reverse?",
            description:
              "Optional — reverses the layout (stats on left, description on right).",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/highlights/HighlightSection1",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div className="">
          <HighlightSection1
            subtitle="OUR MISSION"
            title="TO END"
            title2="CYBER RISK"
            description="We envision a future without cyber risk. With our comprehensive suite of security operations solutions..."
            statValue={9}
            statUnit="TRILLION"
            statDescription="We analyze 9+ trillion security events on our platform per week. Click to learn more about how our platform works."
          />
        </div>
      </DocsWrapper>
    </div>
  );
}

export default HighlightSectionBlock;
