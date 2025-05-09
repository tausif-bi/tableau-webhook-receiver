from flask import Flask, request, jsonify, redirect
import logging
from datetime import datetime
import urllib.parse

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
        final_url = f"{base_url}?Region={encoded_region}"
        
        # Log the redirect URL
        logging.info(f"Redirecting to: {final_url}")
        
        # Redirect to the Tableau PDF URL
        return redirect(final_url)
        
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 