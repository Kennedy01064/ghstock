import os

path = r'c:\Users\HP\Desktop\Stock\app\templates\orders\order_detail.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Search Bar to include Filters
search_block = '''<!-- Search bar -->
        <div class="relative mb-4">
            <svg class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            <input type="text" id="catalog-search" placeholder="Buscar producto…"
                   class="w-full pl-10 pr-4 py-3 rounded-2xl border border-slate-200 bg-white text-sm font-medium focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition-all shadow-sm"
                   oninput="filterCatalog(this.value)">
        </div>'''

new_controls = '''<!-- Controls (Search & Filters) -->
        <div class="flex flex-col md:flex-row gap-3 mb-4">
            <!-- Search bar -->
            <div class="relative flex-1">
                <svg class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                <input type="text" id="catalog-search" placeholder="Buscar producto…"
                       class="w-full pl-10 pr-4 py-3 rounded-2xl border border-slate-200 bg-white text-sm font-medium focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition-all shadow-sm">
            </div>
            
            <!-- Category Filter -->
            <div class="md:w-56 lg:w-64 shrink-0">
                <select id="catalog-category-filter" class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-white text-sm font-medium focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition-all shadow-sm appearance-none cursor-pointer">
                    <option value="">Todas las Categorías</option>
                    {% set categories = [] %}
                    {% for p in products %}
                        {% if p.categoria and p.categoria not in categories %}
                            {% set _ = categories.append(p.categoria) %}
                        {% endif %}
                    {% endfor %}
                    {% for cat in categories|sort %}
                    <option value="{{ cat|lower }}">{{ cat }}</option>
                    {% endfor %}
                </select>
            </div>
            
            <!-- Price Sort -->
            <div class="md:w-56 shrink-0">
                <select id="catalog-sort" class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-white text-sm font-medium focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 outline-none transition-all shadow-sm appearance-none cursor-pointer">
                    <option value="">Orden por defecto</option>
                    <option value="price-asc">Precio: Menor a Mayor</option>
                    <option value="price-desc">Precio: Mayor a Menor</option>
                </select>
            </div>
        </div>'''

if search_block in content:
    content = content.replace(search_block, new_controls)

# 2. Update Catalog Card Attrs
old_card = '''<div class="catalog-card bg-white rounded-2xl shadow-sm border border-slate-200/80 overflow-hidden card-hover"
                 data-name="{{ product.name|lower }}" data-desc="{{ (product.description or '')|lower }}">'''

new_card = '''<div class="catalog-card bg-white rounded-2xl shadow-sm border border-slate-200/80 overflow-hidden card-hover cursor-pointer"
                 data-id="{{ product.id }}"
                 data-name="{{ product.name|lower }}" 
                 data-desc="{{ (product.description or '')|lower }}"
                 data-price="{{ product.precio or 0 }}"
                 data-category="{{ (product.categoria or '')|lower }}"
                 data-img="{{ product.imagen_url or '/static/img/default-product.png' }}"
                 data-stock="{{ product.stock_actual }}"
                 data-unit="{{ product.unit }}"
                 data-raw-name="{{ product.name }}"
                 data-raw-desc="{{ product.description or 'Sin descripción' }}"
                 onclick="if(!event.target.closest('form')){ openProductModal(this); }">'''

if old_card in content:
    content = content.replace(old_card, new_card)

# 3. Add Pagination Container
grid_end = '''        </div>
    </div>
    {% endif %}'''

pag_controls = '''        </div>
        
        <!-- Pagination Controls -->
        <div id="pagination-controls" class="mt-8 flex flex-wrap items-center justify-center gap-1 sm:gap-2">
            <!-- Dynamically populated by JS -->
        </div>
    </div>
    {% endif %}'''

if grid_end in content:
    content = content.replace(grid_end, pag_controls)

# 4. Inject Modal & JS at exactly the end of the file, before </html> if there is one, or just append
modal_and_js = '''

<!-- Product Detail Modal -->
<div id="product-modal" class="fixed inset-0 z-[100] hidden opacity-0 transition-opacity duration-300">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-[#00205B]/80 backdrop-blur-[2px]" onclick="closeProductModal()"></div>
    
    <!-- Modal Dialog -->
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0">
        <div class="relative bg-white rounded-3xl shadow-2xl overflow-hidden text-left transform scale-95 transition-all duration-300 sm:max-w-2xl w-full flex flex-col max-h-[90vh]" id="product-modal-dialog">
            
            <!-- Close Button -->
            <button onclick="closeProductModal()" type="button" class="absolute top-4 right-4 w-9 h-9 flex items-center justify-center bg-white/80 hover:bg-white border text-slate-500 rounded-full shadow-sm z-20 transition-colors">
                <svg class="w-5 h-5 font-bold" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>

            <div class="flex flex-col sm:flex-row h-full overflow-y-auto custom-scrollbar">
                <!-- Image Side -->
                <div class="w-full sm:w-2/5 shrink-0 bg-slate-50 relative min-h-[300px] flex items-center justify-center border-b sm:border-b-0 sm:border-r border-slate-100 p-6">
                    <img id="modal-img" src="" class="w-full h-full object-contain drop-shadow-md transition-all duration-500 hover:scale-105">
                </div>
                
                <!-- Content Side -->
                <div class="w-full sm:w-3/5 p-6 sm:p-8 flex flex-col overflow-y-auto">
                    <div class="mb-4 flex-1">
                        <span id="modal-stock-badge" class="inline-block px-3 py-1 text-[11px] font-extrabold tracking-wide uppercase rounded-full mb-3 text-white shadow-sm"></span>
                        <h3 id="modal-name" class="text-xl sm:text-2xl font-extrabold text-slate-800 leading-tight mb-3"></h3>
                        <p id="modal-desc" class="text-sm text-slate-500 font-medium leading-relaxed"></p>
                    </div>
                    
                    <div class="mt-4 pt-4 border-t border-slate-100 shrink-0">
                        <div class="flex items-end justify-between">
                            <div>
                                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Precio Unitario</p>
                                <p class="text-3xl font-extrabold text-[#FAAC2A]">S/ <span id="modal-price"></span></p>
                            </div>
                            <span id="modal-unit" class="text-[11px] font-bold text-indigo-700 bg-indigo-50 border border-indigo-100 px-2 py-1 rounded-lg"></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
/* Custom scrollbar for modal */
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>

<script>
const itemsPerPage = 18;
let currentPage = 1;
let allCards = [];
let filteredCards = [];

function initCatalog() {
    const catalogContainer = document.getElementById('product-catalog');
    if (!catalogContainer) return;
    
    allCards = Array.from(catalogContainer.querySelectorAll('.catalog-card'));
    filteredCards = [...allCards];
    
    const searchEl = document.getElementById('catalog-search');
    const catEl = document.getElementById('catalog-category-filter');
    const sortEl = document.getElementById('catalog-sort');
    
    if(searchEl) searchEl.addEventListener('input', applyFilters);
    if(catEl) catEl.addEventListener('change', applyFilters);
    if(sortEl) sortEl.addEventListener('change', applyFilters);
    
    renderPage(1);
}

function applyFilters() {
    const searchEl = document.getElementById('catalog-search');
    const catEl = document.getElementById('catalog-category-filter');
    const sortEl = document.getElementById('catalog-sort');
    
    const searchQ = searchEl ? searchEl.value.toLowerCase() : '';
    const catQ = catEl ? catEl.value : '';
    const sortQ = sortEl ? sortEl.value : '';
    
    // Filter
    filteredCards = allCards.filter(card => {
        const name = card.dataset.name;
        const desc = card.dataset.desc;
        const cat = card.dataset.category;
        
        const matchSearch = (name.includes(searchQ) || desc.includes(searchQ));
        const matchCat = (catQ === '' || cat === catQ);
        return matchSearch && matchCat;
    });
    
    // Sort
    if (sortQ === 'price-asc') {
        filteredCards.sort((a, b) => parseFloat(a.dataset.price) - parseFloat(b.dataset.price));
    } else if (sortQ === 'price-desc') {
        filteredCards.sort((a, b) => parseFloat(b.dataset.price) - parseFloat(a.dataset.price));
    } else {
        // default order by ID originally (or name)
        filteredCards.sort((a, b) => a.dataset.name.localeCompare(b.dataset.name));
    }
    
    renderPage(1);
}

function renderPage(page) {
    currentPage = page;
    const catalogContainer = document.getElementById('product-catalog');
    if(!catalogContainer) return;
    
    // Hide all
    allCards.forEach(card => { card.style.display = 'none'; catalogContainer.appendChild(card); }); 
    
    const startIdx = (page - 1) * itemsPerPage;
    const endIdx = startIdx + itemsPerPage;
    const pageCards = filteredCards.slice(startIdx, endIdx);
    
    // Show page cards
    pageCards.forEach(card => {
        card.style.display = 'block';
        catalogContainer.appendChild(card);
    });
    
    renderPagination();
}

function renderPagination() {
    const container = document.getElementById('pagination-controls');
    if(!container) return;
    container.innerHTML = '';
    const totalPages = Math.ceil(filteredCards.length / itemsPerPage);
    if (totalPages <= 1) {
        if(filteredCards.length === 0) {
            container.innerHTML = '<span class="text-sm font-medium text-slate-400">No se encontraron productos</span>';
        }
        return;
    }
    
    // Prev
    const prevBtn = document.createElement('button');
    prevBtn.innerHTML = '&laquo;';
    prevBtn.className = `w-8 sm:w-10 h-8 sm:h-10 flex items-center justify-center rounded-xl text-sm font-bold transition-colors ${currentPage === 1 ? 'text-slate-300 cursor-not-allowed bg-slate-50' : 'text-slate-600 hover:bg-indigo-50 hover:text-indigo-600 bg-white border border-slate-200'}`;
    prevBtn.onclick = () => { if(currentPage > 1) renderPage(currentPage - 1); };
    container.appendChild(prevBtn);
    
    // Pages
    let startP = Math.max(1, currentPage - 2);
    let endP = Math.min(totalPages, currentPage + 2);
    
    if (startP > 1) {
        const firstBtn = document.createElement('button');
        firstBtn.innerText = '1';
        firstBtn.className = `w-8 sm:w-10 h-8 sm:h-10 flex items-center justify-center rounded-xl text-sm font-bold transition-all text-slate-600 hover:bg-slate-100 bg-white border border-slate-200`;
        firstBtn.onclick = () => renderPage(1);
        container.appendChild(firstBtn);
        if (startP > 2) {
            const dots = document.createElement('span');
            dots.innerText = '...';
            dots.className = 'px-1 text-slate-400 font-bold';
            container.appendChild(dots);
        }
    }
    
    for (let i = startP; i <= endP; i++) {
        const btn = document.createElement('button');
        btn.innerText = i;
        btn.className = `w-8 sm:w-10 h-8 sm:h-10 flex items-center justify-center rounded-xl text-sm font-bold transition-all ${currentPage === i ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100 bg-white border border-slate-200'}`;
        btn.onclick = () => renderPage(i);
        container.appendChild(btn);
    }
    
    if (endP < totalPages) {
        if (endP < totalPages - 1) {
            const dots = document.createElement('span');
            dots.innerText = '...';
            dots.className = 'px-1 text-slate-400 font-bold';
            container.appendChild(dots);
        }
        const lastBtn = document.createElement('button');
        lastBtn.innerText = totalPages;
        lastBtn.className = `w-8 sm:w-10 h-8 sm:h-10 flex items-center justify-center rounded-xl text-sm font-bold transition-all text-slate-600 hover:bg-slate-100 bg-white border border-slate-200`;
        lastBtn.onclick = () => renderPage(totalPages);
        container.appendChild(lastBtn);
    }
    
    // Next
    const nextBtn = document.createElement('button');
    nextBtn.innerHTML = '&raquo;';
    nextBtn.className = `w-8 sm:w-10 h-8 sm:h-10 flex items-center justify-center rounded-xl text-sm font-bold transition-colors ${currentPage === totalPages ? 'text-slate-300 cursor-not-allowed bg-slate-50' : 'text-slate-600 hover:bg-indigo-50 hover:text-indigo-600 bg-white border border-slate-200'}`;
    nextBtn.onclick = () => { if(currentPage < totalPages) renderPage(currentPage + 1); };
    container.appendChild(nextBtn);
}

// Modal Functions
window.openProductModal = function(card) {
    const modal = document.getElementById('product-modal');
    const dialog = document.getElementById('product-modal-dialog');
    
    document.getElementById('modal-img').src = card.dataset.img;
    document.getElementById('modal-name').innerText = card.dataset.rawName;
    document.getElementById('modal-desc').innerText = card.dataset.rawDesc;
    document.getElementById('modal-price').innerText = parseFloat(card.dataset.price).toFixed(2);
    document.getElementById('modal-unit').innerText = card.dataset.unit;
    
    const stock = parseInt(card.dataset.stock);
    const badge = document.getElementById('modal-stock-badge');
    badge.innerText = `STOCK DISPONIBLE: ${stock}`;
    badge.className = `inline-block px-3 py-1 text-[11px] font-extrabold tracking-wide uppercase rounded-full mb-4 text-white shadow-sm ${stock > 10 ? 'bg-emerald-500' : (stock > 0 ? 'bg-amber-500' : 'bg-red-500')}`;
    
    modal.classList.remove('hidden');
    // trigger reflow
    void modal.offsetWidth;
    modal.classList.remove('opacity-0');
    dialog.classList.remove('scale-95');
}

window.closeProductModal = function() {
    const modal = document.getElementById('product-modal');
    const dialog = document.getElementById('product-modal-dialog');
    
    modal.classList.add('opacity-0');
    dialog.classList.add('scale-95');
    setTimeout(() => { modal.classList.add('hidden'); }, 300);
}

document.addEventListener('DOMContentLoaded', initCatalog);
// Re-init on htmx swaps if necessary
document.body.addEventListener('htmx:afterSwap', function(evt) {
    if (evt.detail.target.id === 'order-items-list') {
        // Just added an item, catalog is static, no re-init needed
    }
});
</script>
{% endblock %}
'''

if '<!-- Product Detail Modal -->' not in content:
    content = content.replace('{% endblock %}', modal_and_js)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Script executed successfully and replaced all blocks.')

