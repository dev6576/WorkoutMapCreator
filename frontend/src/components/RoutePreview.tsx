import { GoogleMap, Polyline } from "@react-google-maps/api";
import { useEffect } from "react";

export default function RoutePreview({ polyline }: any) {
  useEffect(() => {
    console.log("RoutePreview: polyline prop changed", polyline);
  }, [polyline]);

  if (!polyline) return null;

  return (
    <GoogleMap
      mapContainerStyle={{ width: "100%", height: "400px" }}
      zoom={14}
      center={polyline[0]}
    >
      <Polyline
        path={polyline}
        options={{
          strokeColor: "#ff0000",
          strokeWeight: 4
        }}
      />
    </GoogleMap>
  );
}
