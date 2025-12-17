import { useEffect, useState } from "react";
import { Polyline, CircleMarker, useMapEvents } from "react-leaflet";

type LatLng = {
  lat: number;
  lng: number;
};

export default function RoutePreview({
  polyline,
  onChange,
}: {
  polyline: LatLng[];
  onChange?: (updated: LatLng[]) => void;
}) {
  const [points, setPoints] = useState<LatLng[]>(polyline);

  useEffect(() => {
    setPoints(polyline);
  }, [polyline]);

  // Map click handler to add or remove points
  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;

      // Find if user clicked near an existing point (5 meters threshold)
      const existingIndex = points.findIndex(
        (p) =>
          Math.abs(p.lat - lat) < 0.00005 && Math.abs(p.lng - lng) < 0.00005
      );

      let updated: LatLng[];
      if (existingIndex >= 0) {
        // Remove point
        updated = [...points];
        updated.splice(existingIndex, 1);
      } else {
        // Add new point
        updated = [...points, { lat, lng }];
      }

      setPoints(updated);
      if (onChange) onChange(updated);
    },
  });

  if (!points || points.length === 0) return null;

  return (
    <>
      <Polyline
        positions={points.map((p) => [p.lat, p.lng] as [number, number])}
        pathOptions={{ color: "red", weight: 4 }}
      />
      {points.map((p, idx) => (
        <CircleMarker
          key={idx}
          center={[p.lat, p.lng]}
          radius={6}
          color="blue"
          fillColor="cyan"
          fillOpacity={0.8}
        />
      ))}
    </>
  );
}
