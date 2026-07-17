from reportlab.pdfgen import canvas
from io import BytesIO
def create_pdf(data):
    buffer = BytesIO()
    pdf = canvas.Canvas(
        buffer  )
    pdf.setFont(
        "Helvetica",
        12   )
    y = 800
    pdf.drawString(
        100,
        y,
        "BAO CAO THAM DINH CHO VAY"  )
    y -= 40
    for key,value in data.items():
        pdf.drawString(
            100,
            y,
            f"{key}: {value}"    )
        y -= 25
    pdf.save()
    buffer.seek(0)
    return buffer
