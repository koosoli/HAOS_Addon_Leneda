#!/usr/bin/env python3
"""
Leneda Energy Dashboard - Backend Server (Pure Python stdlib)
Version: 1.0.8
License: GPL-3.0

NO EXTERNAL DEPENDENCIES - Uses only Python standard library

Changelog v1.0.3:
- Added comprehensive debug logging with emojis for easy identification
- Enhanced error messages with specific troubleshooting hints
- Detailed API request/response logging
- Configuration validation with clear status indicators
- Better credential validation and format checking
- Network error categorization and suggestions

Changelog v1.0.2:
- Fixed URL encoding for OBIS codes and metering point parameters
- Enhanced error handling and logging for API requests
- Fixed date formatting issues (now properly requests yesterday's data)
- Added support for multiple config file paths
- Improved HTTP headers for API requests
- Fixed frontend JavaScript logging error
"""

import os
import json
import logging
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse, parse_qs, quote, urlencode
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
        # Try production path first, then test path
        config_paths = [CONFIG_FILE, 'test_options.json', './test_options.json']
        
        logger.info("🔧 Loading configuration...")
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                logger.info(f"📁 Found config file: {config_path}")
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    
                # Log configuration details (safely)
                api_key = config.get('api_key', '')
                energy_id = config.get('energy_id', '')
                metering_points = config.get('metering_points', [])
                
                logger.info(f"✅ Config loaded successfully from: {config_path}")
                logger.info(f"🔑 API key present: {bool(api_key and api_key != 'your-test-api-key')}")
                if api_key and api_key != 'your-test-api-key':
                    logger.info(f"🔑 API key format: {api_key[:8]}...{api_key[-4:]} (length: {len(api_key)})")
                else:
                    logger.warning(f"🔑 API key value: '{api_key}' (placeholder or empty)")
                    
                logger.info(f"🆔 Energy ID present: {bool(energy_id and energy_id != 'your-test-energy-id')}")
                if energy_id and energy_id != 'your-test-energy-id':
                    logger.info(f"🆔 Energy ID: {energy_id}")
                else:
                    logger.warning(f"🆔 Energy ID value: '{energy_id}' (placeholder or empty)")
                    
                logger.info(f"📊 Metering points configured: {len(metering_points)}")
                for i, mp in enumerate(metering_points):
                    code = mp.get('code', '')
                    name = mp.get('name', 'Unnamed')
                    logger.info(f"📊 Meter {i+1}: '{name}' -> {code}")
                    if code == 'LU000000000000000000000000000000':
                        logger.warning(f"📊 Meter {i+1} uses placeholder code!")
                
                return config
        
        logger.error(f"❌ No config file found in paths: {config_paths}")
        logger.error("❌ This will cause the dashboard to show 'API credentials not configured'")
        return {
            'api_key': '',
            'energy_id': '',
            'metering_points': [],
            'billing': {},
            'display': {'theme': 'dark'}
        }
    except Exception as e:
        logger.error(f"💥 Error loading config: {e}")
        return {}


def make_api_request(url, headers=None, method='GET', data=None):
    """Make HTTP request using urllib with robust error handling"""
    try:
        logger.info(f"🌐 Making {method} request to Leneda API")
        logger.info(f"🌐 URL: {url}")
        logger.info(f"🌐 Headers: {dict(headers) if headers else 'None'}")
        
        req = Request(url, headers=headers or {}, method=method)
        if data:
            req.data = json.dumps(data).encode('utf-8')
            logger.info(f"🌐 Request body: {json.dumps(data, indent=2)}")
        
        logger.info(f"🌐 Sending request with {15}s timeout...")
        # Use shorter timeout to avoid hanging
        with urlopen(req, timeout=15) as response:
            response_data = response.read().decode('utf-8')
            logger.info(f"✅ API response status: {response.status}")
            logger.info(f"✅ Response headers: {dict(response.headers)}")
            logger.info(f"✅ Response size: {len(response_data)} characters")
            
            try:
                parsed_data = json.loads(response_data)
                
                # Log response structure
                if isinstance(parsed_data, dict):
                    if 'items' in parsed_data:
                        logger.info(f"📊 Response contains {len(parsed_data['items'])} data items")
                        if parsed_data['items']:
                            first_item = parsed_data['items'][0]
                            logger.info(f"📊 First item sample: {json.dumps(first_item, indent=2)[:200]}...")
                    elif 'aggregatedTimeSeries' in parsed_data:
                        logger.info(f"📊 Response contains {len(parsed_data['aggregatedTimeSeries'])} aggregated items")
                        if parsed_data['aggregatedTimeSeries']:
                            first_item = parsed_data['aggregatedTimeSeries'][0]
                            logger.info(f"📊 First aggregated item: {json.dumps(first_item, indent=2)}")
                    else:
                        logger.info(f"📊 Response structure: {list(parsed_data.keys()) if isinstance(parsed_data, dict) else type(parsed_data)}")
                
                logger.debug(f"📊 Full response: {response_data[:1000]}...")  # Log first 1000 chars
                return parsed_data
                
            except json.JSONDecodeError as je:
                logger.error(f"💥 JSON decode error: {je}")
                logger.error(f"💥 Raw response: {response_data[:500]}...")
                return None
                
    except URLError as e:
        logger.error(f"🌐 Network error for {url}: {e}")
        logger.error(f"🌐 This could be:")
        logger.error(f"🌐   - DNS resolution issue (can't reach api.leneda.eu)")
        logger.error(f"🌐   - Network connectivity problem")
        logger.error(f"🌐   - Firewall blocking HTTPS requests")
        return None
    except HTTPError as e:
        logger.error(f"🌐 HTTP error for {url}: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            logger.error(f"🌐 Error response body: {error_body}")
            
            if e.code == 401:
                logger.error(f"🔑 401 Unauthorized - Check your credentials:")
                logger.error(f"🔑   - API key might be invalid or expired")
                logger.error(f"🔑   - Energy ID might be wrong")
                logger.error(f"🔑   - Account might not have API access")
            elif e.code == 404:
                logger.error(f"📊 404 Not Found - Check your metering point code")
            elif e.code == 429:
                logger.error(f"⏱️ 429 Rate Limited - Too many requests, slow down")
                
        except Exception as ee:
            logger.error(f"🌐 Could not read error body: {ee}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"💥 JSON decode error: {e}")
        return None
    except Exception as e:
        logger.error(f"💥 Unexpected error for {url}: {type(e).__name__}: {e}")
        import traceback
        logger.error(f"💥 Traceback: {traceback.format_exc()}")
        return None


class LenedaHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Leneda dashboard"""
    
    def log_message(self, format, *args):
        """Override to use proper logging"""
        logger.info("🌐 %s - %s" % (self.address_string(), format % args))
    
    def send_json(self, data, status=200):
        """Send JSON response with cache busting"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        # NUCLEAR CACHE BUSTING for API responses too
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()
        response_json = json.dumps(data)
        self.wfile.write(response_json.encode('utf-8'))
        logger.info(f"📡 Sent JSON response ({len(response_json)} chars) with cache busting")
    
    def send_file(self, filepath):
        """Send file response with aggressive cache busting"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            mime_type, _ = mimetypes.guess_type(filepath)
            self.send_response(200)
            self.send_header('Content-Type', mime_type or 'application/octet-stream')
            
            # NUCLEAR CACHE BUSTING - Force browsers to reload everything
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.send_header('Last-Modified', 'Thu, 01 Jan 1970 00:00:00 GMT')
            self.send_header('ETag', f'"{hash(content)}-1.0.7"')
            
            self.end_headers()
            self.wfile.write(content)
            logger.info(f"🗂️ Served file {filepath} with NUCLEAR cache busting")
        except FileNotFoundError:
            self.send_error(404, 'File not found')
        except Exception as e:
            logger.error(f"Error serving file {filepath}: {e}")
            self.send_error(500, 'Internal server error')
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        logger.info(f"🌐 GET request: {self.path}")
        
        # API endpoints
        if path == '/api/health':
            logger.info("🔧 Health check requested")
            # Simple health check - no external dependencies
            self.send_json({
                'status': 'healthy',
                'version': '1.0.8',
                'timestamp': datetime.now().isoformat()
            })
        
        elif path == '/api/debug':
            logger.info("🔧 === DEBUG API REQUEST ===")
            config = load_config()
            
            debug_info = {
                'server_version': '1.0.8',
                'timestamp': datetime.now().isoformat(),
                'config_file_exists': os.path.exists(CONFIG_FILE),
                'config_file_path': CONFIG_FILE,
                'raw_config_keys': list(config.keys()) if config else [],
                'api_key_length': len(config.get('api_key', '')),
                'energy_id_value': config.get('energy_id', ''),
                'metering_points_count': len(config.get('metering_points', [])),
                'request_headers': dict(self.headers),
                'client_address': str(self.client_address)
            }
            
            logger.info(f"🔧 Debug info: {json.dumps(debug_info, indent=2)}")
            self.send_json(debug_info)
        
        elif path == '/api/config':
            logger.info(f"🔧 Request from: {self.client_address}")
            logger.info(f"🔧 User-Agent: {self.headers.get('User-Agent', 'Unknown')}")
            
            config = load_config()
            
            # Prepare safe config for frontend (without sensitive data)
            api_key = config.get('api_key', '')
            energy_id = config.get('energy_id', '')
            metering_points = config.get('metering_points', [])
            
            # Check if credentials are real (not placeholders)
            has_real_api_key = bool(api_key and api_key.strip() and api_key != 'your-test-api-key')
            has_real_energy_id = bool(energy_id and energy_id.strip() and energy_id != 'your-test-energy-id')
            
            logger.info(f"🔧 Raw config values:")
            logger.info(f"🔧   - API key length: {len(api_key)} chars")
            logger.info(f"🔧   - API key starts with: '{api_key[:10]}...' (showing first 10 chars)")
            logger.info(f"🔧   - Energy ID: '{energy_id}'")
            logger.info(f"🔧   - Metering points count: {len(metering_points)}")
            if metering_points:
                for i, mp in enumerate(metering_points):
                    logger.info(f"🔧   - Meter {i+1}: '{mp.get('name', 'Unknown')}' -> '{mp.get('code', 'Unknown')}'")
            
            logger.info(f"🔧 Processed config for frontend:")
            logger.info(f"🔧   - has_api_key result: {has_real_api_key}")
            logger.info(f"🔧   - has_energy_id result: {has_real_energy_id}")
            
            safe_config = {
                'has_api_key': has_real_api_key,
                'has_energy_id': has_real_energy_id,
                'metering_points': metering_points,
                'billing': config.get('billing', {}),
                'display': config.get('display', {})
            }
            
            logger.info(f"🔧 Sending to frontend: {json.dumps(safe_config, indent=2)}")
            self.send_json(safe_config)
            logger.info("🔧 === CONFIG API REQUEST COMPLETE ===")
        
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
        logger.info("📊 === METERING DATA REQUEST ===")
        
        config = load_config()
        api_key = config.get('api_key', '')
        energy_id = config.get('energy_id', '')
        
        logger.info(f"📊 Handling metering data request")
        logger.info(f"📊 API key present: {bool(api_key and api_key != 'your-test-api-key')}")
        logger.info(f"📊 Energy ID present: {bool(energy_id and energy_id != 'your-test-energy-id')}")
        
        if not api_key or not energy_id:
            logger.error("❌ API credentials not configured")
            logger.error("❌ Dashboard will show 'API credentials not configured'")
            self.send_json({'error': 'API credentials not configured'}, 400)
            return
        
        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        metering_point = query.get('metering_point', [None])[0]
        obis_code = query.get('obis_code', ['1-1:1.29.0'])[0]
        start_date = query.get('start_date', [None])[0]
        end_date = query.get('end_date', [None])[0]
        
        logger.info(f"📊 Request parameters:")
        logger.info(f"📊   - Metering point: {metering_point}")
        logger.info(f"📊   - OBIS code: {obis_code}")
        logger.info(f"📊   - Start date: {start_date}")
        logger.info(f"📊   - End date: {end_date}")
        
        if not metering_point:
            logger.error("❌ Missing metering_point parameter")
            self.send_json({'error': 'Missing metering_point parameter'}, 400)
            return
        
        # Default to yesterday (Leneda data is not real-time)
        if not start_date or not end_date:
            # Get yesterday's data since Leneda data is delayed
            yesterday = datetime.now() - timedelta(days=1)
            start_dt = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
            end_dt = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
            start_date = start_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_date = end_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            
            logger.info(f"📊 Using default date range (yesterday):")
            logger.info(f"📊   - Start: {start_date}")
            logger.info(f"📊   - End: {end_date}")
            logger.info(f"📊 NOTE: Leneda has 1-day delay, requesting yesterday's data")
            
        logger.info(f"📊 Final request details:")
        logger.info(f"📊   - Period: {start_date} to {end_date}")
        logger.info(f"📊   - Metering point: {metering_point}")
        logger.info(f"📊   - OBIS code: {obis_code}")
        
        # Build URL with proper encoding
        base_url = f"{LENEDA_API_BASE}/metering-points/{quote(metering_point)}/time-series"
        
        # Properly encode query parameters
        params = {
            'startDateTime': start_date,
            'endDateTime': end_date,
            'obisCode': obis_code
        }
        
        url = f"{base_url}?{urlencode(params)}"
        logger.info(f"📊 Encoded URL: {url}")
        
        headers = {
            'X-API-KEY': api_key,
            'X-ENERGY-ID': energy_id,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        data = make_api_request(url, headers)
        
        if data:
            items_count = len(data.get('items', []))
            logger.info(f"✅ Successfully fetched {items_count} data points")
            if items_count == 0:
                logger.warning(f"⚠️ No data points returned - this might be normal if:")
                logger.warning(f"⚠️   - No consumption during this period")
                logger.warning(f"⚠️   - Data not yet available (1-day delay)")
                logger.warning(f"⚠️   - Weekend/holiday when meter doesn't report")
            else:
                logger.info(f"📊 Data sample: {json.dumps(data.get('items', [])[:2], indent=2)}")
            self.send_json(data)
        else:
            logger.error("❌ Failed to fetch data from Leneda API")
            logger.error("❌ Dashboard will show 'Failed to fetch data from Leneda API'")
            self.send_json({'error': 'Failed to fetch data from Leneda API. Check logs for details.'}, 500)
    
    def handle_aggregated_data(self):
        """Handle aggregated data request"""
        config = load_config()
        api_key = config.get('api_key', '')
        energy_id = config.get('energy_id', '')
        
        logger.info(f"Handling aggregated data request. API key present: {bool(api_key)}")
        
        if not api_key or not energy_id:
            logger.error("API credentials not configured")
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
            logger.error("Missing metering_point parameter")
            self.send_json({'error': 'Missing metering_point parameter'}, 400)
            return
        
        # Default to last 30 days ending yesterday
        if not start_date or not end_date:
            yesterday = datetime.now() - timedelta(days=1)
            end_dt = yesterday.replace(hour=23, minute=59, second=59)
            start_dt = end_dt - timedelta(days=30)
            start_date = start_dt.strftime('%Y-%m-%d')
            end_date = end_dt.strftime('%Y-%m-%d')
        
        logger.info(f"Requesting aggregated data for period: {start_date} to {end_date}")
        logger.info(f"Metering point: {metering_point}, OBIS: {obis_code}, Level: {aggregation_level}")
        
        # Build URL with proper encoding
        base_url = f"{LENEDA_API_BASE}/metering-points/{quote(metering_point)}/time-series/aggregated"
        
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'obisCode': obis_code,
            'aggregationLevel': aggregation_level,
            'transformationMode': 'Accumulation'
        }
        
        url = f"{base_url}?{urlencode(params)}"
        
        headers = {
            'X-API-KEY': api_key,
            'X-ENERGY-ID': energy_id,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        data = make_api_request(url, headers)
        
        if data:
            items_count = len(data.get('aggregatedTimeSeries', []))
            logger.info(f"Successfully fetched {items_count} aggregated data points")
            self.send_json(data)
        else:
            logger.error("Failed to fetch aggregated data from Leneda API")
            self.send_json({'error': 'Failed to fetch aggregated data. Check logs for details.'}, 500)
    
    def handle_calculate_invoice(self):
        """Handle invoice calculation"""
        config = load_config()
        billing = config.get('billing', {})
        api_key = config.get('api_key', '')
        energy_id = config.get('energy_id', '')
        
        logger.info(f"Handling invoice calculation. API key present: {bool(api_key)}")
        
        # Parse query parameters
        query = parse_qs(urlparse(self.path).query)
        metering_point = query.get('metering_point', [None])[0]
        start_date = query.get('start_date', [None])[0]
        end_date = query.get('end_date', [None])[0]
        
        if not metering_point or not start_date or not end_date:
            logger.error("Missing required parameters for invoice calculation")
            self.send_json({
                'error': 'Missing required parameters: metering_point, start_date, end_date'
            }, 400)
            return
        
        logger.info(f"Calculating invoice for period: {start_date} to {end_date}")
        
        # Fetch consumption data with proper URL encoding
        base_url = f"{LENEDA_API_BASE}/metering-points/{quote(metering_point)}/time-series/aggregated"
        
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'obisCode': '1-1:1.29.0',
            'aggregationLevel': 'Infinite',
            'transformationMode': 'Accumulation'
        }
        
        url = f"{base_url}?{urlencode(params)}"
        
        headers = {
            'X-API-KEY': api_key,
            'X-ENERGY-ID': energy_id,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        data = make_api_request(url, headers)
        
        if not data:
            logger.error("Failed to fetch consumption data for invoice")
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
    logger.info("Version: 1.0.8")
    logger.info("License: GPL-3.0")
    logger.info(f"Server listening on: http://0.0.0.0:8099")
    logger.info(f"Static files: {STATIC_DIR}")
    logger.info(f"Config file: {CONFIG_FILE}")
    logger.info(f"Leneda API base: {LENEDA_API_BASE}")
    logger.info("=" * 60)
    logger.info("🔧 TROUBLESHOOTING TIPS:")
    logger.info("🔧 - Check logs for '✅ Config loaded successfully'")
    logger.info("🔧 - Look for '✅ Successfully fetched X data points'")
    logger.info("🔧 - Remember: Leneda has 1-day data delay")
    logger.info("🔧 - If empty dashboard: check credentials & wait 24h")
    logger.info("=" * 60)
    logger.info("READY - No external dependencies required!")
    logger.info("=" * 60)
    
    # Load and log initial configuration
    logger.info("🔧 Loading initial configuration for validation...")
    config = load_config()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        httpd.shutdown()


if __name__ == '__main__':
    main()
