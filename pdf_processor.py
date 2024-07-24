import os
import PyPDF2
import fitz
import pytesseract
import nltk
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate
from tqdm import tqdm
import google.generativeai as genai
import re

# Uncomment the line below to download NLTK data if you haven't already
# nltk.download('punkt')

# Configure the Google API key
genai.configure(api_key=os.getenv("AIzaSyB3OuBGlqQNJNmjR0FwNBf3hcrPXE_r50w"))

def read_computerized_pdf(file_path, is_two_column=False):
    pdf = PyPDF2.PdfReader(open(file_path, 'rb'))
    text = ""
    for page_num in range(len(pdf.pages)):
        page_text = pdf.pages[page_num].extract_text()
        if is_two_column:
            lines = page_text.split('\n')
            mid_index = len(lines) // 2
            left_text = '\n'.join(lines[:mid_index])
            right_text = '\n'.join(lines[mid_index:])
            page_text = left_text + '\n' + right_text
        text += page_text + "\n"
    return text

def read_handwritten_pdf(file_path, is_two_column=False):
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        if is_two_column:
            left_half = img.crop((0, 0, img.width // 2, img.height))
            right_half = img.crop((img.width // 2, 0, img.width, img.height))
            left_text = pytesseract.image_to_string(left_half, lang='eng')
            right_text = pytesseract.image_to_string(right_half, lang='eng')
            page_text = left_text + "\n" + right_text
        else:
            page_text = pytesseract.image_to_string(img, lang='eng')
        text += page_text + "\n"
    return text

def detect_subheadings(text):
    # Using regular expressions to find lines that may serve as subheadings
    lines = text.split('\n')
    subheadings = []
    block = []
    for line in lines:
        if re.match(r'^[A-Z][a-z]+(?:\s[A-Z][a-z]+){0,5}$', line):  # Capitalized lines with up to 7 words
            if block:
                subheadings.append('\n'.join(block))
                block = []
            block.append(line)
        else:
            block.append(line)
    if block:
        subheadings.append('\n'.join(block))
    return subheadings

def chunk_text_by_tokens(text, max_tokens, progress_callback=None):
    tokens = nltk.word_tokenize(text)
    chunks = []
    current_chunk = []
    current_chunk_tokens = 0
    total_tokens = len(tokens)
    for i, token in enumerate(tokens):
        current_chunk.append(token)
        current_chunk_tokens += 1
        if current_chunk_tokens >= max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_chunk_tokens = 0
        if progress_callback:
            # Update progress as a percentage
            progress_callback(int((i + 1) / total_tokens * 100))
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def summarize_text_with_gemini_api(text, max_words=150):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([f"Do not use bold text or formatted text. Make it plain. Summarize the following text in detail, including all key points, important details, and maintaining the original meaning as much as possible. Ensure the summary is comprehensive and retains the essence of the content:\n\n{text}\n\nDetailed and Comprehensive Summary"])
    summary = response.text
    summary_words = summary.strip().split()
    truncated_summary = ' '.join(summary_words[:max_words])
    return truncated_summary

def write_pdf(text_chunks, output_path):
    # Create a PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define custom styles
    title_style = styles['Title']
    normal_style = styles['Normal']
    bullet_style = ParagraphStyle(name='BulletStyle', parent=styles['Normal'], bulletFontName='Helvetica', bulletFontSize=10, leftIndent=20, spaceBefore=10)
    
    # Define a style for bold text
    bold_style = ParagraphStyle(name='BoldStyle', parent=styles['Normal'], fontName='Helvetica-Bold')

    # Prepare the content
    content = []

    for chunk in text_chunks:
        # Split the text into paragraphs
        paragraphs = chunk.split('\n')
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # Detect and handle bold text
            if '**' in para:
                parts = para.split('**')
                formatted_text = ''
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        formatted_text += f'<b>{part}</b>'
                    else:
                        formatted_text += part
                para = formatted_text

            # Add content to the PDF
            if para.startswith('* '):  # Bullet point detection
                para = para[2:]  # Remove the bullet character
                bullet_paragraph = Paragraph(f'• {para}', bullet_style)
                content.append(bullet_paragraph)
            else:
                # Check for bold formatting
                if '<b>' in para:
                    p = Paragraph(para, bold_style)
                else:
                    p = Paragraph(para, normal_style)
                content.append(p)

        content.append(Paragraph('<br/><br/>', normal_style))  # Add spacing between chunks
    
    # Build the PDF
    doc.build(content)

def main(input_pdf_path, output_pdf_path, is_handwritten, is_two_column, progress_callback=None):
    try:
        if is_handwritten:
            text = read_handwritten_pdf(input_pdf_path, is_two_column)
        else:
            text = read_computerized_pdf(input_pdf_path, is_two_column)

        # Detect subheadings and block text
        subheading_blocks = detect_subheadings(text)

        summarized_texts = []
        for block in subheading_blocks:
            max_tokens_per_chunk = 500
            token_chunks = chunk_text_by_tokens(block, max_tokens_per_chunk, progress_callback)

            for chunk in token_chunks:
                summary = summarize_text_with_gemini_api(chunk, max_words=250)
                summarized_texts.append(summary)

        # Use the updated write_pdf function
        write_pdf(summarized_texts, output_pdf_path)

        print("PDF summarization and writing complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_pdf_path = "/path/to/input.pdf"   
    output_pdf_path = "/path/to/output.pdf" 
    is_handwritten = False 
    is_two_column = False  

    main(input_pdf_path, output_pdf_path, is_handwritten, is_two_column)
