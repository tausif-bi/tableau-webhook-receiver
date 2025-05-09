from flask import Flask, request, jsonify, redirect, send_file
import logging
from datetime import datetime
import urllib.parse
import requests
import os
import uuid
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tableau_requests.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

# Create directories for storing PDFs
PDF_STORAGE = Path("pdf_storage")
PDF_STORAGE.mkdir(exist_ok=True)

def download_pdf(url):
    """Download PDF from Tableau URL"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        logging.error(f"Error downloading PDF: {str(e)}")
        return None

def save_pdf(pdf_content, filename):
    """Save PDF to local storage"""
    try:
        filepath = PDF_STORAGE / filename
        with open(filepath, 'wb') as f:
            f.write(pdf_content)
        return filepath
    except Exception as e:
        logging.error(f"Error saving PDF: {str(e)}")
        return None

def process_pdf_with_labeling_service(pdf_path):
    """Send PDF to labeling service and get processed PDF"""
    try:
        # TODO: Replace with your actual labeling service endpoint
        labeling_service_url = "http://your-labeling-service/process"
        
        with open(pdf_path, 'rb') as f:
            files = {'pdf': f}
            response = requests.post(labeling_service_url, files=files)
            response.raise_for_status()
            
            # Save the processed PDF
            processed_filename = f"processed_{pdf_path.name}"
            processed_path = PDF_STORAGE / processed_filename
            with open(processed_path, 'wb') as f:
                f.write(response.content)
            
            return processed_path
    except Exception as e:
        logging.error(f"Error processing PDF with labeling service: {str(e)}")
        return None

@app.route('/tableau-webhook', methods=['GET'])
def tableau_webhook():
    try:
        # Get all URL parameters
        params = request.args.to_dict()
        
        # Log the received parameters
        logging.info(f"Received Tableau request with parameters: {params}")
        
        # Extract specific parameters
        sheet_name = params.get('sheetname', 'Not provided')
        region = params.get('region', 'Not provided')
        
        # Log the extracted information
        logging.info(f"Sheet Name: {sheet_name}")
        logging.info(f"Region: {region}")
        
        # Construct the Tableau PDF URL
        base_url = "https://prod-apsoutheast-b.online.tableau.com/#/site/tausifkhan786-e219ba6206/views/pdftest/Overview.pdf"
        
        # URL encode the region parameter
        encoded_region = urllib.parse.quote(region)
        
        # Construct the final URL with the region parameter
        tableau_url = f"{base_url}?Region={encoded_region}"
        
        # Generate unique filename
        filename = f"{uuid.uuid4()}.pdf"
        
        # Download PDF from Tableau
        pdf_content = download_pdf(tableau_url)
        if not pdf_content:
            return jsonify({
                'status': 'error',
                'message': 'Failed to download PDF from Tableau'
            }), 500
        
        # Save PDF locally
        pdf_path = save_pdf(pdf_content, filename)
        if not pdf_path:
            return jsonify({
                'status': 'error',
                'message': 'Failed to save PDF locally'
            }), 500
        
        # Process PDF with labeling service
        processed_pdf_path = process_pdf_with_labeling_service(pdf_path)
        if not processed_pdf_path:
            return jsonify({
                'status': 'error',
                'message': 'Failed to process PDF with labeling service'
            }), 500
        
        # Return the processed PDF to the client
        return send_file(
            processed_pdf_path,
            as_attachment=True,
            download_name=f"labeled_{sheet_name}_{region}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 