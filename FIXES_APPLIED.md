# Leneda Dashboard Fixes Applied

## Issues Identified and Fixed

### 1. URL Encoding Problems ✅
**Problem**: OBIS codes and parameters weren't properly URL encoded
- `1-1:1.29.0` needs to be encoded as `1-1%3A1.29.0` 
- Special characters in metering point codes weren't handled

**Fix**: Added proper URL encoding using `quote()` and `urlencode()`

### 2. API Request Error Handling ✅  
**Problem**: Limited error reporting made debugging difficult
- No logging of actual API requests
- Generic error messages
- No details about HTTP status codes or response bodies

**Fix**: Enhanced error handling with:
- Detailed logging of API requests and responses
- HTTP status codes in logs
- Response body logging for errors
- Better error messages to users

### 3. Date Format and Timezone Issues ✅
**Problem**: Inconsistent date formatting for API requests
- Mixed use of datetime formats
- Not accounting for Leneda's UTC requirement
- Requesting "today's" data which isn't available

**Fix**: 
- Standardized ISO 8601 date formatting
- Default to yesterday's data (Leneda has 1-day delay)
- Proper timezone handling

### 4. Configuration Path Issues ✅
**Problem**: Server only looked for `/data/options.json` 
- Caused issues during development/testing
- No fallback for different environments

**Fix**: Added multiple config path fallbacks:
- `/data/options.json` (production)
- `test_options.json` (testing)
- `./test_options.json` (local testing)

### 5. Missing HTTP Headers ✅
**Problem**: API requests missing proper headers
- No `Accept` header
- Inconsistent `Content-Type`

**Fix**: Added proper headers:
- `Accept: application/json`
- `Content-Type: application/json`
- Consistent header usage

### 6. Frontend Logging Error ✅
**Problem**: JavaScript used undefined `_LOGGER` variable
- Caused console errors
- Prevented proper error reporting

**Fix**: Changed to `console.error()`

## New Features Added

### 1. API Test Script ✅
Created `test_leneda_api.py` to:
- Test API credentials independently
- Verify network connectivity  
- Debug specific OBIS codes
- Show sample data responses

### 2. Enhanced Logging ✅
Added comprehensive logging:
- API request URLs and headers
- Response status codes
- Data point counts
- Configuration loading status

### 3. Debugging Guide ✅
Created `DEBUG_GUIDE.md` with:
- Step-by-step troubleshooting
- Common error solutions
- Configuration examples
- Understanding data timing

## Key Insights About Leneda API

### Data Timing 🕐
- **NOT real-time**: Data has 1-day delay
- Today's data appears tomorrow
- Dashboard shows "yesterday" as most recent

### OBIS Codes 📊
- `1-1:1.29.0` = Consumption (most common)
- `1-1:2.29.0` = Production (solar panels)
- Must be URL encoded in requests

### Authentication 🔐
- Requires both `X-API-KEY` and `X-ENERGY-ID` headers
- Keys can be regenerated in Leneda portal
- Energy ID is account-specific

## Testing Your Installation

### 1. Test API Connection
```bash
python test_leneda_api.py <api_key> <energy_id> <metering_point>
```

### 2. Check Server Logs
Look for these in Home Assistant addon logs:
- "Config loaded successfully. Has API key: True"
- "Successfully fetched X data points"
- No "Failed to fetch" errors

### 3. Verify Configuration
Ensure addon config has:
- Valid API key (long alphanumeric string)
- Valid Energy ID (usually starts with LUXE-)
- Correct metering point code

### 4. Wait for Data
Remember: If you just set it up today, you'll see data tomorrow!

## Expected Behavior After Fixes

### Dashboard Display
- Shows yesterday's consumption as "today's usage"
- Historical charts work properly
- No "API credentials not configured" errors

### API Requests
- Properly encoded URLs in logs
- 200 status codes for successful requests
- Detailed error messages for failures

### Error Handling
- Clear error messages about what went wrong
- Logs show exact API requests being made
- Network issues properly identified

## If Still Having Issues

1. **Check your credentials** in the Leneda web portal
2. **Run the test script** to verify API access
3. **Check the logs** for specific error messages
4. **Verify network connectivity** to api.leneda.eu
5. **Wait 24 hours** for data to appear if just configured

The most common issue is expecting immediate data when Leneda provides historical data with a 1-day delay!