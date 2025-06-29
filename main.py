from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from io import BytesIO
import os
import threading

app = FastAPI()
lock = threading.Lock()
COUNTER_FILE = "counter.txt"

# Image placeholders only (no rendering)
image_layout = [
    {
        "path": "C:/Users/Lenovo/OneDrive/Desktop/Mann/catalog_images/raw231.jpg",
        "x": 56.7,
        "y": 113.4,
        "w": 198.4,
        "h": 425.2
    },
    {
        "path": "C:/Users/Lenovo/OneDrive/Desktop/Mann/catalog_images/raw12.jpg",
        "x": 326.6,
        "y": 586.4,
        "w": 340.2,
        "h": 141.75
    },
    {
        "path": "C:/Users/Lenovo/OneDrive/Desktop/Mann/catalog_images/su2.jpg",
        "x": 326.6,
        "y": 113.4,
        "w": 241.95,
        "h": 198.45
    }
]

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h2>🧾Product Layout</h2>
    <p>CLick Here </p>
    <p><a href="/generate-catalog-layout/" target="_blank">Generate PDF</a></p>
    """

def get_next_counter():
    with lock:
        if not os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, "w") as f:
                f.write("1")
            return 1
        with open(COUNTER_FILE, "r+") as f:
            count = int(f.read())
            f.seek(0)
            f.write(str(count + 1))
            f.truncate()
            return count

@app.get("/generate-catalog-layout/")
async def generate_catalog_layout():
    pdf_number = get_next_counter()
    filename = f"catalog_layout_{pdf_number}.pdf"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Title placeholder
    c.setFont("Helvetica-Bold", 24)
    # No drawString for title

    # Description block
    c.setFont("Helvetica", 12)
    desc = c.beginText(2 * cm, A4[1] - 4 * cm)
    c.drawText(desc)

    # Specifications block
    spec = c.beginText(11.5 * cm, A4[1] - 11 * cm)
    c.drawText(spec)

    # Skip images but preserve layout
    for img in image_layout:
        pass

    # No footer

    c.showPage()
    c.save()
    buffer.seek(0)

    return Response(
        content=buffer.read(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
