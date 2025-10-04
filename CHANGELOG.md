# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-10-04

### Added
- **Comprehensive debug logging** with emoji indicators for easy log scanning
- **Enhanced error messages** with specific troubleshooting hints for common issues
- **Detailed API request/response logging** showing URLs, headers, and response structure
- **Configuration validation** with clear status indicators for credentials
- **Better credential format checking** (detects placeholder vs real values)
- **Network error categorization** with specific suggestions (DNS, firewall, etc.)
- **Startup troubleshooting tips** displayed in logs

### Improved
- **Log readability** with structured formatting and visual indicators
- **Error diagnosis** with specific HTTP status code explanations (401, 404, 429)
- **Configuration loading** with detailed validation feedback
- **API response analysis** showing data structure and sample content

### Notes
- This version significantly improves troubleshooting capability
- Look for emoji indicators in logs: ✅ (success), ❌ (error), ⚠️ (warning), 🔧 (config), 🌐 (network)
- Enhanced logging will help identify exactly where issues occur

## [1.0.2] - 2025-10-04

### Fixed
- **Critical**: Fixed URL encoding for OBIS codes and metering point parameters (was causing API failures)
- **Critical**: Fixed date formatting issues - now properly requests yesterday's data instead of today's (Leneda has 1-day delay)
- Enhanced error handling and logging for API requests to help with debugging
- Added support for multiple config file paths (development and production)
- Improved HTTP headers for API requests (added Accept header)
- Fixed frontend JavaScript logging error (`_LOGGER` -> `console.error`)

### Added
- Comprehensive debug logging for API requests and responses
- Test script (`test_leneda_api.py`) for independent credential testing
- Debugging guide (`DEBUG_GUIDE.md`) with troubleshooting steps
- Better error messages with specific details about failures

### Changed
- Default behavior now requests yesterday's data (most recent available from Leneda)
- Enhanced configuration loading with fallback paths
- Improved API request timeout (10s -> 15s)

### Notes
- **Important**: Leneda provides historical data with 1-day delay, not real-time data
- If you just configured the addon today, data will appear tomorrow
- This version significantly improves reliability of API connections

## [1.0.1] - 2025-01-XX (Previous Release)

### Added
- Initial stable release of Leneda Energy Dashboard

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
