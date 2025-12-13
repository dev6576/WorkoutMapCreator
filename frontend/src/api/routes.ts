import axios from "axios";

const API_BASE = "http://localhost:8000/api/v1";

export async function uploadRouteImage(file: File) {
  const form = new FormData();
  form.append("file", file);

  console.log("api.uploadRouteImage: uploading file", file.name);
  const res = await axios.post(`${API_BASE}/routes/upload`, form);
  console.log("api.uploadRouteImage: response", res.data);
  return res.data; // { route_id }
}

export async function processRoute(routeId: string, bbox: any) {
  console.log("api.processRoute: routeId, bbox", routeId, bbox);
  const res = await axios.post(
    `${API_BASE}/routes/${routeId}/process`,
    {
      search_scope: {
        bbox,
        padding_meters: 200
      }
    }
  );
  console.log("api.processRoute: response", res.data);
  return res.data;
}

export async function fetchPreview(routeId: string) {
  console.log("api.fetchPreview: fetching preview for", routeId);
  const res = await axios.get(`${API_BASE}/routes/${routeId}/preview`);
  console.log("api.fetchPreview: response", res.data);
  return res.data;
}
