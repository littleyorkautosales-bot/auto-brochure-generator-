import requests
from bs4 import BeautifulSoup
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

URL = "https://www.littleyorkautosales.com/inventory/"

def fetch_inventory():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "lxml")

    cars = []

    items = soup.select(".inventory-item")  # Adjust this selector if needed

    for item in items:
        title = item.select_one(".title").text.strip()
        price = item.select_one(".price").text.strip()
        mileage = item.select_one(".mileage").text.strip()

        cars.append({
            "title": title,
            "price": price,
            "mileage": mileage
        })

    return cars

def generate_pdf(cars):
    styles = getSampleStyleSheet()
    pdf = SimpleDocTemplate("brochure.pdf")

    flow = []
    flow.append(Paragraph("<b>Little York Auto Sales – Inventory Brochure</b>", styles["Title"]))
    flow.append(Paragraph(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    flow.append(Paragraph("<br/><br/>", styles["Normal"]))

    for car in cars:
        flow.append(Paragraph(f"<b>{car['title']}</b>", styles["Heading2"]))
        flow.append(Paragraph(f"Price: {car['price']}", styles["Normal"]))
        flow.append(Paragraph(f"Mileage: {car['mileage']}", styles["Normal"]))
        flow.append(Paragraph("<br/>", styles["Normal"]))

    pdf.build(flow)

if __name__ == "__main__":
    cars = fetch_inventory()
    generate_pdf(cars)
