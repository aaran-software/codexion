import { FC } from "react";
import Counter from "../../../resources/global/helpers/Counter";

interface HighlightSection1Props {
  subtitle: string; // e.g. "OUR MISSION"
  title: string; // e.g. "TO END CYBER RISK"
  title2: string; // e.g. "TO END CYBER RISK"
  description: string; // paragraph text
  statValue: number; // e.g. "9+"
  statUnit: string; // e.g. "TRILLION"
  statDescription: string; // e.g. "We analyze 9+ trillion..."
  reverse?: boolean; // Optional: to reverse the layout
}

const HighlightSection1: FC<HighlightSection1Props> = ({
  subtitle,
  title,
  title2,
  description,
  statValue,
  statUnit,
  statDescription,
  reverse = false,
}) => {
  return (
    <section className="py-16 text-center md:text-left">
      <h4 className="text-primary uppercase text-center tracking-wide mb-3 font-semibold">
        {subtitle}
      </h4>
      <h2 className="text-5xl md:text-6xl font-extrabold text-center leading-tight">
        {title}
      </h2>
      <h2 className="text-5xl md:text-6xl font-extrabold text-center mb-6 leading-tight">
        {title2}
      </h2>
      <div className={`md:flex ${reverse ? "md:flex-row-reverse":""} md:items-start md:gap-12`}>
        <p className={`text-foreground text-lg ${reverse ? "md:text-left" : "md:text-right"} text-justify md:w-2/3 mb-8 md:mb-0`}>
          {description}
        </p>
        <div className={`md:w-1/3 ${reverse ? "md:border-r-3 md:text-right md:pr-5":"md:border-l-3 md:text-left md:pl-5"} text-justify border-primary`}>
          {/* <div className="text-5xl font-extrabold mb-2">{}</div> */}
          <div className={`text-5xl font-bold text-center ${reverse ? "md:text-right" : "md:text-left"} mb-2`}>
            <Counter target={statValue} />+
          </div>
          <div className={`uppercase text-primary font-medium tracking-wide mb-4 text-center ${reverse ? "md:text-right" : "md:text-left"}`}>
            {statUnit}
          </div>
          <p className={`text-gray-600 mb-4`}>{statDescription}</p>
        </div>
      </div>
    </section>
  );
};

export default HighlightSection1;
