import React from 'react'
import DocsWrapper from '../DocsWrapper'
import RatingReviews from "../../../../../resources/UIBlocks/RatingReviews";

function RatingBlock() {
  return (
    <div>
        <DocsWrapper
        title="RatingReviews"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/RatingReviews",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
        <RatingReviews />
      </DocsWrapper>
    </div>
  )
}

export default RatingBlock