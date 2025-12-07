import requests
import base64

API_URL = "http://127.0.0.1:8000/generate_poster"

payload = {
    "summary": "In the aftermath of a new interplanetary conflict, Jake Sully and the Na’vi face a mysterious force born from fire and ash that threatens Pandora’s balance.",
    "style_hint": "epic, bioluminescent, alien",
}

print("Requesting poster...")
resp = requests.post(API_URL, json=payload)
resp.raise_for_status()

data = resp.json()
data_url = data["image_url"]

# data_url 形如 "data:image/png;base64,AAAA...."
header, b64 = data_url.split(",", 1)
img_bytes = base64.b64decode(b64)

out_path = "poster.png"
with open(out_path, "wb") as f:
    f.write(img_bytes)

print(f"Saved to {out_path}")