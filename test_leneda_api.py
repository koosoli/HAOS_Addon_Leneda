#!/usr/bin/env python3
"""
Leneda API Test Script
This script helps test the connection to Leneda API and debug issues
"""

import json
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import quote, urlencode
from datetime import datetime, timedelta

def test_leneda_api(api_key, energy_id, metering_point_code):
    """Test Leneda API connection with given credentials"""
    
    print("=" * 60)
    print("Leneda API Connection Test")
    print("=" * 60)
    
    if not api_key or not energy_id or not metering_point_code:
        print("❌ Missing required credentials:")
        print(f"   API Key: {'✅' if api_key else '❌'}")
        print(f"   Energy ID: {'✅' if energy_id else '❌'}")
        print(f"   Metering Point: {'✅' if metering_point_code else '❌'}")
        return False
    
    print(f"✅ Testing with:")
    print(f"   API Key: {api_key[:10]}..." if len(api_key) > 10 else f"   API Key: {api_key}")
    print(f"   Energy ID: {energy_id}")
    print(f"   Metering Point: {metering_point_code}")
    print()
    
    # Test 1: Get yesterday's aggregated consumption
    print("Test 1: Yesterday's Total Consumption")
    print("-" * 40)
    
    yesterday = datetime.now() - timedelta(days=1)
    start_date = yesterday.strftime('%Y-%m-%d')
    end_date = yesterday.strftime('%Y-%m-%d')
    
    base_url = f"https://api.leneda.eu/api/metering-points/{quote(metering_point_code)}/time-series/aggregated"
    
    params = {
        'startDate': start_date,
        'endDate': end_date,
        'obisCode': '1-1:1.29.0',  # Consumption
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
    
    print(f"Request URL: {url}")
    print(f"Headers: {headers}")
    
    try:
        req = Request(url, headers=headers, method='GET')
        with urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"✅ Success! Status: {response.status}")
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if 'aggregatedTimeSeries' in data and data['aggregatedTimeSeries']:
                consumption = data['aggregatedTimeSeries'][0]['value']
                unit = data.get('unit', 'kWh')
                print(f"📊 Yesterday's consumption: {consumption} {unit}")
            else:
                print("⚠️  No consumption data in response")
                
    except HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"Error details: {error_body}")
        except:
            pass
        return False
        
    except URLError as e:
        print(f"❌ Network Error: {e}")
        print("This could be:")
        print("- DNS resolution issue")
        print("- Network connectivity problem") 
        print("- Firewall blocking the request")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    print()
    
    # Test 2: Get yesterday's 15-minute intervals
    print("Test 2: Yesterday's 15-minute intervals")
    print("-" * 40)
    
    start_datetime = yesterday.replace(hour=0, minute=0, second=0).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_datetime = yesterday.replace(hour=23, minute=59, second=59).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    base_url = f"https://api.leneda.eu/api/metering-points/{quote(metering_point_code)}/time-series"
    
    params = {
        'startDateTime': start_datetime,
        'endDateTime': end_datetime,
        'obisCode': '1-1:1.29.0'
    }
    
    url = f"{base_url}?{urlencode(params)}"
    
    print(f"Request URL: {url}")
    
    try:
        req = Request(url, headers=headers, method='GET')
        with urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"✅ Success! Status: {response.status}")
            
            items = data.get('items', [])
            print(f"📊 Found {len(items)} 15-minute intervals")
            
            if items:
                print("Sample data points:")
                for i, item in enumerate(items[:3]):  # Show first 3 items
                    print(f"  {item['startedAt']}: {item['value']} {data.get('unit', 'kW')}")
                    
                if len(items) > 3:
                    print(f"  ... and {len(items) - 3} more")
            else:
                print("⚠️  No interval data available")
                
    except Exception as e:
        print(f"❌ Error fetching interval data: {e}")
    
    print()
    
    # Test 3: Try to get production data (solar)
    print("Test 3: Production data (Solar)")
    print("-" * 40)
    
    params['obisCode'] = '1-1:2.29.0'  # Production OBIS code
    url = f"{base_url}?{urlencode(params)}"
    
    try:
        req = Request(url, headers=headers, method='GET')
        with urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('items', [])
            print(f"✅ Found {len(items)} production data points")
            if not items:
                print("ℹ️  No solar production data (normal if no solar panels)")
                
    except HTTPError as e:
        if e.code == 404:
            print("ℹ️  No production data available (normal without solar)")
        else:
            print(f"❌ HTTP Error: {e.code} - {e.reason}")
    except Exception as e:
        print(f"❌ Error fetching production data: {e}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    # You can either pass credentials as arguments or edit them here
    if len(sys.argv) >= 4:
        api_key = sys.argv[1]
        energy_id = sys.argv[2] 
        metering_point = sys.argv[3]
    else:
        # Edit these with your actual credentials for testing
        api_key = "your-actual-api-key-here"
        energy_id = "your-actual-energy-id-here"
        metering_point = "your-actual-metering-point-code-here"
        
        print("To use this script with your credentials:")
        print("1. Edit the credentials in this file, OR")
        print("2. Run: python test_leneda_api.py <api_key> <energy_id> <metering_point>")
        print()
        
        if api_key == "your-actual-api-key-here":
            print("⚠️  Please edit the credentials in this file or pass them as arguments")
            sys.exit(1)
    
    test_leneda_api(api_key, energy_id, metering_point)