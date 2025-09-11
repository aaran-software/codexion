import React, { useState } from "react";
import DocsWrapper from "../DocsWrapper";
import SpecTable, {
  TableRow,
} from "../../../../../resources/UIBlocks/table/SpecTable";

function TableBlock() {
  const [tableData] = useState<TableRow[]>([
    {
      header: "Type of Yarn",
      data: [
        "100% Cotton",
        "Recycled Cotton",
        "Organic Cotton",
        "Ecowear",
        "Recycled Polyester",
        "Spandex",
        "Slub",
        "Cloudy Yarn",
        "Viscose",
        "Rayon",
        "Tencel",
      ],
    },
    {
      header: "Fabric Construction",
      data: [
        "Plain Jersey",
        "Jacquard",
        "Single Knit Piqué",
        "2nd and 3rd Fleece",
        "French Terry",
        "Interlock",
        "Flat Knit (Cuff and Collars)",
        "Rib",
        "Waffle",
        "Terry",
        "Striped",
      ],
    },
    {
      header: "Textile Dyeing Production",
      data: [
        "Techniques:",
        "Reactive Dyes",
        "Garment Dyeing",
        "Lava Dyeing",
        "Natural Dyes - Plant Based",
        "Tie & Dye",
        "Mineral Dyeing",
      ],
    },
    {
      header: "Sewing Construction",
      data: [
        "Short Sleeve Tee",
        "Long Sleeve Tee",
        "Raglan Tee",
        "Tank Tops",
        "Hoodies, Sweat-shirts, Pyjama Sets",
        "Pants, Shorts, Rompers, Onesie",
        "Gender: Men, Women, Boys, Girls, Toddlers",
      ],
    },
    {
      header: "Embellishment Techniques",
      data: [
        "Screen Print",
        "Panel Print",
        "Heat Transfer",
        "Rotary Print",
        "Embroidery",
        "Sequins",
        "Applique",
      ],
    },
    {
      header: "Screenprinting",
      data: [
        "PVC and Phthalate Free Inks",
        "Discharge",
        "Foil",
        "Flock",
        "Glow in the dark",
        "High Density",
        "Push Through",
        "Digital Print",
        "Glitter",
        "Crackle",
        "Puff",
      ],
    },
  ]);

  return (
    <div>
      <DocsWrapper
        title="SpecTable"
        propDocs={[
          {
            name: "tableData",
            description: "contains the table rows and cells",
          },
        ]}
        paths={{
          file: "resources/UIBlocks/table/SpecTable",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <SpecTable tableData={tableData} />
      </DocsWrapper>
    </div>
  );
}

export default TableBlock;
