/**
 * API client for SC-AUC-Monitoring
 */

const API_BASE = '/api/v1';

class APIClient {
    /**
     * Get auction lots
     */
    async getAuctionLots(region, itemId) {
        try {
            const response = await fetch(`${API_BASE}/auction/${region}/${itemId}/lots`);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to fetch auction lots');
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching auction lots:', error);
            throw error;
        }
    }

    /**
     * Get auction history
     */
    async getAuctionHistory(region, itemId, limit = 50) {
        try {
            const response = await fetch(`${API_BASE}/auction/${region}/${itemId}/history?limit=${limit}`);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to fetch auction history');
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching auction history:', error);
            throw error;
        }
    }

    /**
     * Search items
     */
    async searchItems(query, realm = 'global') {
        try {
            const response = await fetch(`${API_BASE}/items/search?query=${encodeURIComponent(query)}&realm=${realm}`);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to search items');
            }
            return await response.json();
        } catch (error) {
            console.error('Error searching items:', error);
            throw error;
        }
    }

    /**
     * Get health status
     */
    async getHealth() {
        try {
            const response = await fetch('/health');
            if (!response.ok) {
                throw new Error('Failed to fetch health status');
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching health:', error);
            throw error;
        }
    }
}

// Export singleton
const apiClient = new APIClient();
