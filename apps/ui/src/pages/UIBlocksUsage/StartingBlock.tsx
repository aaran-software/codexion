import React from 'react'
import DocsWrapper from '../DocsWrapper'
import StartingSection1 from "../../../../../resources/UIBlocks/startingsection/StartingSection1";

function StartingBlock() {
  return (
    <div>
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
        <StartingSection1 />
      </DocsWrapper>
    </div>
  )
}

export default StartingBlock