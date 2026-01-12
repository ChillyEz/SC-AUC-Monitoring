/**
 * Region selector component
 */

class RegionSelector {
    constructor(selectElement) {
        this.selectElement = selectElement;
        this.currentRegion = selectElement.value;
        
        this.selectElement.addEventListener('change', (e) => {
            this.currentRegion = e.target.value;
            this.onRegionChange(this.currentRegion);
        });
    }
    
    onRegionChange(region) {
        // Dispatch custom event
        const event = new CustomEvent('regionchange', { detail: { region } });
        document.dispatchEvent(event);
    }
    
    getRegion() {
        return this.currentRegion;
    }
}
