// Leneda Energy Dashboard - JavaScript
// Version: 1.0.5

console.log('🚀 Loading Leneda Dashboard JavaScript v1.0.5');

let config = {};
let charts = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Leneda Dashboard initializing...');
    console.log('🚀 Current URL:', window.location.href);
    console.log('🚀 Setting up application...');
    
    // Set up event listeners
    setupEventListeners();
    
    // Load configuration
    console.log('🚀 About to load configuration...');
    loadConfiguration();
    
    // Initialize charts
    console.log('🚀 Initializing charts...');
    initializeCharts();
    
    // Start auto-refresh
    console.log('🚀 Starting auto-refresh...');
    startAutoRefresh();
    
    console.log('🚀 Initialization complete!');
});

// Event Listeners
function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });
    
    // Theme toggle
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    
    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', refreshData);
    
    // Invoice calculation
    document.getElementById('calculateInvoiceBtn').addEventListener('click', calculateInvoice);
    
    // Chart period selector
    document.getElementById('chartPeriod').addEventListener('change', (e) => {
        updateChartData(e.target.value);
    });
}

// Tab Switching
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
    
    // Load tab-specific data
    if (tabName === 'charts') {
        updateChartData('week');
    } else if (tabName === 'settings') {
        displaySettings();
    }
}

// Theme Toggle
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('themeIcon');
    
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        themeIcon.textContent = '☀️';
        updateChartTheme('light');
    } else {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        themeIcon.textContent = '🌙';
        updateChartTheme('dark');
    }
}

// Load Configuration
async function loadConfiguration() {
    try {
        console.log('🔧 Loading configuration from /api/config...');
        
        // First test if we can reach the server at all
        console.log('🔧 Testing server connectivity...');
        try {
            const healthResponse = await fetch('/api/health');
            console.log('🔧 Health check response status:', healthResponse.status);
            if (healthResponse.ok) {
                const healthData = await healthResponse.json();
                console.log('🔧 Health check data:', healthData);
            }
        } catch (healthError) {
            console.error('❌ Health check failed:', healthError);
        }
        
        // Now try to get the config
        const response = await fetch('/api/config', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Cache-Control': 'no-cache'
            }
        });
        
        console.log('🔧 Config response status:', response.status);
        console.log('🔧 Config response headers:', [...response.headers.entries()]);
        
        if (response.ok) {
            const responseText = await response.text();
            console.log('🔧 Raw config response:', responseText);
            
            config = JSON.parse(responseText);
            console.log('✅ Configuration loaded:', config);
            console.log('🔧 API key status:', config.has_api_key);
            console.log('🔧 Energy ID status:', config.has_energy_id);
            console.log('🔧 Metering points:', config.metering_points?.length || 0);
            
            updateConfigStatus();
            
            // Load initial data if configured
            if (config.has_api_key && config.has_energy_id) {
                console.log('✅ Credentials available, loading data...');
                refreshData();
            } else {
                console.log('❌ Missing credentials - showing error');
                showStatus('Please configure API credentials in settings', 'error');
            }
        } else {
            console.error('❌ Failed to load config, status:', response.status);
            const errorText = await response.text();
            console.error('❌ Error response:', errorText);
            showStatus('Failed to load configuration', 'error');
        }
    } catch (error) {
        console.error('❌ Error loading configuration:', error);
        console.error('❌ Error details:', error.message, error.stack);
        showStatus('Failed to load configuration', 'error');
    }
}

// Update Configuration Status Display
function updateConfigStatus() {
    console.log('🔧 Updating config status display...');
    console.log('🔧 config.has_api_key:', config.has_api_key);
    console.log('🔧 config.has_energy_id:', config.has_energy_id);
    console.log('🔧 config.metering_points:', config.metering_points);
    
    const apiKeyText = config.has_api_key ? '✅ Configured' : '❌ Not Configured';
    const energyIdText = config.has_energy_id ? '✅ Configured' : '❌ Not Configured';
    
    console.log('🔧 Setting API key status to:', apiKeyText);
    console.log('🔧 Setting Energy ID status to:', energyIdText);
    
    document.getElementById('apiKeyStatus').textContent = apiKeyText;
    document.getElementById('energyIdStatus').textContent = energyIdText;
    document.getElementById('meteringPointsCount').textContent = 
        config.metering_points?.length || 0;
}

// Display Settings
function displaySettings() {
    const billing = config.billing || {};
    const billingHtml = `
        <div class="stat-row">
            <span>Energy Supplier</span>
            <span>${billing.energy_supplier_name || 'Not set'}</span>
        </div>
        <div class="stat-row">
            <span>Fixed Fee (Monthly)</span>
            <span>€${billing.energy_fixed_fee_monthly || '0.00'}</span>
        </div>
        <div class="stat-row">
            <span>Variable Rate (per kWh)</span>
            <span>€${billing.energy_variable_rate_per_kwh || '0.00'}</span>
        </div>
        <div class="stat-row">
            <span>Network Operator</span>
            <span>${billing.network_operator_name || 'Not set'}</span>
        </div>
        <div class="stat-row">
            <span>VAT Rate</span>
            <span>${((billing.vat_rate || 0) * 100).toFixed(0)}%</span>
        </div>
        <div class="stat-row">
            <span>Reference Power</span>
            <span>${billing.reference_power_kw || '0'} kW</span>
        </div>
    `;
    
    document.getElementById('billingSettings').innerHTML = billingHtml;
}

// Refresh All Data
async function refreshData() {
    console.log('Refreshing data...');
    showStatus('Refreshing data...', 'success');
    
    try {
        await Promise.all([
            updateDashboardStats(),
            updateLiveChart()
        ]);
        
        showStatus('Data refreshed successfully', 'success');
        setTimeout(() => hideStatus(), 3000);
    } catch (error) {
        console.error('Error refreshing data:', error);
        showStatus('Failed to refresh data', 'error');
    }
}

// Update Dashboard Statistics
async function updateDashboardStats() {
    if (!config.metering_points || config.metering_points.length === 0) {
        showStatus('No metering points configured', 'warning');
        return;
    }
    
    const meteringPoint = config.metering_points[0].code;
    
    try {
        // IMPORTANT: Leneda data is only available for PREVIOUS days (not today)
        // Get yesterday's date range
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        const yesterdayStart = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate());
        const yesterdayEnd = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate(), 23, 59, 59);
        
        // Get yesterday's consumption
        const response = await fetch(`/api/aggregated-data?metering_point=${meteringPoint}&obis_code=1-1:1.29.0&start_date=${formatDate(yesterdayStart)}&end_date=${formatDate(yesterdayEnd)}&aggregation_level=Infinite`);
        
        if (response.ok) {
            const data = await response.json();
            const yesterdayUsage = data.aggregatedTimeSeries?.[0]?.value || 0;
            document.getElementById('todayUsage').textContent = `${yesterdayUsage.toFixed(2)} kWh`;
        }
        
        // Get last 7 days data
        const weekAgo = new Date(yesterdayStart);
        weekAgo.setDate(weekAgo.getDate() - 7);
        const weekResponse = await fetch(`/api/aggregated-data?metering_point=${meteringPoint}&obis_code=1-1:1.29.0&start_date=${formatDate(weekAgo)}&end_date=${formatDate(yesterdayEnd)}&aggregation_level=Infinite`);
        
        if (weekResponse.ok) {
            const weekData = await weekResponse.json();
            const weekUsage = weekData.aggregatedTimeSeries?.[0]?.value || 0;
            document.getElementById('weekConsumption').textContent = `${weekUsage.toFixed(2)} kWh`;
        }
        
        // Get last 30 days data
        const monthAgo = new Date(yesterdayStart);
        monthAgo.setDate(monthAgo.getDate() - 30);
        const monthResponse = await fetch(`/api/aggregated-data?metering_point=${meteringPoint}&obis_code=1-1:1.29.0&start_date=${formatDate(monthAgo)}&end_date=${formatDate(yesterdayEnd)}&aggregation_level=Infinite`);
        
        if (monthResponse.ok) {
            const monthData = await monthResponse.json();
            const monthUsage = monthData.aggregatedTimeSeries?.[0]?.value || 0;
            document.getElementById('monthConsumption').textContent = `${monthUsage.toFixed(2)} kWh`;
            
            // Estimate cost
            const billing = config.billing || {};
            const estimatedCost = monthUsage * (billing.energy_variable_rate_per_kwh || 0.15);
            document.getElementById('monthCost').textContent = `€${estimatedCost.toFixed(2)}`;
        }
        
        // Try to get production data if available (solar)
        const productionResponse = await fetch(`/api/aggregated-data?metering_point=${meteringPoint}&obis_code=1-1:2.29.0&start_date=${formatDate(yesterdayStart)}&end_date=${formatDate(yesterdayEnd)}&aggregation_level=Infinite`);
        
        if (productionResponse.ok) {
            const prodData = await productionResponse.json();
            const yesterdayProduction = prodData.aggregatedTimeSeries?.[0]?.value || 0;
            document.getElementById('solarProduction').textContent = `${yesterdayProduction.toFixed(2)} kWh`;
        } else {
            // No solar production available
            document.getElementById('solarProduction').textContent = 'N/A';
        }
        
    } catch (error) {
        console.error('Error updating dashboard stats:', error);
        showStatus('Error fetching data. Check configuration.', 'error');
    }
}

// Initialize Charts
function initializeCharts() {
    const isDark = document.body.classList.contains('dark-theme');
    const gridColor = isDark ? '#2a2a4e' : '#dee2e6';
    const textColor = isDark ? '#eaeaea' : '#212529';
    
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                labels: {
                    color: textColor
                }
            }
        },
        scales: {
            x: {
                grid: {
                    color: gridColor
                },
                ticks: {
                    color: textColor
                }
            },
            y: {
                grid: {
                    color: gridColor
                },
                ticks: {
                    color: textColor
                }
            }
        }
    };
    
    // Live Chart
    const liveCtx = document.getElementById('liveChart').getContext('2d');
    charts.live = new Chart(liveCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Power (kW)',
                data: [],
                borderColor: '#00b4d8',
                backgroundColor: 'rgba(0, 180, 216, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                x: {
                    ...commonOptions.scales.x,
                    type: 'time',
                    time: {
                        unit: 'minute',
                        displayFormats: {
                            minute: 'HH:mm'
                        }
                    }
                }
            }
        }
    });
    
    // Energy Chart
    const energyCtx = document.getElementById('energyChart').getContext('2d');
    charts.energy = new Chart(energyCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Consumption (kWh)',
                    data: [],
                    backgroundColor: '#ef476f',
                    borderRadius: 6
                },
                {
                    label: 'Production (kWh)',
                    data: [],
                    backgroundColor: '#06ffa5',
                    borderRadius: 6
                }
            ]
        },
        options: commonOptions
    });
    
    // Distribution Chart (Pie)
    const distCtx = document.getElementById('distributionChart').getContext('2d');
    charts.distribution = new Chart(distCtx, {
        type: 'doughnut',
        data: {
            labels: ['Self-Consumed', 'Exported', 'Imported'],
            datasets: [{
                data: [40, 25, 35],
                backgroundColor: ['#06ffa5', '#00b4d8', '#ffb703'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: textColor,
                        padding: 15
                    }
                }
            }
        }
    });
    
    // Interval Chart
    const intervalCtx = document.getElementById('intervalChart').getContext('2d');
    charts.interval = new Chart(intervalCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: '15-min intervals (kW)',
                data: [],
                borderColor: '#0077b6',
                backgroundColor: 'rgba(0, 119, 182, 0.1)',
                tension: 0.3,
                fill: true
            }]
        },
        options: commonOptions
    });
}

// Update Yesterday's Chart (Shows yesterday's 15-minute intervals)
// Note: Leneda does NOT provide live/real-time data - only historical data
async function updateLiveChart() {
    if (!config.metering_points || config.metering_points.length === 0) {
        return;
    }
    
    const meteringPoint = config.metering_points[0].code;
    
    // IMPORTANT: Leneda only provides data from PREVIOUS days
    // Fetch yesterday's 15-minute interval data
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayStart = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate(), 0, 0, 0);
    const yesterdayEnd = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate(), 23, 59, 59);
    
    try {
        const response = await fetch(`/api/metering-data?metering_point=${meteringPoint}&obis_code=1-1:1.29.0&start_date=${yesterdayStart.toISOString()}&end_date=${yesterdayEnd.toISOString()}`);
        
        if (response.ok) {
            const data = await response.json();
            const items = data.items || [];
            
            if (items.length === 0) {
                showStatus('No data available for yesterday. Data appears 1 day later.', 'warning');
                return;
            }
            
            const labels = items.map(item => new Date(item.startedAt));
            const values = items.map(item => item.value);
            
            charts.live.data.labels = labels;
            charts.live.data.datasets[0].data = values;
            charts.live.data.datasets[0].label = `Yesterday's Power (kW) - 15-min intervals`;
            charts.live.update();
            
            // Update peak consumption from yesterday
            if (values.length > 0) {
                const peakValue = Math.max(...values);
                const avgValue = values.reduce((a, b) => a + b, 0) / values.length;
                document.getElementById('currentConsumption').textContent = `${peakValue.toFixed(2)} kW`;
            }
        } else {
            console.error('Failed to fetch metering data');
            showStatus('No data available. Check configuration.', 'error');
        }
    } catch (error) {
        console.error('Error updating yesterday\'s chart:', error);
        showStatus('Error fetching data from Leneda API', 'error');
    }
}

// Update Chart Data
async function updateChartData(period) {
    if (!config.metering_points || config.metering_points.length === 0) {
        return;
    }
    
    const meteringPoint = config.metering_points[0].code;
    
    // IMPORTANT: Leneda data ends YESTERDAY (not today)
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const endDate = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate(), 23, 59, 59);
    
    let startDate;
    let aggregationLevel;
    
    switch (period) {
        case 'day':
            // Yesterday's hourly data
            startDate = new Date(yesterday.getFullYear(), yesterday.getMonth(), yesterday.getDate(), 0, 0, 0);
            aggregationLevel = 'Hour';
            break;
        case 'week':
            // Last 7 days (daily)
            startDate = new Date(endDate);
            startDate.setDate(startDate.getDate() - 7);
            aggregationLevel = 'Day';
            break;
        case 'month':
            // Last 30 days (daily)
            startDate = new Date(endDate);
            startDate.setDate(startDate.getDate() - 30);
            aggregationLevel = 'Day';
            break;
        case 'year':
            // Last 12 months (monthly)
            startDate = new Date(endDate);
            startDate.setMonth(startDate.getMonth() - 12);
            aggregationLevel = 'Month';
            break;
        default:
            startDate = new Date(endDate);
            startDate.setDate(startDate.getDate() - 7);
            aggregationLevel = 'Day';
    }
    
    try {
        // Get consumption data
        const consumptionResponse = await fetch(`/api/aggregated-data?metering_point=${meteringPoint}&obis_code=1-1:1.29.0&start_date=${formatDate(startDate)}&end_date=${formatDate(endDate)}&aggregation_level=${aggregationLevel}`);
        
        let consumptionItems = [];
        if (consumptionResponse.ok) {
            const data = await consumptionResponse.json();
            consumptionItems = data.aggregatedTimeSeries || [];
        }
        
        // Try to get production data
        const productionResponse = await fetch(`/api/aggregated-data?metering_point=${meteringPoint}&obis_code=1-1:2.29.0&start_date=${formatDate(startDate)}&end_date=${formatDate(endDate)}&aggregation_level=${aggregationLevel}`);
        
        let productionItems = [];
        if (productionResponse.ok) {
            const prodData = await productionResponse.json();
            productionItems = prodData.aggregatedTimeSeries || [];
        }
        
        // Update chart
        const labels = consumptionItems.map(item => formatChartDate(new Date(item.startedAt), period));
        const consumptionValues = consumptionItems.map(item => item.value);
        const productionValues = productionItems.map(item => item.value);
        
        charts.energy.data.labels = labels;
        charts.energy.data.datasets[0].data = consumptionValues;
        charts.energy.data.datasets[1].data = productionValues.length > 0 ? productionValues : [];
        charts.energy.update();
        
    } catch (error) {
        console.error('Error updating chart data:', error);
    }
}

// Calculate Invoice
async function calculateInvoice() {
    if (!config.metering_points || config.metering_points.length === 0) {
        showStatus('No metering points configured', 'error');
        return;
    }
    
    const meteringPoint = config.metering_points[0].code;
    
    // Calculate for PREVIOUS MONTH (complete data)
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    
    // Get first day of previous month
    const startOfLastMonth = new Date(yesterday.getFullYear(), yesterday.getMonth() - 1, 1);
    // Get last day of previous month
    const endOfLastMonth = new Date(yesterday.getFullYear(), yesterday.getMonth(), 0, 23, 59, 59);
    
    try {
        const response = await fetch(`/api/calculate-invoice?metering_point=${meteringPoint}&start_date=${formatDate(startOfLastMonth)}&end_date=${formatDate(endOfLastMonth)}`);
        
        if (response.ok) {
            const invoice = await response.json();
            displayInvoice(invoice);
            showStatus('Invoice calculated for previous month', 'success');
        } else {
            showStatus('Failed to calculate invoice', 'error');
        }
    } catch (error) {
        console.error('Error calculating invoice:', error);
        showStatus('Error calculating invoice', 'error');
    }
}

// Display Invoice
function displayInvoice(invoice) {
    const html = `
        <div class="invoice">
            <h4>Invoice Period: ${invoice.period.start} to ${invoice.period.end}</h4>
            <div class="stat-row">
                <span><strong>Total Consumption</strong></span>
                <span><strong>${invoice.consumption_kwh} kWh</strong></span>
            </div>
            <hr style="margin: 20px 0; border-color: var(--border);">
            <h4>Breakdown</h4>
            <div class="stat-row">
                <span>Energy Fixed Fee</span>
                <span>€${invoice.breakdown.energy_fixed_fee}</span>
            </div>
            <div class="stat-row">
                <span>Energy Variable</span>
                <span>€${invoice.breakdown.energy_variable}</span>
            </div>
            <div class="stat-row">
                <span>Network Metering Fee</span>
                <span>€${invoice.breakdown.network_metering_fee}</span>
            </div>
            <div class="stat-row">
                <span>Network Power Reference</span>
                <span>€${invoice.breakdown.network_power_reference}</span>
            </div>
            <div class="stat-row">
                <span>Network Variable</span>
                <span>€${invoice.breakdown.network_variable}</span>
            </div>
            <div class="stat-row">
                <span>Compensation Fund</span>
                <span style="color: var(--success);">€${invoice.breakdown.compensation_fund}</span>
            </div>
            <div class="stat-row">
                <span>Electricity Tax</span>
                <span>€${invoice.breakdown.electricity_tax}</span>
            </div>
            <hr style="margin: 20px 0; border-color: var(--border);">
            <div class="stat-row">
                <span><strong>Subtotal</strong></span>
                <span><strong>€${invoice.subtotal}</strong></span>
            </div>
            <div class="stat-row">
                <span>VAT (${(invoice.vat.rate * 100).toFixed(0)}%)</span>
                <span>€${invoice.vat.amount}</span>
            </div>
            <div class="stat-row" style="font-size: 1.2rem; color: var(--accent-primary);">
                <span><strong>Total</strong></span>
                <span><strong>€${invoice.total} ${invoice.currency}</strong></span>
            </div>
        </div>
    `;
    
    document.getElementById('invoiceContent').innerHTML = html;
}

// Update Chart Theme
function updateChartTheme(theme) {
    const gridColor = theme === 'dark' ? '#2a2a4e' : '#dee2e6';
    const textColor = theme === 'dark' ? '#eaeaea' : '#212529';
    
    Object.values(charts).forEach(chart => {
        if (chart.options.scales) {
            if (chart.options.scales.x) {
                chart.options.scales.x.grid.color = gridColor;
                chart.options.scales.x.ticks.color = textColor;
            }
            if (chart.options.scales.y) {
                chart.options.scales.y.grid.color = gridColor;
                chart.options.scales.y.ticks.color = textColor;
            }
        }
        if (chart.options.plugins?.legend?.labels) {
            chart.options.plugins.legend.labels.color = textColor;
        }
        chart.update();
    });
}

// Show Status Message
function showStatus(message, type) {
    const banner = document.getElementById('statusBanner');
    const messageEl = document.getElementById('statusMessage');
    
    messageEl.textContent = message;
    banner.className = `status-banner ${type}`;
}

// Hide Status Message
function hideStatus() {
    document.getElementById('statusBanner').classList.add('hidden');
}

// Auto Refresh
function startAutoRefresh() {
    const interval = (config.display?.update_interval_seconds || 300) * 1000;
    
    setInterval(() => {
        if (config.has_api_key && config.has_energy_id) {
            updateDashboardStats();
            updateLiveChart();
        }
    }, interval);
}

// Utility Functions
function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function formatChartDate(date, period) {
    if (period === 'day') {
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    } else if (period === 'week' || period === 'month') {
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    } else {
        return date.toLocaleDateString('en-US', { month: 'short' });
    }
}

console.log('Leneda Dashboard app.js loaded');
