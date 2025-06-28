<<<<<<< HEAD
from fastapi import FastAPI, Response
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
    width, height = A4

    # ---- Title ----
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkred)
    c.drawString(2 * cm, height - 2.5 * cm, "RAW SUGAR")

    # ---- Description ----
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.black)
    desc = c.beginText(2 * cm, height - 4 * cm)
    description_lines = [
        "Description:",
        "",
        "• Raw sugar is partially refined sugar with ",
        "natural molasses content,",
        "  giving it a distinct color and flavor.",
        "• It is used in sugar refining, bakeries, ",
        "confectioneries, and specialty foods.",
        "• Suitable for industrial and limited direct consumption.",
        "• Its versatility makes it suitable for both ,",
        "industrial and limited direct consumption"
    ]
    for line in description_lines:
        desc.textLine(line)
    c.drawText(desc)

    # ---- Specs ----
    c.setFont("Helvetica-Bold", 12)
    spec = c.beginText(11.5 * cm, height - 11 * cm)  # aligned lower so it’s next to the tall image
    spec_lines = [
        "Specifications:",
        "",
        "• Brownish crystals",
        "• Color: Light Brown",
        "• Moisture: Max 0.10%",
        "• Polarity: 98.50% Min",
        "• ICUMSA: 600–1200",
        "• Ash Content: Max 0.25%",
        "• Grain Size: Medium",
        "• HS Code: 1709671"
    ]
    for line in spec_lines:
        spec.textLine(line)
    c.drawText(spec)

    # ---- Image Paths ----
    left_image = r"C:\Users\Lenovo\OneDrive\Desktop\Mann\catalog_images\raw231.jpg"   # Tall Left
    top_right_image = r"C:\Users\Lenovo\OneDrive\Desktop\Mann\catalog_images\raw12.jpg"
    bottom_right_image = r"C:\Users\Lenovo\OneDrive\Desktop\Mann\catalog_images\su2.jpg"

    # ---- Left Image (Tall) ----
    if os.path.exists(left_image):
        c.drawImage(
            ImageReader(left_image),
            x=2 * cm, y=4 * cm,
            width=7 * cm, height=15 * cm,
            preserveAspectRatio=True
        )

    # ---- Top-Right Image ----
    if os.path.exists(top_right_image):
        c.drawImage(
            ImageReader(top_right_image),
            x=11.5 * cm, y=height - 6 * cm,
            width=12 * cm, height=5 * cm,
            preserveAspectRatio=True
        )

    # ---- Bottom-Right Image ----
    if os.path.exists(bottom_right_image):
        c.drawImage(
            ImageReader(bottom_right_image),
            x=11.5 * cm, y=4 * cm,
            width=8.5 * cm, height=7 * cm,
            preserveAspectRatio=True
        )

    # ---- Footer ----
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.gray)
    c.drawString(2 * cm, 1.2 * cm, "© 2025 Mann Foods • www.mannfoods.in")

    c.showPage()
    c.save()
    buffer.seek(0)

    return Response(
        content=buffer.read(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
=======
from fastapi import FastAPI, Response
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
    width, height = A4

    # ---- Title ----
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkred)
    c.drawString(2 * cm, height - 2.5 * cm, "RAW SUGAR")

    # ---- Description ----
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.black)
    desc = c.beginText(2 * cm, height - 4 * cm)
    description_lines = [
        "Description:",
        "",
        "• Raw sugar is partially refined sugar with ",
        "natural molasses content,",
        "  giving it a distinct color and flavor.",
        "• It is used in sugar refining, bakeries, ",
        "confectioneries, and specialty foods.",
        "• Suitable for industrial and limited direct consumption.",
        "• Its versatility makes it suitable for both ,",
        "industrial and limited direct consumption"
    ]
    for line in description_lines:
        desc.textLine(line)
    c.drawText(desc)

    # ---- Specs ----
    c.setFont("Helvetica-Bold", 12)
    spec = c.beginText(11.5 * cm, height - 11 * cm)  # aligned lower so it’s next to the tall image
    spec_lines = [
        "Specifications:",
        "",
        "• Brownish crystals",
        "• Color: Light Brown",
        "• Moisture: Max 0.10%",
        "• Polarity: 98.50% Min",
        "• ICUMSA: 600–1200",
        "• Ash Content: Max 0.25%",
        "• Grain Size: Medium",
        "• HS Code: 1709671"
    ]
    for line in spec_lines:
        spec.textLine(line)
    c.drawText(spec)

    # ---- Image Paths ----
    left_image = r"C:\Users\Lenovo\OneDrive\Desktop\Mann\catalog_images\raw231.jpg"   # Tall Left
    top_right_image = r"C:\Users\Lenovo\OneDrive\Desktop\Mann\catalog_images\raw12.jpg"
    bottom_right_image = r"C:\Users\Lenovo\OneDrive\Desktop\Mann\catalog_images\su2.jpg"

    # ---- Left Image (Tall) ----
    if os.path.exists(left_image):
        c.drawImage(
            ImageReader(left_image),
            x=2 * cm, y=4 * cm,
            width=7 * cm, height=15 * cm,
            preserveAspectRatio=True
        )

    # ---- Top-Right Image ----
    if os.path.exists(top_right_image):
        c.drawImage(
            ImageReader(top_right_image),
            x=11.5 * cm, y=height - 6 * cm,
            width=12 * cm, height=5 * cm,
            preserveAspectRatio=True
        )

    # ---- Bottom-Right Image ----
    if os.path.exists(bottom_right_image):
        c.drawImage(
            ImageReader(bottom_right_image),
            x=11.5 * cm, y=4 * cm,
            width=8.5 * cm, height=7 * cm,
            preserveAspectRatio=True
        )

    # ---- Footer ----
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.gray)
    c.drawString(2 * cm, 1.2 * cm, "© 2025 Mann Foods • www.mannfoods.in")

    c.showPage()
    c.save()
    buffer.seek(0)

    return Response(
        content=buffer.read(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
>>>>>>> fd32d464763a6b4ada6b435112fdaae2f364e6ed
