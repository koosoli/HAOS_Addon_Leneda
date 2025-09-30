#!/usr/bin/env python3
"""
Leneda Energy Dashboard - Backend Server
Version: 0.1.0
"""

import os
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, jsonify, send_from_directory, request
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', static_url_path='')

# Configuration
CONFIG_FILE = '/data/options.json'
LENEDA_API_BASE = 'https://api.leneda.eu/api'


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


def get_leneda_headers(config):
    """Get headers for Leneda API requests"""
    return {
        'X-API-KEY': config.get('api_key', ''),
        'X-ENERGY-ID': config.get('energy_id', ''),
        'Content-Type': 'application/json'
    }


@app.route('/')
def index():
    """Serve the main dashboard page"""
    return send_from_directory('static', 'index.html')


@app.route('/api/config')
def get_config():
    """Get addon configuration (without sensitive data)"""
    config = load_config()
    # Remove sensitive information
    safe_config = {
        'has_api_key': bool(config.get('api_key')),
        'has_energy_id': bool(config.get('energy_id')),
        'metering_points': config.get('metering_points', []),
        'billing': config.get('billing', {}),
        'display': config.get('display', {})
    }
    return jsonify(safe_config)


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'version': '0.1.0'})


@app.route('/api/metering-data')
def get_metering_data():
    """Get metering data from Leneda API"""
    config = load_config()
    
    # Get query parameters
    metering_point = request.args.get('metering_point')
    obis_code = request.args.get('obis_code', '1-1:1.29.0')  # Default: consumption
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not metering_point:
        return jsonify({'error': 'Missing metering_point parameter'}), 400
    
    # Default to last 24 hours if no dates provided
    if not start_date or not end_date:
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=1)
        start_date = start_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_date = end_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    try:
        url = f"{LENEDA_API_BASE}/metering-points/{metering_point}/time-series"
        params = {
            'startDateTime': start_date,
            'endDateTime': end_date,
            'obisCode': obis_code
        }
        
        headers = get_leneda_headers(config)
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            logger.error(f"Leneda API error: {response.status_code} - {response.text}")
            return jsonify({
                'error': f'API error: {response.status_code}',
                'message': response.text
            }), response.status_code
            
    except Exception as e:
        logger.error(f"Error fetching metering data: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/aggregated-data')
def get_aggregated_data():
    """Get aggregated metering data from Leneda API"""
    config = load_config()
    
    metering_point = request.args.get('metering_point')
    obis_code = request.args.get('obis_code', '1-1:1.29.0')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    aggregation_level = request.args.get('aggregation_level', 'Day')
    
    if not metering_point:
        return jsonify({'error': 'Missing metering_point parameter'}), 400
    
    # Default to last 30 days
    if not start_date or not end_date:
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=30)
        start_date = start_dt.strftime('%Y-%m-%d')
        end_date = end_dt.strftime('%Y-%m-%d')
    
    try:
        url = f"{LENEDA_API_BASE}/metering-points/{metering_point}/time-series/aggregated"
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'obisCode': obis_code,
            'aggregationLevel': aggregation_level,
            'transformationMode': 'Accumulation'
        }
        
        headers = get_leneda_headers(config)
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            logger.error(f"Leneda API error: {response.status_code} - {response.text}")
            return jsonify({
                'error': f'API error: {response.status_code}',
                'message': response.text
            }), response.status_code
            
    except Exception as e:
        logger.error(f"Error fetching aggregated data: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/calculate-invoice')
def calculate_invoice():
    """Calculate energy invoice based on configuration"""
    config = load_config()
    billing = config.get('billing', {})
    
    # Get metering data for the requested period
    metering_point = request.args.get('metering_point')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not metering_point:
        return jsonify({'error': 'Missing metering_point parameter'}), 400
    
    try:
        # Fetch consumption data
        consumption_url = f"{LENEDA_API_BASE}/metering-points/{metering_point}/time-series/aggregated"
        params = {
            'startDate': start_date,
            'endDate': end_date,
            'obisCode': '1-1:1.29.0',  # Consumption
            'aggregationLevel': 'Infinite',
            'transformationMode': 'Accumulation'
        }
        
        headers = get_leneda_headers(config)
        response = requests.get(consumption_url, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch consumption data'}), 500
        
        data = response.json()
        total_kwh = data.get('aggregatedTimeSeries', [{}])[0].get('value', 0)
        
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
        
        return jsonify({
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
        })
        
    except Exception as e:
        logger.error(f"Error calculating invoice: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logger.info("Starting Leneda Energy Dashboard Server")
    logger.info(f"Serving on port 8099")
    app.run(host='0.0.0.0', port=8099, debug=False)