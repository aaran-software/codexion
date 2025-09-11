import React from "react";

type Location = {
  name: string;
  coordinates: [number, number];
};

type WorldMapProps = {
  locations: Location[];
  startLocationName?: string;
  lineColor?: string;
  markerColor?: string;
  startMarkerColor?: string;
  textColor?: string;
  fontSize?: number;
  mapImage?: string;
};

const project = (lon: number, lat: number) => {
  const x = lon + 180;
  const y = 90 - lat;
  return [x, y];
};

const WorldMap: React.FC<WorldMapProps> = ({
  locations,
  startLocationName = "India",
  lineColor = "orange",
  markerColor = "blue",
  startMarkerColor = "red",
  textColor = "black",
  mapImage = "https://upload.wikimedia.org/wikipedia/commons/8/80/World_map_-_low_resolution.svg",
}) => {
  const startLocation = locations.find((loc) => loc.name === startLocationName);

  const createCurvePath = ([x1, y1]: number[], [x2, y2]: number[]) => {
    const cx = (x1 + x2) / 2;
    const cy = (y1 + y2) / 2 - 20;
    return `M ${x1},${y1} Q ${cx},${cy} ${x2},${y2}`;
  };

  return (
    <div className="relative inline-block">
      <svg
        viewBox="0 0 360 180"
        className="w-full h-auto"
        preserveAspectRatio="xMidYMid meet"
      >
        {/* Map */}
        <image href={mapImage} x="0" y="0" width="360" height="180" />

        {/* Lines */}
        {startLocation &&
          locations
            .filter((loc) => loc.name !== startLocationName)
            .map((loc, i) => {
              const start = project(
                startLocation.coordinates[0],
                startLocation.coordinates[1]
              );
              const end = project(loc.coordinates[0], loc.coordinates[1]);
              const path = createCurvePath(start, end);

              return (
                <path
                  key={i}
                  d={path}
                  fill="none"
                  stroke={lineColor}
                  strokeWidth={0.8}
                  strokeDasharray="5,5"
                />
              );
            })}

        {/* Markers */}
        {locations.map((loc, i) => {
          const [x, y] = project(loc.coordinates[0], loc.coordinates[1]);
          const fillColor =
            loc.name === startLocationName ? startMarkerColor : markerColor;

          return <circle key={i} r={2} fill={fillColor} cx={x} cy={y} />;
        })}
      </svg>

      {/* Locations legend INSIDE bottom-right of map */}
      <div className="absolute bottom-0 sm:bottom-2 right-2 md:right-20 rounded-md p-2">
        <h3 className="text-[8px] sm:text-xs font-semibold mb-1">Locations</h3>
        <ul className="space-y-1 grid grid-cols-3 text-xs">
          {locations.map((loc, i) => {
            const isStart = loc.name === startLocationName;
            return (
              <li key={i} className="flex items-center gap-1">
                <span
                  className="w-2 h-2 rounded-full"
                  style={{
                    backgroundColor: isStart ? startMarkerColor : markerColor,
                  }}
                />
                <span className="text-[8px] sm:text-xs" style={{ color: textColor }}>{loc.name}</span>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
};

export default WorldMap;
