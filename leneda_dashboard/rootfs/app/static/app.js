// Leneda Energy Dashboard - JavaScript
// Version: 0.1.0

let config = {};
let charts = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Leneda Dashboard initializing...');
    
    // Set up event listeners
    setupEventListeners();
    
    // Load configuration
    loadConfiguration();
    
    // Initialize charts
    initializeCharts();
    
    // Start auto-refresh
    startAutoRefresh();
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
        const response = await fetch('/api/config');
        if (response.ok) {
            config = await response.json();
            console.log('Configuration loaded:', config);
            updateConfigStatus();
            
            // Load initial data if configured
            if (config.has_api_key && config.has_energy_id) {
                refreshData();
            } else {
                showStatus('Please configure API credentials in settings', 'error');
            }
        }
    } catch (error) {
        console.error('Error loading configuration:', error);
        showStatus('Failed to load configuration', 'error');
    }
}

// Update Configuration Status Display
function updateConfigStatus() {
    document.getElementById('apiKeyStatus').textContent = 
        config.has_api_key ? '✅ Configured' : '❌ Not Configured';
    document.getElementById('energyIdStatus').textContent = 
        config.has_energy_id ? '✅ Configured' : '❌ Not Configured';
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
        return;
    }
    
    const meteringPoint = config.metering_points[0].code;
    
    try {
        // Get today's data
        const today = new Date();
        const startOfDay = new Date(today.getFullYear(), today.getMonth(), today.getDate());
        const response = await fetch(`/api/aggregated-data?metering_point=${meteringPoint}&obisCode=1-1:1.29.0&start_date=${formatDate(startOfDay)}&end_date=${formatDate(today)}&aggregation_level=Infinite`);
        
        if (response.ok) {
            const data = await response.json();
            const todayUsage = data.aggregatedTimeSeries?.[0]?.value || 0;
            document.getElementById('todayUsage').textContent = `${todayUsage.toFixed(2)} kWh`;
        }
        
        // Get week data
        const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
        const weekResponse = await fetch(`/api/aggregated-data?metering_point=${meteringPoint}&obisCode=1-1:1.29.0&start_date=${formatDate(weekAgo)}&end_date=${formatDate(today)}&aggregation_level=Infinite`);
        
        if (weekResponse.ok) {
            const weekData = await weekResponse.json();
            const weekUsage = weekData.aggregatedTimeSeries?.[0]?.value || 0;
            document.getElementById('weekConsumption').textContent = `${weekUsage.toFixed(2)} kWh`;
        }
        
        // Get month data
        const monthAgo = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
        const monthResponse = await fetch(`/api/aggregated-data?metering_point=${meteringPoint}&obisCode=1-1:1.29.0&start_date=${formatDate(monthAgo)}&end_date=${formatDate(today)}&aggregation_level=Infinite`);
        
        if (monthResponse.ok) {
            const monthData = await monthResponse.json();
            const monthUsage = monthData.aggregatedTimeSeries?.[0]?.value || 0;
            document.getElementById('monthConsumption').textContent = `${monthUsage.toFixed(2)} kWh`;
            
            // Estimate cost
            const billing = config.billing || {};
            const estimatedCost = monthUsage * (billing.energy_variable_rate_per_kwh || 0.15);
            document.getElementById('monthCost').textContent = `€${estimatedCost.toFixed(2)}`;
        }
        
        // Try to get production data if available
        const productionResponse = await fetch(`/api/aggregated-data?metering_point=${meteringPoint}&obisCode=1-1:2.29.0&start_date=${formatDate(startOfDay)}&end_date=${formatDate(today)}&aggregation_level=Infinite`);
        
        if (productionResponse.ok) {
            const prodData = await productionResponse.json();
            const todayProduction = prodData.aggregatedTimeSeries?.[0]?.value || 0;
            document.getElementById('solarProduction').textContent = `${todayProduction.toFixed(2)} kWh`;
        }
        
    } catch (error) {
        console.error('Error updating dashboard stats:', error);
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

// Update Live Chart
async function updateLiveChart() {
    if (!config.metering_points || config.metering_points.length === 0) {
        return;
    }
    
    const meteringPoint = config.metering_points[0].code;
    const now = new Date();
    const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);
    
    try {
        const response = await fetch(`/api/metering-data?metering_point=${meteringPoint}&obisCode=1-1:1.29.0&start_date=${oneHourAgo.toISOString()}&end_date=${now.toISOString()}`);
        
        if (response.ok) {
            const data = await response.json();
            const items = data.items || [];
            
            const labels = items.map(item => new Date(item.startedAt));
            const values = items.map(item => item.value);
            
            charts.live.data.labels = labels;
            charts.live.data.datasets[0].data = values;
            charts.live.update();
            
            // Update current consumption
            if (values.length > 0) {
                const currentValue = values[values.length - 1];
                document.getElementById('currentConsumption').textContent = `${currentValue.toFixed(2)} kW`;
            }
        }
    } catch (error) {
        console.error('Error updating live chart:', error);
    }
}

// Update Chart Data
async function updateChartData(period) {
    if (!config.metering_points || config.metering_points.length === 0) {
        return;
    }
    
    const meteringPoint = config.metering_points[0].code;
    const now = new Date();
    let startDate;
    let aggregationLevel;
    
    switch (period) {
        case 'day':
            startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
            aggregationLevel = 'Hour';
            break;
        case 'week':
            startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            aggregationLevel = 'Day';
            break;
        case 'month':
            startDate = new Date(now.getFullYear(), now.getMonth(), 1);
            aggregationLevel = 'Day';
            break;
        case 'year':
            startDate = new Date(now.getFullYear(), 0, 1);
            aggregationLevel = 'Month';
            break;
        default:
            startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            aggregationLevel = 'Day';
    }
    
    try {
        const response = await fetch(`/api/aggregated-data?metering_point=${meteringPoint}&obisCode=1-1:1.29.0&start_date=${formatDate(startDate)}&end_date=${formatDate(now)}&aggregation_level=${aggregationLevel}`);
        
        if (response.ok) {
            const data = await response.json();
            const items = data.aggregatedTimeSeries || [];
            
            const labels = items.map(item => formatChartDate(new Date(item.startedAt), period));
            const values = items.map(item => item.value);
            
            charts.energy.data.labels = labels;
            charts.energy.data.datasets[0].data = values;
            charts.energy.update();
        }
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
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    
    try {
        const response = await fetch(`/api/calculate-invoice?metering_point=${meteringPoint}&start_date=${formatDate(startOfMonth)}&end_date=${formatDate(now)}`);
        
        if (response.ok) {
            const invoice = await response.json();
            displayInvoice(invoice);
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
