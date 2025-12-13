import cv2
import pytesseract
from typing import List, Dict, Tuple

Pixel = Tuple[int, int]


def extract_numeric_markers(image_path: str) -> List[Dict]:
    """
    Extract numeric markers like 1,2,3,5km from route images.
    Returns pixel-space markers.
    """
    img = cv2.imread(image_path)
    if img is None:
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DICT,
        config="--psm 6 digits"
    )

    markers = []

    for i, text in enumerate(data["text"]):
        text = text.strip().lower()
        if not text:
            continue

        value = None
        if text.isdigit():
            value = int(text)
        elif text.endswith("km") and text[:-2].isdigit():
            value = int(text[:-2])

        if value is not None:
            x = data["left"][i] + data["width"][i] // 2
            y = data["top"][i] + data["height"][i] // 2

            markers.append({
                "value": value,
                "pixel": (x, y)
            })

    return markers
