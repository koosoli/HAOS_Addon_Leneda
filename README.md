# Leneda Energy Dashboard for Home Assistant

Advanced energy monitoring dashboard for Leneda smart meters in Luxembourg.

[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)
![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg)
![Supports armhf Architecture](https://img.shields.io/badge/armhf-yes-green.svg)
![Supports armv7 Architecture](https://img.shields.io/badge/armv7-yes-green.svg)
![Supports i386 Architecture](https://img.shields.io/badge/i386-yes-green.svg)

## Features

- ⚡ **Real-time Monitoring**: View energy consumption and solar production with 15-minute interval precision
- 📊 **Interactive Charts**: Multiple chart types powered by Chart.js for comprehensive data visualization
- 💰 **Invoice Calculator**: Automatic cost calculation based on Luxembourg energy tariffs
- 🌙 **Dark Mode**: Beautiful dark theme optimized for Home Assistant (with light mode toggle)
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- 🔄 **Auto-refresh**: Configurable automatic data updates
- 🇱🇺 **Luxembourg Optimized**: Pre-configured with Enovos and Creos tariff structures

## Installation

### 1. Add Repository to Home Assistant

1. Go to **Settings** → **Add-ons** → **Add-on Store**
2. Click the menu (⋮) in the top right corner
3. Select **Repositories**
4. Add this URL: `https://github.com/koosoli/HAOS_Addon_Leneda`
5. Click **Add**

### 2. Install the Add-on

1. Find "Leneda Energy Dashboard" in the add-on store
2. Click on it and then click **Install**
3. Wait for the installation to complete

### 3. Configure

1. Go to the **Configuration** tab
2. Add your Leneda API credentials:
   ```yaml
   api_key: "your_api_key_here"
   energy_id: "your_energy_id_here"
   metering_points:
     - code: "LU000000000000000000000000000000"
       name: "Main Meter"
       type: "consumption"
   ```
3. (Optional) Adjust billing rates and display preferences
4. Click **Save**

### 4. Start the Add-on

1. Go to the **Info** tab
2. Click **Start**
3. Enable "Start on boot" if desired
4. Access the dashboard via "Open Web UI" or the sidebar icon

## Getting Your API Credentials

1. Log in to the [Leneda Portal](https://portal.leneda.eu/)
2. Navigate to **Settings** → **API Keys**
3. Generate a new API key
4. Copy your:
   - API Key
   - Energy ID
   - Metering Point Code(s)

## Configuration Options

### Required
- `api_key`: Your Leneda API key
- `energy_id`: Your Leneda Energy ID
- `metering_points`: Array of metering point configurations
  - `code`: Metering point code (30 characters starting with "LU")
  - `name`: Display name for the meter
  - `type`: One of: `consumption`, `production`, or `both`

### Optional - Billing
Customize Luxembourg energy tariffs for invoice calculations:
- `energy_supplier_name`: Default "Enovos"
- `energy_fixed_fee_monthly`: Monthly fixed fee (EUR)
- `energy_variable_rate_per_kwh`: Energy cost per kWh (EUR)
- `network_operator_name`: Default "Creos"
- `network_metering_fee_monthly`: Monthly metering fee (EUR)
- `network_power_reference_fee_monthly`: Power reference fee (EUR)
- `network_variable_rate_per_kwh`: Network cost per kWh (EUR)
- `exceedance_rate_per_kwh`: Exceedance charge per kWh (EUR)
- `compensation_fund_rate_per_kwh`: Compensation fund rate per kWh (EUR, can be negative)
- `electricity_tax_per_kwh`: Electricity tax per kWh (EUR)
- `vat_rate`: VAT rate (default 0.08 for 8%)
- `reference_power_kw`: Reference power in kW (default 12.0)
- `currency`: Currency code (EUR, USD, or CHF)

### Optional - Display
- `theme`: Interface theme (`dark`, `light`, or `auto`)
- `language`: Interface language (`en`, `de`, `fr`, or `lb`)
- `update_interval_seconds`: Auto-refresh interval in seconds (60-3600)
- `default_date_range`: Default chart range (`day`, `week`, `month`, or `year`)
- `show_gas_data`: Enable gas data display (boolean)

## Dashboard Features

### Dashboard Tab
- Current consumption and solar production
- Today's usage statistics
- Weekly and monthly summaries
- Live power flow visualization

### Charts Tab
- Energy analysis with multiple time ranges
- 15-minute interval consumption graphs
- Consumption distribution pie charts
- Interactive Chart.js visualizations

### Invoice Tab
- Automatic invoice calculation
- Detailed cost breakdown
- Monthly projections
- Luxembourg tariff support

### Settings Tab
- Configuration status overview
- Billing settings display
- Quick access to configuration instructions

## Troubleshooting

### Addon doesn't appear in store
- Ensure the repository URL is correct
- Click "Check for updates" in the add-on store
- Clear browser cache (Ctrl+F5 / Cmd+Shift+R)

### No data showing
- Verify your API credentials are correct
- Check that your metering point codes are valid
- Review add-on logs for API errors

### Charts not loading
- Ensure your browser supports JavaScript
- Check console for errors (F12 Developer Tools)
- Verify internet connectivity for Chart.js CDN

## Support

- **Issues**: [GitHub Issues](https://github.com/koosoli/HAOS_Addon_Leneda/issues)
- **Documentation**: [Technical Docs](DOCS.md)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Credits

Created by Olivier Koos for the Luxembourg Home Assistant community.

---

**Note**: This add-on requires a valid Leneda API account and active smart meter in Luxembourg.
