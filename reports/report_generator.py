from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime


def generate_report(material_name, stack, loads, A, B, D, filename="laminate_report.pdf"):

    c = canvas.Canvas(filename, pagesize=letter)

    width, height = letter

    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Composite Laminate Analysis Report")

    y -= 40

    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Material: {material_name}")
    y -= 20

    c.drawString(50, y, f"Stacking Sequence: {stack}")
    y -= 20

    c.drawString(50, y, f"Loads: {loads}")
    y -= 30

    c.drawString(50, y, "ABD Matrix")

    y -= 20

    for matrix, name in [(A,"A"),(B,"B"),(D,"D")]:

        c.drawString(50, y, f"{name} Matrix")

        y -= 20

        for row in matrix:

            c.drawString(70, y, str([round(v,3) for v in row]))

            y -= 20

        y -= 10

    y -= 20

    c.drawString(50, y, f"Generated: {datetime.datetime.now()}")

    c.save()
