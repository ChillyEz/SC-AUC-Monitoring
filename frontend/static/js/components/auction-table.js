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
                <th>Текущая цена</th>
                <th>Выкуп</th>
                <th>Количество</th>
                <th>Окончание</th>
            </tr>
        `;
        table.appendChild(thead);
        
        // Body
        const tbody = document.createElement('tbody');
        lots.forEach(lot => {
            const row = document.createElement('tr');
            
            // Использовать currentPrice или buyoutPrice как fallback
            const displayPrice = lot.currentPrice || lot.buyoutPrice || lot.startPrice || 0;
            const buyoutPrice = lot.buyoutPrice || 0;
            
            // Рассчитать оставшееся время
            const endTime = lot.endTime ?  new Date(lot.endTime) : null;
            const timeLeft = endTime ? this.formatTimeLeft(endTime) : 'N/A';
            
            row.innerHTML = `
                <td class="price">${displayPrice. toLocaleString()} ₽</td>
                <td class="price">${buyoutPrice.toLocaleString()} ₽</td>
                <td class="amount">${lot.amount}</td>
                <td class="time-left">${timeLeft}</td>
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
     * Format time left until end
     */
    static formatTimeLeft(endTime) {
        const now = new Date();
        const diff = endTime - now;
        
        if (diff < 0) return 'Истёк';
        
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        
        if (hours > 24) {
            const days = Math.floor(hours / 24);
            return `${days}д ${hours % 24}ч`;
        }
        
        return `${hours}ч ${minutes}м`;
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
            // API возвращает "time", а не "sold_at"
            const soldDate = item.time ? new Date(item.time).toLocaleString('ru-RU') : 'N/A';
            row.innerHTML = `
                <td class="price">${(item.price || 0).toLocaleString()} ₽</td>
                <td class="amount">${item.amount || 0}</td>
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