# Leneda Energy Dashboard

Advanced energy dashboard for Leneda smart meters with invoice calculations and 15-minute interval visualization.

![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg)
![Supports armhf Architecture](https://img.shields.io/badge/armhf-yes-green.svg)
![Supports armv7 Architecture](https://img.shields.io/badge/armv7-yes-green.svg)

## About

This add-on provides a comprehensive energy dashboard for Leneda smart meters in Luxembourg. It offers:

- ⚡ Real-time energy monitoring with 15-minute intervals
- 🌞 Solar production and consumption tracking
- 💰 Automatic invoice calculation based on Luxembourg tariffs
- 📈 Historical data analysis and visualization
- 🌙 Dark mode interface optimized for Home Assistant

## Installation

1. Add this repository to your Home Assistant add-on store
2. Install the "Leneda Energy Dashboard" add-on
3. Configure your Leneda API credentials
4. Start the add-on
5. Access the dashboard from your sidebar

## Configuration

**Required:**
- `api_key`: Your Leneda API key
- `energy_id`: Your Leneda Energy ID
- `metering_points`: List of your metering point codes

**Optional:**
- Customize billing rates for invoice calculations
- Adjust display preferences (theme, update interval)
- Configure reference power limits

## Getting API Credentials

1. Log in to [Leneda Portal](https://portal.leneda.eu)
2. Navigate to Settings → API Keys
3. Generate a new API key
4. Copy your API Key and Energy ID
5. Find your Metering Point Code(s)

## Support

For issues and questions:
- [GitHub Issues](https://github.com/koosoli/HAOS_Addon_Leneda/issues)
- [Documentation](https://github.com/koosoli/HAOS_Addon_Leneda/blob/main/README.md)
