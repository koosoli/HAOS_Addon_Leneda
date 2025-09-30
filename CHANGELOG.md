# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-XX

### Added
- Initial release of Leneda Energy Dashboard
- Real-time energy monitoring with Leneda API integration
- 15-minute interval data visualization
- Dark mode interface (default) with light mode toggle
- Interactive charts using Chart.js:
  - Live power consumption chart
  - Historical energy consumption chart
  - Production vs consumption comparison
  - 15-minute interval detailed view
  - Distribution pie chart
- Invoice calculator with Luxembourg tariff support:
  - Energy supplier charges (fixed + variable)
  - Network operator charges (metering + power reference + variable)
  - Exceedance charges for power above reference
  - Compensation fund credits
  - Electricity tax
  - VAT calculations
- Dashboard with key metrics:
  - Current consumption
  - Today's usage
  - Solar production
  - Weekly statistics
  - Monthly statistics
- Configuration management:
  - Multi-metering point support
  - Customizable billing rates
  - Display preferences (theme, language, update interval)
  - Support for consumption, production, and combined meters
- Auto-refresh functionality (configurable interval)
- Responsive design for mobile, tablet, and desktop
- Home Assistant ingress integration
- Health check endpoint
- Comprehensive error handling and logging

### Technical Details
- Python 3.11 backend with Flask
- Simple, reliable Dockerfile using python:3.11-alpine
- No complex build dependencies (no npm during Docker build)
- Static frontend with vanilla JavaScript
- Chart.js for data visualization
- RESTful API architecture
- Proper Home Assistant addon structure with rootfs

### Configuration
- Support for multiple metering points
- Configurable Luxembourg energy tariffs
- Display customization (theme, language, update interval)
- Gas data support (optional)
- Reference power limit configuration

## [Unreleased]

### Planned Features
- Export data to CSV
- Comparison with previous periods
- Energy cost predictions
- Power quality metrics
- Gas consumption tracking (when enabled)
- Multi-language support (German, French, Luxembourgish)
- Email invoice summaries
- Integration with Home Assistant energy dashboard
- Custom alert thresholds
- Historical data retention settings
