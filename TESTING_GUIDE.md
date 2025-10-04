# Home Assistant Addon Configuration Test

This file helps you test your Leneda configuration locally before deploying to Home Assistant.

## Step 1: Get Your Credentials

From your Home Assistant Leneda addon configuration, copy:
1. **API Key** - Long alphanumeric string from Leneda portal
2. **Energy ID** - Usually starts with "LUXE-" 
3. **Metering Point Code** - Your actual meter code

## Step 2: Create Test Configuration

Edit the file `test_options.json` in this directory with your REAL credentials:

```json
{
  "api_key": "PUT_YOUR_REAL_API_KEY_HERE",
  "energy_id": "PUT_YOUR_REAL_ENERGY_ID_HERE",
  "metering_points": [
    {
      "code": "PUT_YOUR_REAL_METERING_POINT_CODE_HERE",
      "name": "Main Meter",
      "type": "consumption"
    }
  ],
  "billing": {
    "energy_supplier_name": "Enovos",
    "energy_fixed_fee_monthly": 1.50,
    "energy_variable_rate_per_kwh": 0.1500,
    "network_operator_name": "Creos",
    "network_metering_fee_monthly": 5.90,
    "network_power_reference_fee_monthly": 19.27,
    "network_variable_rate_per_kwh": 0.0759,
    "exceedance_rate_per_kwh": 0.1139,
    "compensation_fund_rate_per_kwh": -0.0376,
    "electricity_tax_per_kwh": 0.0010,
    "vat_rate": 0.08,
    "reference_power_kw": 12.0,
    "currency": "EUR"
  },
  "display": {
    "theme": "dark",
    "language": "en",
    "update_interval_seconds": 300,
    "default_date_range": "week",
    "show_gas_data": false
  }
}
```

## Step 3: Test API Connection

Run this command with your actual credentials:

```bash
python test_leneda_api.py YOUR_API_KEY YOUR_ENERGY_ID YOUR_METERING_POINT_CODE
```

This will tell you if:
- Your credentials are valid
- The API is reachable
- Data is available for your meter

## Step 4: Test Local Server

1. Start the server: `python leneda_dashboard/rootfs/app/server.py`
2. Open browser: `http://localhost:8099`
3. Check for any error messages

## Common Issues

### "No data" but credentials are correct
- **Leneda has 1-day delay** - Today's data appears tomorrow
- Check if data exists for YESTERDAY, not today

### "API credentials not configured"
- Check that `test_options.json` has your real credentials
- Make sure there are no extra spaces or quotes

### "Network error"
- Check internet connection
- Try the API test script first

### Still not working?
- Check Home Assistant addon logs for specific error messages
- Verify your Leneda account has API access enabled
- Make sure your metering point code is exactly correct