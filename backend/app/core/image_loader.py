from fastapi import UploadFile
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


async def save_image(file: UploadFile, route_id: str) -> str:
    path = UPLOAD_DIR / f"{route_id}_{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    return str(path)
