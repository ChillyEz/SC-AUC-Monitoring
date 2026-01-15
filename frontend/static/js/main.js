/**
 * Main application logic
 */

// Initialize components
const regionSelector = new RegionSelector(document.getElementById('region'));
const itemSelector = new ItemSelector(
    document.getElementById('item-id'),
    document.getElementById('search-btn')
);

// UI elements
const lotsContainer = document.getElementById('lots-container');
const lotsLoading = document. getElementById('lots-loading');
const lotsError = document.getElementById('lots-error');

const historyContainer = document.getElementById('history-container');
const historyLoading = document.getElementById('history-loading');
const historyError = document.getElementById('history-error');

const apiBadge = document. getElementById('api-badge');

/**
 * Load and display auction data
 */
async function loadAuctionData(region, itemId) {
    // Reset containers
    lotsContainer.innerHTML = '';
    historyContainer.innerHTML = '';
    lotsError.style.display = 'none';
    historyError.style.display = 'none';
    
    // Show loading
    lotsLoading.style.display = 'block';
    historyLoading.style.display = 'block';
    
    // Load lots
    try {
        const lotsData = await apiClient. getAuctionLots(region, itemId);
        lotsLoading.style.display = 'none';
        AuctionTable.renderLotsTable(lotsData.lots, lotsContainer);
    } catch (error) {
        lotsLoading. style.display = 'none';
        lotsError.textContent = `Ошибка загрузки лотов: ${error.message}`;
        lotsError.style.display = 'block';
    }
    
    // Load history
    try {
        const historyData = await apiClient.getAuctionHistory(region, itemId, 50);
        historyLoading.style.display = 'none';
        // ← ИСПРАВИТЬ: API возвращает "prices", а не "history"
        AuctionTable.renderHistoryTable(historyData.prices, historyContainer);
    } catch (error) {
        historyLoading.style.display = 'none';
        historyError.textContent = `Ошибка загрузки истории: ${error.message}`;
        historyError.style. display = 'block';
    }
}

/**
 * Handle item selection
 */
document.addEventListener('itemselect', async (event) => {
    const { itemId } = event.detail;
    const region = regionSelector.getRegion();
    
    console.log(`Loading data for: ${region} / ${itemId}`);
    await loadAuctionData(region, itemId);
});

/**
 * Initialize app
 */
async function initApp() {
    try {
        // Check API status
        const health = await apiClient.getHealth();
        if (health.using_demo_api) {
            apiBadge.textContent = 'Demo API';
            apiBadge.style.background = '#f59e0b';
        } else {
            apiBadge.textContent = 'Production API';
            apiBadge.style.background = '#10b981';
        }
        
        console.log('App initialized', health);
    } catch (error) {
        console.error('Failed to initialize app:', error);
        apiBadge.textContent = 'API Error';
        apiBadge.style. background = '#ef4444';
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initApp);