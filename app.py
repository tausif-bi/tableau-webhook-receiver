from flask import Flask, request, jsonify
import logging
from datetime import datetime

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
        
        # Extract specific parameters (customize based on your needs)
        sheet_name = params.get('sheet_name', 'Not provided')
        filter_name = params.get('filter_name', 'Not provided')
        
        # Log the extracted information
        logging.info(f"Sheet Name: {sheet_name}")
        logging.info(f"Filter Name: {filter_name}")
        
        # You can add your custom processing logic here
        # For example, storing in a database, triggering other actions, etc.
        
        return jsonify({
            'status': 'success',
            'message': 'Parameters received successfully',
            'data': {
                'sheet_name': sheet_name,
                'filter_name': filter_name,
                'timestamp': datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 