import React from "react";
import AboutSection from "../../../../../resources/UIBlocks/about/AboutSection";

function AboutBlock() {
  return (
    <div>
      <AboutSection
        subtitle="About Textilery"
        title="We Provide The Best Textile Industry Since 2005"
        description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        experienceYears={16}
        counterDuration={2000}
        experienceLabel="Years Of Experiences"
        leftImage="/assets/bg2.jpg"
        rightImage="/assets/bg.jpg"
        features={[
          { id: "f1", text: "Best Quality Standards" },
          { id: "f2", text: "100% Satisfaction Guarantee" },
          { id: "f3", text: "Quality Control System" },
          { id: "f4", text: "Commitment to Customers" },
          { id: "f5", text: "Highly Professional Team" },
        ]}
        founderName="Miya Draper"
        founderRole="PVR Groups"
        founderImage="/assets/user.png"
        buttonLabel="About Us"
        onButtonClick={() => alert("Go to About Page")}
      />
    </div>
  );
}

export default AboutBlock;
