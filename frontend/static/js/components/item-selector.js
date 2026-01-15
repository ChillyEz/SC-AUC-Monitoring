/**
 * Item selector component with autocomplete
 */

class ItemSelector {
    constructor(inputElement, searchButton) {
        this.inputElement = inputElement;
        this.searchButton = searchButton;
        this.currentItemId = '';
        this.currentItemCategory = '';
        this.autocompleteDropdown = null;
        this. searchTimeout = null;
        this.selectedIndex = -1;
        this. currentAbortController = null;  // ← Для отмены запросов
        
        this.initAutocomplete();
        
        // Enter key to search or select from dropdown
        this.inputElement.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (this.autocompleteDropdown && this.selectedIndex >= 0) {
                    this.selectItemFromDropdown(this.selectedIndex);
                } else {
                    this.handleSearch();
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                this. navigateDropdown(1);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.navigateDropdown(-1);
            } else if (e.key === 'Escape') {
                this.hideAutocomplete();
            }
        });
        
        // Button click to search
        this.searchButton.addEventListener('click', () => {
            this.handleSearch();
        });
    }
    
    initAutocomplete() {
        // Create autocomplete dropdown
        this.autocompleteDropdown = document.createElement('div');
        this.autocompleteDropdown.className = 'autocomplete-dropdown';
        this.autocompleteDropdown. style.display = 'none';
        
        // Position relative to input
        const inputParent = this.inputElement.parentElement;
        inputParent.style.position = 'relative';
        inputParent.appendChild(this.autocompleteDropdown);
        
        // Input event for search
        this.inputElement.addEventListener('input', (e) => {
            this.handleInput(e.target.value);
        });
        
        // Hide dropdown on outside click
        document.addEventListener('click', (e) => {
            if (e.target !== this.inputElement && ! this.autocompleteDropdown. contains(e.target)) {
                this.hideAutocomplete();
            }
        });
    }
    
    handleInput(query) {
        // Clear existing timeout
        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }
        
        // Cancel previous request
        if (this. currentAbortController) {
            this.currentAbortController.abort();
            this.currentAbortController = null;
        }
        
        const trimmedQuery = query.trim();
        console.log(`[ItemSelector] Input: "${trimmedQuery}" (length: ${trimmedQuery.length})`);
        
        // Hide if too short
        if (trimmedQuery.length < 2) {
            this.hideAutocomplete();
            return;
        }
        
        // Show loading indicator
        this.showLoading();
        
        // Debounce search (500ms - немного увеличил для более медленных запросов)
        this.searchTimeout = setTimeout(async () => {
            await this.searchItems(trimmedQuery);
        }, 500);
    }
    
    showLoading() {
        this.autocompleteDropdown.innerHTML = '<div class="autocomplete-loading">🔍 Поиск... </div>';
        this.autocompleteDropdown.style.display = 'block';
    }
    
    showError(message) {
        this.autocompleteDropdown.innerHTML = `<div class="autocomplete-error">❌ ${message}</div>`;
        this.autocompleteDropdown.style.display = 'block';
    }
    
    showEmpty() {
        this.autocompleteDropdown.innerHTML = '<div class="autocomplete-empty">😕 Ничего не найдено</div>';
        this.autocompleteDropdown.style.display = 'block';
    }
    
    async searchItems(query) {
        console.log(`[ItemSelector] Searching for: "${query}"`);
        
        // Create abort controller
        this.currentAbortController = new AbortController();
        const signal = this.currentAbortController.signal;
        
        try {
            const startTime = Date.now();
            const response = await apiClient.searchItems(query, 'ru', signal);
            const duration = Date.now() - startTime;
            
            console.log(`[ItemSelector] Search completed in ${duration}ms, found ${response.items?. length || 0} items`);
            
            if (response. items && response.items.length > 0) {
                this.showAutocomplete(response.items);
            } else {
                this.showEmpty();
            }
        } catch (error) {
            if (error.name === 'AbortError') {
                console. log('[ItemSelector] Search aborted');
                return;
            }
            
            console.error('[ItemSelector] Search error:', error);
            this.showError('Ошибка поиска. Попробуйте снова.');
        } finally {
            this.currentAbortController = null;
        }
    }
    
    showAutocomplete(items) {
        console.log(`[ItemSelector] Showing ${items.length} items in dropdown`);
        
        this.autocompleteDropdown.innerHTML = '';
        this.selectedIndex = -1;
        
        items.forEach((item, index) => {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'autocomplete-item';
            itemDiv.dataset.index = index;
            itemDiv.dataset.itemId = item.id;
            itemDiv.dataset.category = item.category;
            
            // Create icon element
            const icon = document.createElement('img');
            icon.src = item.icon_url || '';
            icon.alt = item.name;
            icon.className = 'item-icon';
            icon.onerror = function() { 
                this.style.display = 'none';
                console.warn(`[ItemSelector] Failed to load icon:  ${item.icon_url}`);
            };
            
            // Create info container
            const infoDiv = document.createElement('div');
            infoDiv.className = 'item-info';
            
            // Create name element
            const nameDiv = document.createElement('div');
            nameDiv.className = 'item-name';
            nameDiv.textContent = item.name;
            
            // Create ID element
            const idDiv = document.createElement('div');
            idDiv.className = 'item-id';
            idDiv.textContent = item.id;
            
            // Assemble the structure
            infoDiv.appendChild(nameDiv);
            infoDiv.appendChild(idDiv);
            itemDiv.appendChild(icon);
            itemDiv.appendChild(infoDiv);
            
            itemDiv.addEventListener('click', () => {
                console.log(`[ItemSelector] Item clicked: ${item.id}`);
                this.selectItem(item);
            });
            
            this.autocompleteDropdown.appendChild(itemDiv);
        });
        
        this.autocompleteDropdown.style.display = 'block';
    }
    
    hideAutocomplete() {
        if (this.autocompleteDropdown) {
            this.autocompleteDropdown.style.display = 'none';
            this.selectedIndex = -1;
        }
    }
    
    navigateDropdown(direction) {
        if (! this.autocompleteDropdown || this.autocompleteDropdown.style.display === 'none') {
            return;
        }
        
        const items = this.autocompleteDropdown.querySelectorAll('.autocomplete-item');
        if (items.length === 0) return;
        
        // Remove current selection
        if (this.selectedIndex >= 0 && items[this.selectedIndex]) {
            items[this.selectedIndex]. classList.remove('selected');
        }
        
        // Update index
        this.selectedIndex += direction;
        if (this.selectedIndex < 0) {
            this. selectedIndex = items.length - 1;
        } else if (this.selectedIndex >= items.length) {
            this.selectedIndex = 0;
        }
        
        // Add new selection
        if (items[this.selectedIndex]) {
            items[this.selectedIndex].classList.add('selected');
            items[this.selectedIndex].scrollIntoView({ block: 'nearest' });
        }
    }
    
    selectItemFromDropdown(index) {
        const items = this.autocompleteDropdown.querySelectorAll('.autocomplete-item');
        if (items[index]) {
            const itemId = items[index].dataset. itemId;
            const category = items[index].dataset.category;
            const itemName = items[index].querySelector('.item-name').textContent;
            this.selectItem({ id: itemId, category: category, name: itemName });
        }
    }
    
    selectItem(item) {
        console.log(`[ItemSelector] Item selected: ${item.id}`);
        this.currentItemId = item.id;
        this. currentItemCategory = item.category;
        this.inputElement.value = item.name || item.id;
        this.hideAutocomplete();
        this.onItemSelect(item. id);
    }
    
    handleSearch() {
        const itemId = this.currentItemId || this.inputElement.value. trim();
        if (!itemId) {
            alert('Пожалуйста, введите ID предмета или выберите из списка');
            return;
        }
        
        console.log(`[ItemSelector] Manual search:  ${itemId}`);
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