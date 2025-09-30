#!/usr/bin/env python3
"""
Leneda Energy Dashboard - Backend Server (Pure Python stdlib)
Version: 1.0.0
License: GPL-3.0

NO EXTERNAL DEPENDENCIES - Uses only Python standard library
"""

import os
import json
import logging
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse, parse_qs
import mimetypes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG_FILE = '/data/options.json'
LENEDA_API_BASE = 'https://api.leneda.eu/api'
STATIC_DIR = '/app/static'


def load_config():
    """Load addon configuration"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            logger.warning(f"Config file not found: {CONFIG_FILE}")
            return {
                'api_key': '',
                'energy_id': '',
                'metering_points': [],
                'billing': {},
                'display': {'theme': 'dark'}
            }
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {}


def make_api_request(url, headers=None, method='GET', data=None):
    """Make HTTP request using urllib"""
    try:
        req = Request(url, headers=headers or {}, method=method)
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except (URLError, HTTPError) as e:
        logger.error(f"Request error for {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None


class LenedaHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Leneda dashboard"""
    
    def log_message(self, format, *args):
        """Override to use proper logging"""
        logger.info("%s - %s" % (self.address_string(), format % args))
    
    def send_json(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_file(self, filepath):
        """Send file response"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            mime_type, _ = mimetypes.guess_type(filepath)
            self.send_response(200)
            self.send_header('Content-Type', mime_type or 'application/octet-stream')
            self.send_header('Cache-Control', 'public, max-age=3600')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, 'File not found')
        except Exception as e:
            logger.error(f"Error serving file {filepath}: {e}")
            self.send_error(500, 'Internal server error')
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        # API endpoints
        if path == '/api/health':
            self.send_json({
                'status': 'healthy',
                'version': '0.1.0',
                'timestamp': datetime.now().isoformat()
            })
        
        elif path == '/api/config':
            config = load_config()
            # Remove sensitive data
            safe_config = {
                'has_api_key': bool(config.get('api_key')),
                'has_energy_id': bool(config.get('energy_id')),
                'metering_points': config.get('metering_points', []),
                'billing': config.get('billing', {}),
                'display': config.get('display', {})
            }
            self.send_json(safe_config)
        
        elif path == '/api/metering-data':
            self.handle_metering_data()
        
        elif path == '/api/aggregated-data':
            self.handle_aggregated_data()
        
        elif path == '/api/calculate-invoice':
            self.handle_calculate_invoice()
        
        # Static files
        elif path == '/' or path == '/index.html':
            self.send_file(os.path.join(STATIC_DIR, 'index.html'))
        
        elif path.startswith('/'):
            # Serve static files
            filepath = os.path.join(STATIC_DIR, path.lstrip('/'))
            if os.path.isfile(filepath):
                self.send_file(filepath)
            else:
                self.send_error(404, 'File not found')
        
        else:
            self.send_error(404, 'Not found')
    
    def handle_metering_data(self):
        """Handle metering data request"""
        config = load_config()
        api_key = config.get('api_key', '')
        energy_id = config.get('energy_id', '')
        
        if not api_key or not energy_id:
            self.send_json({'error': 'API credentials not configured'}, 400)
            return
        
        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        metering_point = query.get('metering_point', [None])[0]
        obis_code = query.get('obis_code', ['1-1:1.29.0'])[0]
        start_date = query.get('start_date', [None])[0]
        end_date = query.get('end_date', [None])[0]
        
        if not metering_point:
            self.send_json({'error': 'Missing metering_point parameter'}, 400)
            return
        
        # Default to last 24 hours if no dates provided
        if not start_date or not end_date:
            end_dt = datetime.now()
            start_dt = end_dt - timedelta(days=1)
            start_date = start_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_date = end_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Build URL with query parameters
        url = f"{LENEDA_API_BASE}/metering-points/{metering_point}/time-series"
        url += f"?startDateTime={start_date}&endDateTime={end_date}&obisCode={obis_code}"
        
        headers = {
            'X-API-KEY': api_key,
            'X-ENERGY-ID': energy_id,
            'Content-Type': 'application/json'
        }
        
        data = make_api_request(url, headers)
        
        if data:
            self.send_json(data)
        else:
            self.send_json({'error': 'Failed to fetch data from Leneda API'}, 500)
    
    def handle_aggregated_data(self):
        """Handle aggregated data request"""
        config = load_config()
        api_key = config.get('api_key', '')
        energy_id = config.get('energy_id', '')
        
        if not api_key or not energy_id:
            self.send_json({'error': 'API credentials not configured'}, 400)
            return
        
        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        metering_point = query.get('metering_point', [None])[0]
        obis_code = query.get('obis_code', ['1-1:1.29.0'])[0]
        start_date = query.get('start_date', [None])[0]
        end_date = query.get('end_date', [None])[0]
        aggregation_level = query.get('aggregation_level', ['Day'])[0]
        
        if not metering_point:
            self.send_json({'error': 'Missing metering_point parameter'}, 400)
            return
        
        # Default to last 30 days
        if not start_date or not end_date:
            end_dt = datetime.now()
            start_dt = end_dt - timedelta(days=30)
            start_date = start_dt.strftime('%Y-%m-%d')
            end_date = end_dt.strftime('%Y-%m-%d')
        
        # Build URL
        url = f"{LENEDA_API_BASE}/metering-points/{metering_point}/time-series/aggregated"
        url += f"?startDate={start_date}&endDate={end_date}&obisCode={obis_code}"
        url += f"&aggregationLevel={aggregation_level}&transformationMode=Accumulation"
        
        headers = {
            'X-API-KEY': api_key,
            'X-ENERGY-ID': energy_id,
            'Content-Type': 'application/json'
        }
        
        data = make_api_request(url, headers)
        
        if data:
            self.send_json(data)
        else:
            self.send_json({'error': 'Failed to fetch aggregated data'}, 500)
    
    def handle_calculate_invoice(self):
        """Handle invoice calculation"""
        config = load_config()
        billing = config.get('billing', {})
        api_key = config.get('api_key', '')
        energy_id = config.get('energy_id', '')
        
        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        metering_point = query.get('metering_point', [None])[0]
        start_date = query.get('start_date', [None])[0]
        end_date = query.get('end_date', [None])[0]
        
        if not metering_point or not start_date or not end_date:
            self.send_json({
                'error': 'Missing required parameters: metering_point, start_date, end_date'
            }, 400)
            return
        
        # Fetch consumption data
        url = f"{LENEDA_API_BASE}/metering-points/{metering_point}/time-series/aggregated"
        url += f"?startDate={start_date}&endDate={end_date}"
        url += "&obisCode=1-1:1.29.0&aggregationLevel=Infinite&transformationMode=Accumulation"
        
        headers = {
            'X-API-KEY': api_key,
            'X-ENERGY-ID': energy_id,
            'Content-Type': 'application/json'
        }
        
        data = make_api_request(url, headers)
        
        if not data:
            self.send_json({'error': 'Failed to fetch consumption data'}, 500)
            return
        
        # Extract total consumption
        total_kwh = 0
        if data.get('aggregatedTimeSeries'):
            total_kwh = data['aggregatedTimeSeries'][0].get('value', 0)
        
        # Calculate invoice components
        energy_fixed = billing.get('energy_fixed_fee_monthly', 1.50)
        energy_variable = total_kwh * billing.get('energy_variable_rate_per_kwh', 0.1500)
        network_metering = billing.get('network_metering_fee_monthly', 5.90)
        network_power_ref = billing.get('network_power_reference_fee_monthly', 19.27)
        network_variable = total_kwh * billing.get('network_variable_rate_per_kwh', 0.0759)
        exceedance = 0  # TODO: Calculate based on reference power
        compensation = total_kwh * billing.get('compensation_fund_rate_per_kwh', -0.0376)
        electricity_tax = total_kwh * billing.get('electricity_tax_per_kwh', 0.0010)
        
        subtotal = (energy_fixed + energy_variable + network_metering + 
                   network_power_ref + network_variable + exceedance + 
                   compensation + electricity_tax)
        
        vat_rate = billing.get('vat_rate', 0.08)
        vat_amount = subtotal * vat_rate
        total = subtotal + vat_amount
        
        invoice = {
            'period': {
                'start': start_date,
                'end': end_date
            },
            'consumption_kwh': round(total_kwh, 2),
            'breakdown': {
                'energy_fixed_fee': round(energy_fixed, 2),
                'energy_variable': round(energy_variable, 2),
                'network_metering_fee': round(network_metering, 2),
                'network_power_reference': round(network_power_ref, 2),
                'network_variable': round(network_variable, 2),
                'exceedance': round(exceedance, 2),
                'compensation_fund': round(compensation, 2),
                'electricity_tax': round(electricity_tax, 2)
            },
            'subtotal': round(subtotal, 2),
            'vat': {
                'rate': vat_rate,
                'amount': round(vat_amount, 2)
            },
            'total': round(total, 2),
            'currency': billing.get('currency', 'EUR')
        }
        
        self.send_json(invoice)


def main():
    """Start the HTTP server"""
    server_address = ('', 8099)
    httpd = HTTPServer(server_address, LenedaHandler)
    
    logger.info("=" * 60)
    logger.info("  Leneda Energy Dashboard - Starting Server")
    logger.info("=" * 60)
    logger.info("Version: 1.0.0")
    logger.info("License: GPL-3.0")
    logger.info(f"Server listening on: http://0.0.0.0:8099")
    logger.info(f"Static files: {STATIC_DIR}")
    logger.info(f"Config file: {CONFIG_FILE}")
    logger.info("=" * 60)
    logger.info("READY - No external dependencies required!")
    logger.info("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        httpd.shutdown()


if __name__ == '__main__':
    main()
