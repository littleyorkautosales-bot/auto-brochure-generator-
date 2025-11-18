import csv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime

CSV_FILE = "inventory.csv"
PLACEHOLDER_IMAGE = "car_placeholder.png"

def fetch_inventory():
    cars = []
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cars.append({
                "title": f"{row['Year']} {row['Make']} {row['Model']}",
                "price": row['Price'],
                "mileage": row['Mileage'],
                "features": row.get('Features', '')
            })
    return cars

def generate_pdf(cars):
    styles = getSampleStyleSheet()
    pdf = SimpleDocTemplate("brochure.pdf")

    flow = []
    flow.append(Paragraph("<b>Little York Auto Sales – Inventory Brochure</b>", styles["Title"]))
    flow.append(Paragraph(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    flow.append(Spacer(1, 0.2*inch))

    for car in cars:
        # Add placeholder image
        img = Image(PLACEHOLDER_IMAGE, width=3*inch, height=1.5*inch)
        flow.append(img)
        flow.append(Spacer(1, 0.1*inch))
        
        # Add car info
        flow.append(Paragraph(f"<b>{car['title']}</b>", styles["Heading2"]))
        flow.append(Paragraph(f"Price: {car['price']}", styles["Normal"]))
        flow.append(Paragraph(f"Mileage: {car['mileage']}", styles["Normal"]))
        flow.append(Paragraph(f"Features: {car['features']}", styles["Normal"]))
        flow.append(Spacer(1, 0.3*inch))

    pdf.build(flow)

if __name__ == "__main__":
    cars = fetch_inventory()
    generate_pdf(cars)
