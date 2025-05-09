from flask import Flask, request, send_file
import logging
from pathlib import Path
import uuid
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('labeling_service.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

# Create directories for storing PDFs
PDF_STORAGE = Path("labeling_storage")
PDF_STORAGE.mkdir(exist_ok=True)

def add_label_to_pdf(pdf_path, label_text):
    """Add a label to the PDF"""
    try:
        # Read the original PDF
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        # Create a new PDF with the label
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 12)
        can.drawString(50, 50, label_text)  # Position the label
        can.save()
        packet.seek(0)
        label_pdf = PdfReader(packet)

        # Add the label to each page
        for page in reader.pages:
            page.merge_page(label_pdf.pages[0])
            writer.add_page(page)

        # Save the result
        output_path = PDF_STORAGE / f"labeled_{pdf_path.name}"
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        return output_path
    except Exception as e:
        logging.error(f"Error adding label to PDF: {str(e)}")
        return None

@app.route('/process', methods=['POST'])
def process_pdf():
    try:
        if 'pdf' not in request.files:
            return {'error': 'No PDF file provided'}, 400

        pdf_file = request.files['pdf']
        if pdf_file.filename == '':
            return {'error': 'No selected file'}, 400

        # Save the uploaded PDF
        filename = f"{uuid.uuid4()}.pdf"
        pdf_path = PDF_STORAGE / filename
        pdf_file.save(pdf_path)

        # Get label text from request (you can customize this)
        label_text = request.form.get('label_text', 'Processed by Labeling Service')
        
        # Add label to PDF
        processed_pdf_path = add_label_to_pdf(pdf_path, label_text)
        if not processed_pdf_path:
            return {'error': 'Failed to process PDF'}, 500

        # Return the processed PDF
        return send_file(
            processed_pdf_path,
            as_attachment=True,
            download_name=f"labeled_{pdf_file.filename}",
            mimetype='application/pdf'
        )

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)  # Using port 5001 to avoid conflict with main app 