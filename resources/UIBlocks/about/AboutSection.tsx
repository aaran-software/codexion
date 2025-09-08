import { CheckCircle } from "lucide-react";
import Counter from "../../global/helpers/Counter";

interface FeatureItem {
  id: string;
  text: string;
}

interface AboutProps {
  subtitle: string;
  title: string;
  description: string;
  experienceYears: number;
  experienceLabel: string;
  leftImage: string;
  rightImage: string;
  features: FeatureItem[];
  founderName: string;
  founderRole: string;
  founderImage: string;
  buttonLabel: string;
  onButtonClick?: () => void;
  counterDuration:number
}

const AboutSection: React.FC<AboutProps> = ({
  subtitle,
  title,
  description,
  experienceYears,
  experienceLabel,
  leftImage,
  rightImage,
  features,
  founderName,
  founderRole,
  founderImage,
  buttonLabel,
  onButtonClick,
  counterDuration
}) => {
  return (
    <section className="py-16 px-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        {/* Left Images */}
        <div className="relative w-full flex justify-center md:justify-start">
          {/* Left Image */}
          <img
            src={leftImage}
            alt="About Left"
            className="rounded-lg shadow-lg w-[85%] h-[55vh] md:w-[70%] md:h-[80vh] object-cover"
          />

          {/* Right Image */}
          <img
            src={rightImage}
            alt="About Right"
            className="
                absolute 
                top-1/2 
                left-[45%] 
                -translate-y-1/2 
                rounded-lg shadow-lg 
                w-[65%] h-[35vh] 
                md:w-[50%] md:h-[60vh] 
                object-cover 
                border-[10px] md:border-[16px] border-white
                "
          />
        </div>

        {/* Right Content */}
        <div>
          <p className="text-green-600 font-medium mb-2">{subtitle}</p>
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {title}
          </h2>
          <p className="text-gray-600 mb-6">{description}</p>

          {/* Experience + Features */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-green-900 text-white p-8 rounded-lg text-center flex flex-col justify-center items-center">
              <h3 className="text-5xl font-bold">
                <Counter target={experienceYears} duration={counterDuration} />+
              </h3>

              <p className="mt-2 text-lg">{experienceLabel}</p>
            </div>

            <ul className="space-y-3">
              {features.map((f) => (
                <li
                  key={f.id}
                  className="flex items-center gap-2 text-gray-700"
                >
                  <CheckCircle className="text-green-500 w-5 h-5" />
                  {f.text}
                </li>
              ))}
            </ul>
          </div>

          {/* Founder */}
          <div className="flex items-center gap-4">
            <img
              src={founderImage}
              alt={founderName}
              className="w-14 h-14 rounded-full object-cover"
            />
            <div>
              <h4 className="font-semibold text-gray-900">{founderName}</h4>
              <p className="text-gray-500 text-sm">{founderRole}</p>
            </div>
            <button
              onClick={onButtonClick}
              className="ml-auto bg-green-500 text-white px-5 py-2 rounded shadow hover:bg-green-600 transition"
            >
              {buttonLabel}
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
