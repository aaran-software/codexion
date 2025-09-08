import React, { useEffect, useState } from "react";
import { Link as ScrollLink } from "react-scroll";
import Button from "../../../resources/components/button/Button";

type ContactItem = {
  icon: string;
  title: string;
  value: string;
  href:string
};

type CTAContent = {
  title: string;
  subTitle?: string;
  buttonText: string;
  buttonLink: string; // scroll id or external link
  contacts?: ContactItem[];
};

type BusinessHighlightsSection2Props = {
  backgroundImage: string;
  cta: CTAContent;
};

export default function BusinessHighlightsSection2({
  backgroundImage,
  cta,
}: BusinessHighlightsSection2Props) {
  const [inView, setInView] = useState(false);

  useEffect(() => {
    const section = document.getElementById("stats-section");
    if (!section) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => setInView(entry.isIntersecting));
      },
      { threshold: 0.3 }
    );

    observer.observe(section);
    return () => {
      if (section) observer.unobserve(section);
    };
  }, []);

  return (
    <div id="stats-section" className="relative w-full">
      {/* Background Image */}
      <div
        className={`absolute inset-0 bg-fixed bg-cover bg-center transition-opacity duration-700 ${
          inView ? "opacity-90" : "opacity-0"
        }`}
        style={{ backgroundImage: `url(${backgroundImage})` }}
      ></div>

      {/* Overlay */}
      <div className="absolute inset-0 bg-primary/75"></div>

      {/* Content */}
      <div className="relative z-10 px-5 lg:px-[12%] py-10 flex flex-col justify-between">
        <h1 className="text-2xl md:text-4xl text-primary-foreground my-5 font-bold text-center">
          {cta.title}
        </h1>

        {cta.subTitle && (
          <p className="text-center py-5 text-primary-foreground">{cta.subTitle}</p>
        )}

        {cta.contacts && (
          <div className="flex flex-col sm:flex-row justify-center items-center gap-6 my-10">
            {cta.contacts.map((contact, index) => (
              <div key={index} className="flex gap-3">
                <img
                  src={contact.icon}
                  alt={contact.title}
                  className="shrink-0 h-12"
                />
                <div>
                  <h1 className="text-primary-foreground font-semibold">
                    {contact.title}
                  </h1>
                  <a href={contact.href} className="text-primary-foreground">{contact.value}</a>
                </div>
              </div>
            ))}
          </div>
        )}

        <Button className="bg-primary-foreground w-max font-semibold text-primary rounded-sm border border-ring/30 hover:bg-primary hover:border-ring hover:text-primary-foreground px-4 py-2 text-center text-sm md:text-xl cursor-pointer block mx-auto">
          {cta.buttonText}
        </Button>
      </div>
    </div>
  );
}
