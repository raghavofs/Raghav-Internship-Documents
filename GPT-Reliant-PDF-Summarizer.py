from openai import OpenAI
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

api_key = "500293d613d84863bfcff567380fe4d1"
base_url = "https://api.aimlapi.com"
client = OpenAI(api_key=api_key, base_url=base_url)

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
    return text

def generate_summary(topic, content):
    # Example function to generate a summary for a given topic
    # This could be replaced with your AI assistant's logic
    return f"Summary for {topic}: {content[:200]}..."

def generate_summarized_pdf(pdf_path, output_pdf_path, unit, chapter, topics):
    # Extract text from PDF file (textbook)
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Create a PDF document
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    
    # Initialize coordinates for positioning text
    y = 750
    
    # Write the unit and chapter header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, y, f"Unit {unit}, Chapter {chapter}")
    y -= 20  # Move down the y-coordinate
    
    # Iterate through topics and generate summaries
    for topic in topics:
        # Generate a summary for the current topic
        summary = generate_summary(topic, pdf_text)
        
        # Write topic and summary to the PDF
        c.setFont("Helvetica", 12)
        c.drawString(120, y, f"Topic: {topic}")
        y -= 15  # Move down the y-coordinate
        
        c.drawString(120, y, f"Summary: {summary}")
        y -= 40  # Move down further for the next topic
        
        # Optional: Add more formatting or structure as needed
    
    # Save the PDF document
    c.save()

if __name__ == "__main__":
    # Example usage: Provide the path to your textbook PDF file and specify topics
    pdf_file = input("Enter path to your textbook PDF file: ").strip()
    output_pdf_file = input("Enter path for the output summarized PDF file: ").strip()
    
    if not os.path.exists(pdf_file):
        print(f"Error: PDF file '{pdf_file}' not found.")
    else:
        # Specify the unit, chapter, and topics of interest
        unit = input("Enter unit number: ").strip()
        chapter = input("Enter chapter number: ").strip()
        topics = input("Enter topics (comma-separated): ").strip().split(",")
        
        # Generate the summarized PDF
        generate_summarized_pdf(pdf_file, output_pdf_file, unit, chapter, topics)
        print(f"Summarized PDF generated: {output_pdf_file}")
