import React, { useState } from "react";
import DocsWrapper from "../DocsWrapper";
import VerticalImageList from "../../../../../resources/UIBlocks/Slider/VerticalImageList";

function SliderBlock() {
  const [selectedIndex, setSelectedIndex] = useState(0);

  const images = [
    "/assets/bg.jpg",
    "/assets/bg.jpg",
    "/assets/bg.jpg",
    "/assets/bg.jpg",
  ];
  return (
    <div className="flex flex-col gap-10">
      <DocsWrapper
        title="ScrollAdverthisment2"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/Promotion/ScrollAdverthisment2",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div className="flex gap-4">
          {/* Thumbnails (vertical) */}
          <VerticalImageList
            images={images}
            selectedIndex={selectedIndex}
            onSelect={setSelectedIndex}
            direction="vertical" // default
          />

          {/* Main Image Preview */}
          <div className="flex-1 flex items-center justify-center border p-2">
            <img
              src={images[selectedIndex]}
              alt="Selected"
              className="w-[400px] h-[400px] object-contain"
            />
          </div>
        </div>
      </DocsWrapper>
      <DocsWrapper
        title="ScrollAdverthisment2"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/Promotion/ScrollAdverthisment2",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <div className="flex flex-col-reverse gap-4">
          {/* Thumbnails (vertical) */}
          <VerticalImageList
            images={images}
            selectedIndex={selectedIndex}
            onSelect={setSelectedIndex}
            direction="horizontal" // default
          />

          {/* Main Image Preview */}
          <div className="flex-1 flex items-center justify-center border p-2">
            <img
              src={images[selectedIndex]}
              alt="Selected"
              className="w-[400px] h-[400px] object-contain"
            />
          </div>
        </div>
      </DocsWrapper>
    </div>
  );
}

export default SliderBlock;
