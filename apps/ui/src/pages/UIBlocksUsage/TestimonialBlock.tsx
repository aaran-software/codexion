import React from 'react'
import DocsWrapper from '../DocsWrapper'
import TestimonialCarousel from "../../../../../resources/UIBlocks/testimonials/TestimonialCard";

function TestimonialBlock() {

  const Testimonials = [
    {
      id: 1,
      company: "TechCorp",
      logo: "/assets/client/client.png",
      feedback: "The software streamlined our operations...",
      client: "John Doe, CTO",
    },
    {
      id: 2,
      company: "HealthPlus",
      logo: "/assets/client/client.png",
      feedback: "We reduced costs by 25% after implementing... ",
      client: "Sarah Lee, Operations Head",
    },
    {
      id: 3,
      company: "HealthPlus",
      logo: "/assets/client/client.png",
      feedback: "We reduced costs by 25% after implementing... ",
      client: "Sarah Lee, Operations Head",
    },
  ];
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
         <TestimonialCarousel testimonials={Testimonials} heading={'Our Client Reviews'} />
      </DocsWrapper>
    </div>
  )
}

export default TestimonialBlock