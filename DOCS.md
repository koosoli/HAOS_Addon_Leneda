# Leneda Energy Dashboard Documentation

## Architecture

### Overview
The Leneda Energy Dashboard is a Home Assistant add-on that provides a comprehensive energy monitoring interface for Leneda smart meters in Luxembourg.

```
┌─────────────────────────────────────────┐
│     Home Assistant (Ingress)            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   Flask Web Server (Port 8099)          │
│   ┌─────────────────────────────────┐   │
│   │  Static Frontend                │   │
│   │  - HTML/CSS/JavaScript          │   │
│   │  - Chart.js visualizations      │   │
│   └─────────────────────────────────┘   │
│   ┌─────────────────────────────────┐   │
│   │  REST API                       │   │
│   │  - /api/config                  │   │
│   │  - /api/metering-data           │   │
│   │  - /api/aggregated-data         │   │
│   │  - /api/calculate-invoice       │   │
│   └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     Leneda API (api.leneda.eu)          │
└─────────────────────────────────────────┘
```

### Components

#### Backend (server.py)
- **Flask Application**: Lightweight Python web server
- **API Integration**: Communicates with Leneda API
- **Data Processing**: Aggregates and calculates energy data
- **Invoice Calculation**: Computes billing based on Luxembourg tariffs

#### Frontend
- **HTML/CSS**: Modern, responsive interface with dark mode
- **JavaScript**: Interactive dashboard with real-time updates
- **Chart.js**: Data visualization library for charts and graphs

#### Configuration
- **config.yaml**: Addon configuration schema
- **options.json**: User configuration data (stored in /data/)

## API Endpoints

### GET /api/config
Returns the addon configuration (without sensitive data).

**Response:**
```json
{
  "has_api_key": true,
  "has_energy_id": true,
  "metering_points": [...],
  "billing": {...},
  "display": {...}
}
```

### GET /api/health
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

### GET /api/metering-data
Fetches raw metering data from Leneda API.

**Parameters:**
- `metering_point` (required): Metering point code
- `obis_code` (optional): OBIS code (default: 1-1:1.29.0)
- `start_date` (optional): Start date in ISO format
- `end_date` (optional): End date in ISO format

**Response:**
```json
{
  "meteringPointCode": "LU...",
  "obisCode": "1-1:1.29.0",
  "intervalLength": "PT15M",
  "unit": "kW",
  "items": [
    {
      "value": 14.588,
      "startedAt": "2024-07-01T01:00:00Z",
      "type": "Actual",
      "version": 1,
      "calculated": false
    }
  ]
}
```

### GET /api/aggregated-data
Fetches aggregated metering data.

**Parameters:**
- `metering_point` (required): Metering point code
- `obis_code` (optional): OBIS code
- `start_date` (optional): Start date
- `end_date` (optional): End date
- `aggregation_level` (optional): Hour, Day, Week, Month, Infinite

**Response:**
```json
{
  "aggregatedTimeSeries": [
    {
      "value": 3744.0485,
      "startedAt": "2025-01-01T23:00:00Z",
      "endedAt": "2025-01-31T23:00:00Z",
      "calculated": false
    }
  ],
  "unit": "kWh"
}
```

### GET /api/calculate-invoice
Calculates invoice based on configuration.

**Parameters:**
- `metering_point` (required): Metering point code
- `start_date` (required): Start date
- `end_date` (required): End date

**Response:**
```json
{
  "period": {
    "start": "2025-01-01",
    "end": "2025-01-31"
  },
  "consumption_kwh": 850.5,
  "breakdown": {
    "energy_fixed_fee": 1.50,
    "energy_variable": 127.58,
    "network_metering_fee": 5.90,
    "network_power_reference": 19.27,
    "network_variable": 64.54,
    "exceedance": 0.00,
    "compensation_fund": -31.98,
    "electricity_tax": 0.85
  },
  "subtotal": 187.66,
  "vat": {
    "rate": 0.08,
    "amount": 15.01
  },
  "total": 202.67,
  "currency": "EUR"
}
```

## Configuration Schema

### Metering Points
```yaml
metering_points:
  - code: "LU000000000000000000000000000000"  # 32-digit code
    name: "Main Meter"                        # Display name
    type: "consumption"                        # consumption|production|both
```

### Billing Configuration
All rates are per month unless specified otherwise:

```yaml
billing:
  energy_supplier_name: "Enovos"               # String
  energy_fixed_fee_monthly: 1.50               # EUR/month
  energy_variable_rate_per_kwh: 0.1500         # EUR/kWh
  network_operator_name: "Creos"               # String
  network_metering_fee_monthly: 5.90           # EUR/month
  network_power_reference_fee_monthly: 19.27   # EUR/month
  network_variable_rate_per_kwh: 0.0759        # EUR/kWh
  exceedance_rate_per_kwh: 0.1139              # EUR/kWh (above reference)
  compensation_fund_rate_per_kwh: -0.0376      # EUR/kWh (credit)
  electricity_tax_per_kwh: 0.0010              # EUR/kWh
  vat_rate: 0.08                               # 8% = 0.08
  reference_power_kw: 12.0                     # kW
  currency: "EUR"                              # EUR|USD|CHF
```

### Display Configuration
```yaml
display:
  theme: "dark"                    # dark|light|auto
  language: "en"                   # en|de|fr|lb
  update_interval_seconds: 300     # 60-3600 seconds
  default_date_range: "week"       # day|week|month|year
  show_gas_data: false             # true|false
```

## Deployment

### Development
```bash
# Test locally
docker build -t leneda-dashboard .
docker run -p 8099:8099 \
  -v $(pwd)/test-options.json:/data/options.json \
  leneda-dashboard
```

### Production (Home Assistant)
1. Copy to `/addons/leneda_dashboard/`
2. Restart Home Assistant
3. Install from Add-on Store
4. Configure and start

## Security Considerations

- API keys stored in Home Assistant's secure configuration
- HTTPS enforced through Home Assistant ingress
- No sensitive data in frontend code
- API key never sent to client
- Rate limiting on Leneda API calls
- Input validation on all user inputs

## Performance

- **Initial Load**: < 2 seconds
- **Data Refresh**: 5-minute intervals (configurable)
- **Chart Rendering**: < 500ms
- **API Response**: < 1 second (depends on Leneda API)
- **Memory Usage**: ~50-100 MB
- **CPU Usage**: < 5% (idle), ~15% (during refresh)

## Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Responsive design

## Troubleshooting

### Common Issues

1. **API Authentication Fails**
   - Verify API key and Energy ID are correct
   - Check that credentials haven't expired
   - Ensure metering points are accessible

2. **No Data Displayed**
   - Check Leneda account has data available
   - Verify date range has data
   - Review browser console for errors

3. **Charts Not Updating**
   - Check auto-refresh interval
   - Verify internet connectivity
   - Review addon logs

### Debug Mode

Enable debug logging in configuration:
```yaml
log_level: debug
```

Then check logs in Home Assistant:
Settings → Add-ons → Leneda Dashboard → Log

## Future Enhancements

- [ ] Data export (CSV, JSON)
- [ ] Email notifications for high usage
- [ ] Integration with HA Energy Dashboard
- [ ] Historical data retention
- [ ] Multi-language support
- [ ] Custom alert thresholds
- [ ] Power quality metrics
- [ ] Predictive analytics
- [ ] Mobile app companion

## Contributing

See CONTRIBUTING.md for guidelines on:
- Code style
- Testing requirements
- Pull request process
- Issue reporting

## License

GNU General Public License v3.0 - see LICENSE file for details.
