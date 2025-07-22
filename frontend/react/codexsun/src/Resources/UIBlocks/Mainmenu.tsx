import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createPortal } from "react-dom";
import settings from "../../../public/JSON/ecart/ecart.json";

interface SubMenuItems {
  title: string;
  path?: string;
}

interface SubMenuGroup {
  title: string;
  items: SubMenuItems[];
}

interface CardItems {
  title: string;
  description: string;
  image: string;
}

type DynamicSubMenus = {
  [key: `subMenu${string}`]: SubMenuGroup | undefined;
};

interface MenuItem extends DynamicSubMenus {
  name: string;
  image: string;
  alt: string;
  card: CardItems;
}

interface MenuWrapper {
  menu: MenuItem;
}

const Mainmenu: React.FC = () => {
  const navigate = useNavigate();
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
  const anchorRefs = useRef<(HTMLDivElement | null)[]>([]);
  const hoverTimeout = useRef<NodeJS.Timeout | null>(null);
  const [position, setPosition] = useState({ top: 0, left: 0 });

  const handleMouseEnter = (index: number) => {
    if (hoverTimeout.current) clearTimeout(hoverTimeout.current);
    setHoveredIndex(index);
  };

  const handleMouseLeave = () => {
    if (hoverTimeout.current) clearTimeout(hoverTimeout.current);
    hoverTimeout.current = setTimeout(() => setHoveredIndex(null), 150);
  };

  const handleCategoryClick = (categoryName: string) => {
    navigate(`/category/${categoryName.toLowerCase()}`);
  };

  useEffect(() => {
    if (
      hoveredIndex !== null &&
      anchorRefs.current[hoveredIndex] &&
      settings.Mainmenu[hoveredIndex].menu
    ) {
      const rect = anchorRefs.current[hoveredIndex]!.getBoundingClientRect();
      const margin = 8;
      const edgeGap = 12;
      const top = rect.bottom + window.scrollY + margin;

      const menuItem = settings.Mainmenu[hoveredIndex].menu;
      const submenuKeys = Object.keys(menuItem).filter(
        (key) =>
          key.startsWith("subMenu") &&
          typeof (menuItem as any)[key] === "object" &&
          (menuItem as any)[key]?.items
      );

      const columnWidth = 180;
      const cardWidth = 320;
      const totalWidth = submenuKeys.length * columnWidth + cardWidth;

      requestAnimationFrame(() => {
        let left = rect.left + rect.width / 2 + window.scrollX - totalWidth / 2;
        const maxLeft = window.innerWidth - totalWidth - edgeGap;

        if (left + totalWidth > window.innerWidth) {
          left = Math.max(maxLeft, margin);
        }
        if (left < margin) {
          left = margin;
        }

        setPosition({ top, left });
      });
    }
  }, [hoveredIndex]);

  return (
    <div className="px-2 mt-4 mb-6">
      <div className="flex gap-5 sm:gap-15 md:gap-10 m-5 lg:mx-20 bg-background overflow-x-auto justify-between scrollbar-hide px-1">
        {settings.Mainmenu.map((item: MenuWrapper, index: number) => {
          const category = item.menu;
          return (
            <div
              key={index}
              ref={(el) => {
                anchorRefs.current[index] = el;
              }}
              onClick={() => handleCategoryClick(category.name)}
              onMouseEnter={() => handleMouseEnter(index)}
              onMouseLeave={handleMouseLeave}
              className="cursor-pointer w-[100px] sm:w-auto flex-shrink-0 text-center relative"
            >
              <img
                src={category.image}
                alt={category.alt}
                className="w-[70px] h-[70px] mx-auto object-scale-down"
              />
              <p className="text-sm font-medium mt-1">{category.name}</p>
            </div>
          );
        })}
      </div>

      {hoveredIndex !== null &&
        createPortal(
          <div
            onMouseEnter={() => handleMouseEnter(hoveredIndex)}
            onMouseLeave={handleMouseLeave}
            className="absolute z-[100000] bg-background border border-ring/30 rounded-md shadow-lg text-sm max-h-[60vh] overflow-x-auto  duration-500 overflow-y-hidden"
            style={{
              top: position.top,
              left: position.left,
              maxWidth: "calc(100vw - 16px)",
            }}
          >
            <div className="flex flex-row w-max max-w-screen  px-2">
              <div className="flex flex-col justify-between w-[300px] gap-3 px-3 py-2 h-full shrink-0">
                <div>
                  <h3 className="text-lg font-semibold">
                    {settings.Mainmenu[hoveredIndex].menu.card.title}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {settings.Mainmenu[hoveredIndex].menu.card.description}
                  </p>
                </div>
                <img
                  src={settings.Mainmenu[hoveredIndex].menu.card.image}
                  alt={settings.Mainmenu[hoveredIndex].menu.card.title}
                  className="object-scale-down h-60 rounded"
                />
              </div>

              {Object.entries(settings.Mainmenu[hoveredIndex].menu)
                .filter(
                  ([key, value]) =>
                    key.startsWith("subMenu") &&
                    typeof value === "object" &&
                    (value as any)?.items
                )
                .map(([key, value]) => {
                  const group = value as SubMenuGroup;
                  return (
                    <ul
                      key={key}
                      className="min-w-[180px] max-h-[400px] overflow-y-auto py-2 border-l border-ring/30 shrink-0"
                    >
                      <li className="px-3 py-1 text-xs font-semibold text-foreground">
                        {group.title}
                      </li>
                      {group.items.map((item, i) => (
                        <li
                          key={i}
                          onClick={(e) => {
                            e.stopPropagation();
                            if (item.path) {
                              navigate(item.path);
                              setHoveredIndex(null);
                            }
                          }}
                          className="cursor-pointer px-3 py-2 hover:underline hover:text-update rounded text-sm text-foreground/60"
                        >
                          {item.title}
                        </li>
                      ))}
                    </ul>
                  );
                })}
            </div>
          </div>,
          document.body
        )}
    </div>
  );
};

export default Mainmenu;
