#!/usr/bin/env python3
"""
Quick Leneda Dashboard Diagnostic
Run this with your real credentials to see what's happening
"""

import json
import sys
from datetime import datetime, timedelta

def main():
    print("=" * 60)
    print("LENEDA DASHBOARD DIAGNOSTIC")
    print("=" * 60)
    print()
    
    print("The dashboard is empty because one of these issues:")
    print()
    print("1. ❌ PLACEHOLDER CREDENTIALS")
    print("   Your test_options.json has fake credentials:")
    print("   - api_key: 'your-test-api-key'")
    print("   - energy_id: 'your-test-energy-id'")
    print("   - metering_point: 'LU000000000000000000000000000000'")
    print()
    print("2. ❌ EXPECTING TODAY'S DATA")
    print("   Leneda has 1-day delay - today's data appears tomorrow!")
    print(f"   Today is: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"   Latest available data: {(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')}")
    print()
    print("3. ❌ HOME ASSISTANT vs LOCAL TESTING")
    print("   Local test uses: test_options.json")
    print("   Home Assistant uses: /data/options.json (in container)")
    print()
    
    print("🔧 TO FIX:")
    print()
    print("FOR LOCAL TESTING:")
    print("1. Edit test_options.json with your REAL credentials")
    print("2. Run: python test_leneda_api.py <real_api_key> <real_energy_id> <real_meter_code>")
    print()
    print("FOR HOME ASSISTANT:")
    print("1. Check your addon configuration has real credentials")
    print("2. Look at Home Assistant logs for error messages")
    print("3. Wait 24 hours if you just configured it (for data to appear)")
    print()
    
    print("📋 CHECKLIST:")
    print("- [ ] API key is real (not 'your-test-api-key')")
    print("- [ ] Energy ID is real (not 'your-test-energy-id')")  
    print("- [ ] Metering point is real (not 'LU000000...')")
    print("- [ ] Waited 24 hours for data to appear")
    print("- [ ] Checked Home Assistant addon logs")
    print("- [ ] Tested API with test script")
    print()
    
    # Check current test config
    try:
        with open('test_options.json', 'r') as f:
            config = json.load(f)
            
        print("🔍 CURRENT TEST CONFIG:")
        api_key = config.get('api_key', '')
        energy_id = config.get('energy_id', '')
        meter_code = config.get('metering_points', [{}])[0].get('code', '')
        
        print(f"API Key: {api_key}")
        print(f"Energy ID: {energy_id}")
        print(f"Meter Code: {meter_code}")
        print()
        
        if api_key == "your-test-api-key":
            print("❌ PROBLEM: Still using placeholder API key!")
        else:
            print("✅ API key looks real")
            
        if energy_id == "your-test-energy-id":
            print("❌ PROBLEM: Still using placeholder Energy ID!")
        else:
            print("✅ Energy ID looks real")
            
        if meter_code == "LU000000000000000000000000000000":
            print("❌ PROBLEM: Still using placeholder meter code!")
        else:
            print("✅ Meter code looks real")
            
    except FileNotFoundError:
        print("❌ test_options.json not found")
    except Exception as e:
        print(f"❌ Error reading config: {e}")
    
    print()
    print("=" * 60)
    print("NEXT STEPS:")
    print("1. Put your REAL credentials in test_options.json")
    print("2. Run: python test_leneda_api.py <real_creds>")
    print("3. If that works, update your Home Assistant addon config")
    print("4. Remember: Data has 1-day delay!")
    print("=" * 60)

if __name__ == "__main__":
    main()