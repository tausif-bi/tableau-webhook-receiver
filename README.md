# Tableau Webhook Receiver

This Flask application receives and processes URL actions from Tableau, capturing sheet names and filter parameters.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the server:
```bash
python app.py
```

The server will run on port 5000 by default.

## Tableau URL Action Format

Use the following URL format in your Tableau URL action:
```
http://your-vps-ip:5000/tableau-webhook?sheet_name={sheet_name}&filter_name={filter_name}
```

Replace `your-vps-ip` with your VPS machine's IP address or domain name.

## Logging

The application logs all received requests to `tableau_requests.log` in the project directory. 