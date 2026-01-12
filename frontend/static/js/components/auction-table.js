/**
 * Auction table component
 */

class AuctionTable {
    /**
     * Render auction lots table
     */
    static renderLotsTable(lots, container) {
        if (!lots || lots.length === 0) {
            container.innerHTML = '<p class="no-data">Лоты не найдены</p>';
            return;
        }
        
        const table = document.createElement('table');
        table.className = 'auction-table';
        
        // Header
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Цена</th>
                <th>Количество</th>
                <th>Время</th>
            </tr>
        `;
        table.appendChild(thead);
        
        // Body
        const tbody = document.createElement('tbody');
        lots.forEach(lot => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="price">${lot.price.toLocaleString()} ₽</td>
                <td class="amount">${lot.amount}</td>
                <td class="time-left">${lot.time_left || 'N/A'}</td>
            `;
            tbody.appendChild(row);
        });
        table.appendChild(tbody);
        
        container.innerHTML = '';
        container.appendChild(table);
        
        // Meta info
        const meta = document.createElement('div');
        meta.className = 'table-meta';
        meta.textContent = `Найдено лотов: ${lots.length}`;
        container.appendChild(meta);
    }
    
    /**
     * Render auction history table
     */
    static renderHistoryTable(history, container) {
        if (!history || history.length === 0) {
            container.innerHTML = '<p class="no-data">История не найдена</p>';
            return;
        }
        
        const table = document.createElement('table');
        table.className = 'auction-table';
        
        // Header
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Цена</th>
                <th>Количество</th>
                <th>Дата продажи</th>
            </tr>
        `;
        table.appendChild(thead);
        
        // Body
        const tbody = document.createElement('tbody');
        history.forEach(item => {
            const row = document.createElement('tr');
            const soldDate = item.sold_at ? new Date(item.sold_at).toLocaleString('ru-RU') : 'N/A';
            row.innerHTML = `
                <td class="price">${item.price.toLocaleString()} ₽</td>
                <td class="amount">${item.amount}</td>
                <td class="time-left">${soldDate}</td>
            `;
            tbody.appendChild(row);
        });
        table.appendChild(tbody);
        
        container.innerHTML = '';
        container.appendChild(table);
        
        // Meta info
        const meta = document.createElement('div');
        meta.className = 'table-meta';
        meta.textContent = `Найдено записей: ${history.length}`;
        container.appendChild(meta);
    }
}
