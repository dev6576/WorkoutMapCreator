import React from "react";
import { GoogleMap, DrawingManager, useLoadScript } from "@react-google-maps/api";

const libraries: any = ["drawing"];

interface MapBoxSelectorProps {
  onBoxSelected: (bbox: { north: number; east: number; south: number; west: number }) => void;
}

export default function MapBoxSelector({ onBoxSelected }: MapBoxSelectorProps) {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_KEY,
    libraries,
  });

  if (loadError) return <div>Error loading map</div>;
  if (!isLoaded) return <div>Loading map...</div>;

  return (
    <GoogleMap
      mapContainerStyle={{ width: "100%", height: "400px" }}
      zoom={13}
      center={{ lat: 12.9716, lng: 77.5946 }} // Default center, can make dynamic later
    >
      <DrawingManager
        options={{
          drawingControl: true,
          drawingControlOptions: {
            drawingModes: [google.maps.drawing.OverlayType.RECTANGLE],
            position: google.maps.ControlPosition.TOP_CENTER,
          },
          rectangleOptions: {
            fillColor: "#ffff00",
            fillOpacity: 0.2,
            strokeColor: "#ff0000",
            strokeWeight: 2,
            clickable: false,
            editable: true,
            draggable: false,
          },
        }}
        onRectangleComplete={(rect) => {
          const bounds = rect.getBounds();
          if (!bounds) return;

          const ne = bounds.getNorthEast();
          const sw = bounds.getSouthWest();

          onBoxSelected({
            north: ne.lat(),
            east: ne.lng(),
            south: sw.lat(),
            west: sw.lng(),
          });

          // Optional: remove rectangle after selection or keep it for reference
          rect.setMap(null);
        }}
      />
    </GoogleMap>
  );
}
