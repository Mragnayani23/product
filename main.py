from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import List, Optional
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
import threading

app = FastAPI()
lock = threading.Lock()
COUNTER_FILE = "counter.txt"

# 🧱 Request body schema
class ImageData(BaseModel):
    path: str
    x: float
    y: float
    w: float
    h: float

class ProductData(BaseModel):
    name: Optional[str] = ""
    description: List[str] = []
    specifications: List[str] = []
    hs_code: Optional[str] = ""
    quantity: Optional[str] = ""
    unit: Optional[str] = ""
    fcl_type: Optional[str] = ""
    packaging: Optional[str] = ""
    quantity_per_fcl: Optional[str] = ""
    images: List[ImageData] = []

# 🔢 Auto-incrementing PDF number
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

@app.get("/")
def root():
    return {
        "message": "POST your product data to /generate-catalog-pdf/ to receive a customized PDF."
    }

# 📩 POST endpoint to accept input & return PDF
@app.post("/generate-catalog-pdf/")
async def generate_catalog_pdf(data: ProductData):
    pdf_number = get_next_counter()
    filename = f"catalog_generated_{pdf_number}.pdf"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    if data.name:
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.darkred)
        c.drawString(2 * cm, height - 2.5 * cm, data.name)

    # Description
    if data.description:
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        desc = c.beginText(2 * cm, height - 4 * cm)
        desc.textLine("Description:")
        desc.textLine("")
        for line in data.description:
            desc.textLine(line)
        c.drawText(desc)

    # Specifications
    c.setFont("Helvetica", 12)
    spec = c.beginText(11.5 * cm, height - 11 * cm)
    if data.specifications:
        spec.textLine("Specifications:")
        spec.textLine("")
        for line in data.specifications:
            spec.textLine(line)
        spec.textLine("")
    if data.hs_code:
        spec.textLine(f"• HS Code: {data.hs_code}")
    if data.quantity:
        spec.textLine(f"• Quantity: {data.quantity} {data.unit}")
    if data.fcl_type:
        spec.textLine(f"• FCL Type: {data.fcl_type}")
    if data.packaging:
        spec.textLine(f"• Packaging: {data.packaging}")
    if data.quantity_per_fcl:
        spec.textLine(f"• Quantity/FCL: {data.quantity_per_fcl}")
    c.drawText(spec)

    # Images (if provided)
    for img in data.images:
        if os.path.exists(img.path):
            c.drawImage(
                ImageReader(img.path),
                x=img.x,
                y=img.y,
                width=img.w,
                height=img.h,
                preserveAspectRatio=True
            )

    c.showPage()
    c.save()
    buffer.seek(0)

    return Response(
        content=buffer.read(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
