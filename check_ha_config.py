#!/usr/bin/env python3
"""
Home Assistant Leneda Configuration Checker
This helps verify your Home Assistant addon configuration is working
"""

import json
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import quote, urlencode
from datetime import datetime, timedelta

def check_ha_logs():
    """Instructions for checking Home Assistant logs"""
    print("🔍 TO CHECK YOUR HOME ASSISTANT CONFIGURATION:")
    print()
    print("1. Go to Home Assistant → Settings → Add-ons")
    print("2. Click on 'Leneda Energy Dashboard'")
    print("3. Go to the 'Log' tab")
    print("4. Look for these messages:")
    print()
    print("✅ GOOD SIGNS:")
    print("   - 'Config loaded successfully. Has API key: True'")
    print("   - 'Successfully fetched X data points'")
    print("   - 'API response status: 200'")
    print()
    print("❌ PROBLEM SIGNS:")
    print("   - 'API credentials not configured'")
    print("   - 'HTTP error for https://api.leneda.eu: 401'")
    print("   - 'Network error'")
    print("   - 'Failed to fetch data from Leneda API'")
    print()

def test_api_manually():
    """Show how to test the API manually"""
    print("🧪 TO TEST YOUR API MANUALLY:")
    print()
    print("Replace these with your REAL values and run in terminal:")
    print()
    print('curl -X GET "https://api.leneda.eu/api/metering-points/YOUR_METER_CODE/time-series/aggregated?startDate=2025-10-03&endDate=2025-10-03&obisCode=1-1%3A1.29.0&aggregationLevel=Infinite&transformationMode=Accumulation" \\')
    print('  -H "X-API-KEY: YOUR_API_KEY" \\')
    print('  -H "X-ENERGY-ID: YOUR_ENERGY_ID" \\')
    print('  -H "Content-Type: application/json"')
    print()
    print("This should return yesterday's total consumption.")
    print("If you get an error, that's the problem!")
    print()

def main():
    print("=" * 70)
    print("HOME ASSISTANT LENEDA CONFIGURATION CHECKER")
    print("=" * 70)
    print()
    
    print("🏠 HOME ASSISTANT vs LOCAL TESTING:")
    print()
    print("LOCAL TESTING (this folder):")
    print("- Uses: test_options.json (has fake credentials)")
    print("- Server loads placeholder values")
    print("- Dashboard will be empty")
    print()
    print("HOME ASSISTANT ADDON:")
    print("- Uses: /data/options.json (has your real credentials)")
    print("- Server loads your actual API key, Energy ID, meter code")
    print("- Dashboard should work (with 1-day data delay)")
    print()
    
    print("📅 DATA TIMING REMINDER:")
    print(f"- Today: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"- Latest Leneda data: {(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')}")
    print("- If you configured it TODAY, data appears TOMORROW!")
    print()
    
    check_ha_logs()
    test_api_manually()
    
    print("🔧 TROUBLESHOOTING STEPS:")
    print()
    print("1. Check Home Assistant addon logs for errors")
    print("2. Verify your credentials in the addon configuration")
    print("3. Test API manually with curl command above")
    print("4. If configured today, wait until tomorrow")
    print("5. Restart the addon if needed")
    print()
    
    print("📋 CONFIGURATION CHECKLIST:")
    print("- [ ] API key is from Leneda portal (long alphanumeric)")
    print("- [ ] Energy ID is correct (usually starts with LUXE-)")
    print("- [ ] Metering point code is exact (check for typos)")
    print("- [ ] Internet connection works from Home Assistant")
    print("- [ ] Waited 24+ hours if just configured")
    print()
    
    print("=" * 70)
    print("SUMMARY: Your Home Assistant addon DOES use your real")
    print("configuration. The empty dashboard is likely due to:")
    print("1. Data timing (1-day delay)")
    print("2. API connectivity issues")
    print("3. Small credential errors")
    print("=" * 70)

if __name__ == "__main__":
    main()