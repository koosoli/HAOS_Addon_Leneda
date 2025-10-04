# Leneda Dashboard Debugging Guide

## Common Issues and Solutions

### Issue: No data appears in dashboard after entering credentials

This is the most common issue. Follow these debugging steps:

### Step 1: Verify Your Credentials

1. **API Key Format**: Should be a long alphanumeric string
2. **Energy ID Format**: Usually starts with "LUXE-" followed by characters
3. **Metering Point Code**: Usually starts with "LU" followed by numbers/letters

### Step 2: Test API Connection

Use the provided test script to verify your credentials work:

```bash
python test_leneda_api.py <your-api-key> <your-energy-id> <your-metering-point>
```

### Step 3: Understanding Leneda Data Timing

**IMPORTANT**: Leneda does NOT provide real-time data!

- Data is available for **previous days only**
- Today's data appears **tomorrow**
- The dashboard shows "yesterday's" data as the most recent

### Step 4: Check Server Logs

Look for these log messages in the Home Assistant addon logs:

```
✅ Good signs:
- "Config loaded successfully. Has API key: True"
- "Successfully fetched X data points"
- "API response status: 200"

❌ Problem indicators:
- "API credentials not configured"
- "HTTP error for https://api.leneda.eu: 401"
- "Network error" 
- "Failed to fetch data from Leneda API"
```

### Step 5: Common Error Solutions

#### Error: "401 Unauthorized"
- **Cause**: Invalid API key or Energy ID
- **Solution**: 
  1. Log into Leneda portal
  2. Regenerate API key
  3. Verify Energy ID is correct
  4. Update addon configuration

#### Error: "404 Not Found" 
- **Cause**: Invalid metering point code
- **Solution**:
  1. Check metering point code in Leneda portal
  2. Ensure exact format (including dashes/letters)

#### Error: "Network error" or DNS issues
- **Cause**: Home Assistant can't reach api.leneda.eu
- **Solution**:
  1. Check internet connection
  2. Verify DNS resolution
  3. Check firewall settings

#### No data but API calls succeed
- **Cause**: Requesting today's data (not available)
- **Solution**: 
  1. Data appears with 1-day delay
  2. Check yesterday's data
  3. Wait until tomorrow for today's data

### Step 6: Manual API Testing

You can test the API manually using curl:

```bash
# Test aggregated consumption for yesterday
curl -X GET "https://api.leneda.eu/api/metering-points/YOUR_METERING_POINT/time-series/aggregated?startDate=2024-10-03&endDate=2024-10-03&obisCode=1-1%3A1.29.0&aggregationLevel=Infinite&transformationMode=Accumulation" \
  -H "X-API-KEY: YOUR_API_KEY" \
  -H "X-ENERGY-ID: YOUR_ENERGY_ID" \
  -H "Content-Type: application/json"
```

Replace:
- `YOUR_METERING_POINT` with your actual metering point code
- `YOUR_API_KEY` with your actual API key  
- `YOUR_ENERGY_ID` with your actual energy ID
- `2024-10-03` with yesterday's date

### Step 7: Dashboard Configuration

Ensure your addon configuration follows this format:

```json
{
  "api_key": "your-actual-api-key",
  "energy_id": "your-actual-energy-id", 
  "metering_points": [
    {
      "code": "LU000000000000000000000000000000",
      "name": "Main Meter",
      "type": "consumption"
    }
  ]
}
```

### Step 8: Data Availability

Different OBIS codes provide different data:

- `1-1:1.29.0` - **Consumption** (most common)
- `1-1:2.29.0` - **Production** (solar panels)
- `1-1:3.29.0` - Reactive consumption
- `1-1:4.29.0` - Reactive production

If you don't have solar panels, production data (`1-1:2.29.0`) will be empty.

### Step 9: Time Zones and Dates

Leneda uses UTC times. The dashboard automatically:
- Converts local times to UTC for API requests
- Requests previous day's data (since today's isn't available)
- Shows times in local timezone in the UI

### Step 10: Frequency Limits

Leneda may have API rate limits:
- Don't refresh too frequently
- Default refresh is 5 minutes (300 seconds)
- Increase interval if you get rate limit errors

## Troubleshooting Checklist

- [ ] API key is valid and correctly entered
- [ ] Energy ID is valid and correctly entered  
- [ ] Metering point code is exact (check for typos)
- [ ] Internet connection is working
- [ ] Home Assistant can reach api.leneda.eu
- [ ] Waiting for previous day's data (not today's)
- [ ] Checked addon logs for error messages
- [ ] Tested with manual API call
- [ ] Verified account has access to the metering point

## Still Having Issues?

1. **Check Leneda Portal**: Verify you can see data in the official Leneda web interface
2. **Contact Leneda Support**: Ensure your account has API access enabled
3. **Test Network**: Try the API call from outside Home Assistant
4. **Check Logs**: Enable debug logging in Home Assistant

## Example Working Configuration

```yaml
# In Home Assistant addon config
api_key: "abcd1234efgh5678ijkl9012mnop3456"
energy_id: "LUXE-MA-MU-ABCD5"
metering_points:
  - code: "LU123456789012345678901234567890"
    name: "Main Consumption"
    type: "consumption"
billing:
  energy_supplier_name: "Enovos"
  energy_fixed_fee_monthly: 1.50
  energy_variable_rate_per_kwh: 0.1500
  # ... other billing settings
```

Remember: The most common issue is expecting real-time data when Leneda only provides historical data with a 1-day delay!