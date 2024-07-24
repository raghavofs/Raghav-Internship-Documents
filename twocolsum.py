import PyPDF2
import gpt4all
import os
import nltk
from tqdm import tqdm
import re
import fitz
import pytesseract
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

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

def chunk_text_by_subheadings(text):
   
    subheading_pattern = re.compile(r'\n([A-Z][a-zA-Z\s]{0,4})\n')
    subheading_chunks = subheading_pattern.split(text)
    
  
    chunks = []
    current_chunk = ""
    for i, chunk in enumerate(subheading_chunks):
        if i % 2 == 0:
            current_chunk += chunk
        else:
            current_chunk += chunk + "\n"
            chunks.append(current_chunk.strip())
            current_chunk = ""
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

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

def nested_chunk_text(text, max_tokens):
    
    subheading_chunks = chunk_text_by_subheadings(text)
    all_chunks = []
    for subheading_chunk in subheading_chunks:
        token_chunks = chunk_text_by_tokens(subheading_chunk, max_tokens)
        all_chunks.extend(token_chunks)
    return all_chunks

def summarize_text_with_gpt4all(text, model, max_words=150):

    prompt = f"Summarize the following text in detail, including all key points, important details, and maintaining the original meaning as much as possible. Ensure the summary is comprehensive and retains the essence of the content. If there are case studies, reproduce them in a better way. Maximum Length = {max_words} words.:\n\n{text}\n\nDetailed and Comprehensive Summary:"

    summary = model.generate(prompt)
    
    
    summary_words = summary.strip().split()
    truncated_summary = ' '.join(summary_words[:max_words])
    
    return truncated_summary

def write_pdf(text_chunks, output_path):
    
    c = canvas.Canvas(output_path, pagesize=letter)
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

def main(input_pdf, output_pdf, is_handwritten, is_two_column=False):
    try:
        if is_handwritten:
            text = read_handwritten_pdf(input_pdf, is_two_column)
        else:
            text = read_computerized_pdf(input_pdf, is_two_column)
        
        
        max_tokens_per_chunk = 200
        
        
        token_chunks = chunk_text_by_tokens(text, max_tokens_per_chunk)
        
        model_path = "/Users/raghavsubramaniam/Library/Application Support/nomic.ai/GPT4All"
        model_file = "Hermes.gguf"  
        
        model = gpt4all.GPT4All(model_name="hermes", model_path=model_path, allow_download=False)
        
        summarized_texts = []
        with tqdm(total=len(token_chunks), desc="Summarizing Chunks") as pbar:
            for chunk in token_chunks:
                summary = summarize_text_with_gpt4all(chunk, model, max_words=150)  
                if isinstance(summary, bytes):
                    summary = summary.decode("utf-8")
                summarized_texts.append(summary)
                pbar.update(1)
        print(summarized_texts)
        
        write_pdf(summarized_texts, output_pdf)
    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_pdf_path = "/Users/raghavsubramaniam/Desktop/ied.pdf"
    output_pdf_path = "/Users/raghavsubramaniam/Desktop/output.pdf"
    

    print("Select the type of PDF:")
    print("1. Handwritten")
    print("2. Computerized (Typed)")
    pdf_type = input("Enter your choice (1 or 2): ")
    
    if pdf_type == "1":
        is_handwritten = True
    elif pdf_type == "2":
        is_handwritten = False
    else:
        print("Invalid choice. Exiting.")
        exit()
    
   
    print("Is the PDF in two-column format?")
    print("1. Yes")
    print("2. No")
    column_choice = input("Enter your choice (1 or 2): ")
    if column_choice == "1":
        is_two_column = True
    elif column_choice == "2":
        is_two_column = False
    else:
        print("Invalid choice. Exiting.")
        exit()
    
    main(input_pdf_path, output_pdf_path, is_handwritten, is_two_column)
