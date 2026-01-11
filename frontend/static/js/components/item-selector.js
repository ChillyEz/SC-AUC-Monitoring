/**
 * Item selector component
 */

class ItemSelector {
    constructor(inputElement, searchButton) {
        this.inputElement = inputElement;
        this.searchButton = searchButton;
        this.currentItemId = '';
        
        // Enter key to search
        this.inputElement.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.handleSearch();
            }
        });
        
        // Button click to search
        this.searchButton.addEventListener('click', () => {
            this.handleSearch();
        });
    }
    
    handleSearch() {
        const itemId = this.inputElement.value.trim();
        if (!itemId) {
            alert('Пожалуйста, введите ID предмета');
            return;
        }
        
        this.currentItemId = itemId;
        this.onItemSelect(itemId);
    }
    
    onItemSelect(itemId) {
        // Dispatch custom event
        const event = new CustomEvent('itemselect', { detail: { itemId } });
        document.dispatchEvent(event);
    }
    
    getItemId() {
        return this.currentItemId;
    }
}
