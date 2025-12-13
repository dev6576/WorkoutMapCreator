import { uploadRouteImage } from "../api/routes";

export default function RouteUploader({ onUploaded }: any) {
  const handleFile = async (e: any) => {
    const file = e.target.files[0];
    if (!file) return;

    console.log("RouteUploader: file selected", file.name, file.size);
    try {
      const res = await uploadRouteImage(file);
      console.log("RouteUploader: upload response", res);
      onUploaded(res.route_id);
    } catch (err) {
      console.error("RouteUploader: upload error", err);
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFile} />
    </div>
  );
}
