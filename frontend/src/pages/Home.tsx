import { useState, useEffect } from "react";
import RouteUploader from "../components/RouteUploader";
import MapBoxSelector from "../components/MapBoxSelector";
import RoutePreview from "../components/RoutePreview";
import { processRoute, fetchPreview } from "../api/routes";

export default function Home() {
  const [routeId, setRouteId] = useState<string | null>(null);
  const [bbox, setBbox] = useState<any>(null);
  const [polyline, setPolyline] = useState<any>(null);
  const [processing, setProcessing] = useState(false);

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
          {bbox && (
            <pre>
              {JSON.stringify(bbox, null, 2)}
            </pre>
          )}
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

      {polyline && (
        <section style={{ marginBottom: "1rem" }}>
          <h2>Step 4: Preview Route</h2>
          <RoutePreview polyline={polyline} />
        </section>
      )}
    </div>
  );
}
