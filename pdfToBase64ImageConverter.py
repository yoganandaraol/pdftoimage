from flask import Flask, request, jsonify
import fitz  # PyMuPDF
from PIL import Image
import base64
import io

app = Flask(__name__)

def pdf_page_to_base64(file_stream, page_number):
    # Open the PDF file from the file stream
    pdf_document = fitz.open(stream=file_stream, filetype="pdf")
    
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

@app.route('/convert', methods=['POST'])
def convert_pdf_page():
    try:
        pdf_file = request.files['pdf']
        page_number = int(request.form['page_number'])
        
        # Convert the specified page to a base64 string using the file stream
        base64_image = pdf_page_to_base64(pdf_file.stream, page_number)
        
        return jsonify({'base64_image': base64_image})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
