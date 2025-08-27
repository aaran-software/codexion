import DocsWrapper from "../DocsWrapper";
import MapSection from "../../../../../resources/UIBlocks/map/MapSection";

function MapBlock() {
  return (
    <div>
      <DocsWrapper
        title="Consultant"
        propDocs={[
          {
            name: "companyInfo",
            description:
              "Array of statistic objects with `icon`, `count`, `symbol`, and `field` to display key company metrics.",
          },
          {
            name: "backgroundImage",
            description: "Background image URL for the section.",
          },
          {
            name: "cta",
            description:
              "Call-to-action object with `title`, `buttonText`, and `buttonLink`.",
          },
        ]}
        paths={{
          file: "/resources/UIBlocks/consultant/Consultant",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: ["Features Section", "Landing Pages", "Service Blocks"],
        }}
      >
        <MapSection
          title="Our Global Presence"
          description="See where our offices and key client locations are situated across the world. We are proud to serve clients in multiple regions, connecting businesses globally."
          buttonLabel="Contact Us"
          buttonPath="contact"
          startLocationName="India"
          lineColor="orange"
          markerColor="blue"
          startMarkerColor="red"
          textColor="black"
          locations={[
            { name: "India", coordinates: [-27.106713, -62.113318] }, //{x,y}
            { name: "Gujarat", coordinates: [-58.2772, -4.0583] },
            { name: "Delhi", coordinates: [-27.2529, 62.2048] },
            { name: "Odisha", coordinates: [10.0, -10.0] },
          ]}
          mapImage="/assets/india.png"
          mapAlign="right"
          fontSize={5}
        />
      </DocsWrapper>
    </div>
  );
}

export default MapBlock;
