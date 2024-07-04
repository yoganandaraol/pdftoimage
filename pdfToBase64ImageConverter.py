import fitz  # PyMuPDF
from PIL import Image
import base64
import io

def pdf_page_to_base64(pdf_path, page_number):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Get the specified page
    page = pdf_document.load_page(page_number - 1)  # Page numbers are 0-based in PyMuPDF
    
    # Render the page to a pixmap
    pix = page.get_pixmap()
    
    # Convert the pixmap to an image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Save the image to a bytes buffer
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    
    # Encode the bytes buffer to a base64 string
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return img_str
