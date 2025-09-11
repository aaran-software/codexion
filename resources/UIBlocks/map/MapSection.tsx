import React from "react";
import WorldMap from "./WorldMap"; // your WorldMap component
import Button from "../../components/button/Button";
import { useNavigate } from "react-router-dom";

type Location = {
  name: string;
  coordinates: [number, number];
};

type MapSectionProps = {
  title: string;
  description: string;
  // WorldMap props
  startLocationName: string;
  lineColor?: string;
  markerColor?: string;
  startMarkerColor?: string;
  textColor?: string;
  locations: Location[];
  mapImage: string;
  mapAlign?: "left" | "right"; // left or right alignment
};

const MapSection: React.FC<MapSectionProps> = ({
  title,
  description,
  startLocationName,
  lineColor = "green",
  markerColor = "green",
  startMarkerColor = "red",
  textColor = "black",
  locations,
  mapImage,
  mapAlign = "right",
}) => {
 
  return (
    <div
      className={`grid gap-4 ${
        mapAlign === "left" ? "grid-cols-1 md:grid-cols-[70%_30%]" : "grid-cols-1 md:grid-cols-[30%_70%]"
      } items-center`}
    >
      {/* Text section */}
      {mapAlign === "right" && (
        <div>
          <h1 className="text-2xl font-bold">{title}</h1>
          <h3 className="mt-2 text-lg text-justify">{description}</h3>
          
        </div>
      )}

      {/* Map section */}
      <WorldMap
        startLocationName={startLocationName}
        lineColor={lineColor}
        markerColor={markerColor}
        startMarkerColor={startMarkerColor}
        textColor={textColor}
        locations={locations}
        mapImage={mapImage}
      />

      {/* If mapAlign is left, text goes after map */}
      {mapAlign === "left" && (
        <div>
          <h1 className="text-2xl font-bold">{title}</h1>
          <h3 className="mt-2 text-lg text-justify">{description}</h3>
        </div>
      )}
    </div>
  );
};

export default MapSection;
