import { useState, useEffect } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import RouteUploader from "../components/RouteUploader";
import MapBoxSelector from "../components/MapBoxSelector";
import RoutePreview from "../components/RoutePreview";
import { processRoute, fetchPreview } from "../api/routes";

export default function Home() {
  const [routeId, setRouteId] = useState<string | null>(null);
  const [bbox, setBbox] = useState<any>(null);
  const [polyline, setPolyline] = useState<any>(null);
  const [processing, setProcessing] = useState(false);
  const [refinedPolyline, setRefinedPolyline] = useState<any>(null);

  function downloadRouteGPX(points: { lat: number; lng: number }[]) {
    const gpxHeader = `<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="WorkoutMapCreator" xmlns="http://www.topografix.com/GPX/1/1">
  <trk>
    <name>My Route</name>
    <trkseg>
`;

    const gpxFooter = `
    </trkseg>
  </trk>
</gpx>`;

    const gpxPoints = points
      .map(p => `      <trkpt lat="${p.lat}" lon="${p.lng}"></trkpt>`)
      .join("\n");

    const gpxContent = gpxHeader + gpxPoints + gpxFooter;

    const blob = new Blob([gpxContent], { type: "application/gpx+xml" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "route.gpx";
    a.click();
    URL.revokeObjectURL(url);
  }

  const handleProcess = async () => {
    if (!routeId || !bbox) return;
    console.log("Home.handleProcess: starting", { routeId, bbox });
    setProcessing(true);

    try {
      await processRoute(routeId, bbox);
      const preview = await fetchPreview(routeId);
      setPolyline(preview.polyline.geo); // Array of {lat,lng}
    } catch (err) {
      console.error(err);
      alert("Error processing route");
    } finally {
      setProcessing(false);
    }
  };

  useEffect(() => {
    console.log("Home mounted");
  }, []);

  useEffect(() => {
    console.log("Home: routeId changed", routeId);
  }, [routeId]);

  useEffect(() => {
    console.log("Home: bbox changed", bbox);
  }, [bbox]);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Workout Map Creator</h1>

      <section style={{ marginBottom: "1rem" }}>
        <h2>Step 1: Upload Route Image</h2>
        <RouteUploader onUploaded={setRouteId} />
        {routeId && <p>Uploaded! Route ID: {routeId}</p>}
      </section>

      {routeId && (
        <section style={{ marginBottom: "1rem" }}>
          <h2>Step 2: Select Map Bounding Box</h2>
          <MapBoxSelector onBoxSelected={setBbox} />
          {bbox && <pre>{JSON.stringify(bbox, null, 2)}</pre>}
        </section>
      )}

      {routeId && bbox && (
        <section style={{ marginBottom: "1rem" }}>
          <h2>Step 3: Process Route</h2>
          <button onClick={handleProcess} disabled={processing}>
            {processing ? "Processing..." : "Process Route"}
          </button>
        </section>
      )}

      {polyline?.length > 0 && (
        <section style={{ marginBottom: "1rem" }}>
          <h2>Step 4: Preview & Refine Route</h2>
          <MapContainer
            center={[polyline[0].lat, polyline[0].lng]}
            zoom={14}
            style={{ width: "100%", height: "400px" }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            <RoutePreview
              polyline={polyline}
              onChange={(updated) => setRefinedPolyline(updated)}
            />
          </MapContainer>

          {refinedPolyline && (
            <button
              style={{ marginTop: "1rem" }}
              onClick={() => downloadRouteGPX(refinedPolyline)}
            >
              Download Navigable Route (GPX)
            </button>
          )}
        </section>
      )}
    </div>
  );
}
