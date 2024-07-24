from flask import Flask, render_template, request, send_file, jsonify
import PyPDF2
import os
import fitz
import pytesseract
import nltk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from io import BytesIO
from tqdm import tqdm
import re
import google.generativeai as genai

nltk.download('punkt')

app = Flask(__name__)

# Configure the Google API key
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

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

def chunk_text_by_tokens(text, max_tokens):
    tokens = nltk.word_tokenize(text)
    chunks = []
    current_chunk = []
    current_chunk_tokens = 0
    for token in tokens:
        current_chunk.append(token)
        current_chunk_tokens += 1
        if current_chunk_tokens >= max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_chunk_tokens = 0
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def summarize_text_with_gemini_api(text, max_words=150):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([f"Summarize the following text in detail, including all key points, important details, and maintaining the original meaning as much as possible. Ensure the summary is comprehensive and retains the essence of the content:\n\n{text}\n\nDetailed and Comprehensive Summary"])
    summary = response.text
    summary_words = summary.strip().split()
    truncated_summary = ' '.join(summary_words[:max_words])
    return truncated_summary

def write_pdf(text_chunks):
    output = BytesIO()
    c = canvas.Canvas(output, pagesize=letter)
    width, height = letter
    x, y = 30, height - 40
    for chunk in text_chunks:
        paragraphs = chunk.split('\n')
        for paragraph in paragraphs:
            lines = simpleSplit(paragraph, c._fontname, c._fontsize, width - 60)
            for line in lines:
                c.drawString(x, y, line)
                y -= 15
                if y < 40:
                    c.showPage()
                    c.setFont(c._fontname, c._fontsize)
                    y = height - 40
                    x = 30
            y -= 15
            if y < 40:
                c.showPage()
                c.setFont(c._fontname, c._fontsize)
                y = height - 40
                x = 30
    c.save()
    output.seek(0)
    return output

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_pdf = request.files["input_pdf"]
        pdf_type = request.form["pdf_type"]
        is_two_column = request.form.get("is_two_column") == "on"
        is_handwritten = pdf_type == "handwritten"
        
        input_pdf_path = os.path.join("uploads", input_pdf.filename)
        input_pdf.save(input_pdf_path)
        
        try:
            if is_handwritten:
                text = read_handwritten_pdf(input_pdf_path, is_two_column)
            else:
                text = read_computerized_pdf(input_pdf_path, is_two_column)
            
            max_tokens_per_chunk = 200
            token_chunks = chunk_text_by_tokens(text, max_tokens_per_chunk)
            total_chunks = len(token_chunks)
            
            summarized_texts = []
            for i, chunk in enumerate(token_chunks):
                summary = summarize_text_with_gemini_api(chunk, max_words=150)
                summarized_texts.append(summary)
                
                # Send progress update to client
                progress = int((i + 1) / total_chunks * 100)
                progress_data = {'progress': progress}
                yield jsonify(progress_data)
            
            output_pdf = write_pdf(summarized_texts)
            
            return send_file(output_pdf, as_attachment=True, download_name="output.pdf", mimetype="application/pdf")
        except Exception as e:
            return f"An error occurred: {e}"
    
    return render_template("index.html")

@app.route("/Downloads")
def download():
    try:
        output_pdf = write_pdf([])  # Provide an empty list or any default content if needed
        return send_file(output_pdf, as_attachment=True, download_name="output.pdf", mimetype="application/pdf")
    except Exception as e:
        return f"An error occurred during download: {e}"

if __name__ == "__main__":
    app.run(debug=True)
