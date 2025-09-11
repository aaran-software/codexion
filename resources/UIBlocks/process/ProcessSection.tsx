import React from "react";

type Item = {
  title: string;
  description: string;
  icon?: React.ReactNode | string;
};

type ListProps = {
  items: Item[];
  className?: string;
  title: string;
};

function TitleIconDescriptionCard({
  title,
  description,
  icon,
  index,
}: Item & { index: number }) {
  const isEven = index % 2 === 0;

  return (
    <div className="grid grid-cols-[1fr_auto_1fr] px-2 items-center gap-4">
      {/* Left cell */}
      <div className="flex flex-col items-end text-right w-full break-words">
        {isEven ? (
          <h3 className="text-sm sm:text-lg md:text-xl font-semibold leading-tight break-words text-highlight2">
            {title}
          </h3>
        ) : (
          <p className="text-xs md:text-base text-foreground break-words">
            {description}
          </p>
        )}
      </div>

      {/* Center icon */}
      <div className="flex justify-center shrink-0">
        <div className="w-12 h-12 md:w-24 md:h-24 rounded-full flex items-center justify-center">
          {typeof icon === "string" ? (
            <img
              src={icon}
              alt="icon"
              className="w-8 h-8 md:w-20 md:h-20 object-contain"
            />
          ) : (
            icon
          )}
        </div>
      </div>

      {/* Right cell */}
      <div className="flex flex-col items-start text-left w-full break-words">
        {isEven ? (
          <p className="text-xs md:text-base text-foreground break-words">
            {description}
          </p>
        ) : (
          <h3 className="text-sm sm:text-lg md:text-xl font-semibold leading-tight break-words text-highlight2">
            {title}
          </h3>
        )}
      </div>
    </div>
  );
}

export default function ProcessSection({
  items,
  className = "",
  title,
}: ListProps) {
  return (
    <div className="max-w-full overflow-x-hidden">
      <h1 className="text-center text-xl md:text-4xl font-bold pb-10 break-words">
        {title}
      </h1>
      <div className={`flex flex-col gap-5 ${className}`}>
        {items.map((item, idx) => (
          <TitleIconDescriptionCard key={idx} {...item} index={idx} />
        ))}
      </div>
    </div>
  );
}
