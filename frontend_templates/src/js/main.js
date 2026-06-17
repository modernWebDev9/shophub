// ========================================
// SHARED JAVASCRIPT
// ========================================

// Language Switcher
function toggleLang() {
  const menu = document.getElementById('langMenu');
  if (menu) menu.classList.toggle('active');
}

function setLang(lang) {
  const menu = document.getElementById('langMenu');
  if (menu) menu.classList.remove('active');
  const btn = document.querySelector('.lang-btn');
  if (btn) btn.innerHTML = `🌐 ${lang.toUpperCase()} ▼`;
}

// Theme Toggle
function toggleTheme() {
  document.body.classList.toggle('dark');
  const btn = document.getElementById('themeBtn');
  if (btn) {
    btn.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙';
  }
  localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
}

// Mobile Menu
function toggleMobileMenu() {
  const menu = document.getElementById('mobileMenu');
  if (menu) menu.classList.toggle('active');
}

// Wishlist
function toggleWishlist(btn) {
  btn.classList.toggle('active');
  btn.textContent = btn.classList.contains('active') ? '❤️' : '🤍';
}

// Add to Cart
function addToCart(id) {
  const badge = document.querySelector('.cart-badge');
  if (badge) {
    const current = parseInt(badge.textContent) || 0;
    badge.textContent = current + 1;
    badge.style.transform = 'scale(1.3)';
    setTimeout(() => { badge.style.transform = 'scale(1)'; }, 300);
  }
  alert(`Product ${id} added to cart!`);
}

// Load products from API
async function loadProducts(url, containerId) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    const container = document.getElementById(containerId);
    if (container) {
      container.innerHTML = data.products.map(product => createProductCard(product)).join('');
    }
  } catch (error) {
    console.error('Error loading products:', error);
  }
}

// Create product card HTML
function createProductCard(product) {
  return `
    <div class="product-card animate-scaleIn">
      <div class="product-card-image">
        <img src="${product.image || 'https://placehold.co/400x400/ffedd5/orange?text=Product'}" alt="${product.name}" loading="lazy">
        ${product.badge ? `<span class="product-badge hot">${product.badge}</span>` : ''}
        <button class="wishlist-btn" onclick="toggleWishlist(this)">🤍</button>
      </div>
      <div class="product-card-body">
        <h3 class="product-card-title">${product.name}</h3>
        <div class="product-card-price">
          <span class="current">$${product.price}</span>
          ${product.compare_at_price ? `<span class="original">$${product.compare_at_price}</span>` : ''}
        </div>
        <div class="product-card-rating">
          <span class="stars">${'★'.repeat(Math.floor(product.rating || 0))}</span>
          <span style="color: var(--gray); font-size: 0.875rem;">(${product.reviews || 0})</span>
        </div>
        <div class="product-card-actions">
          <a href="product-detail.html?id=${product.id}" class="btn btn-secondary btn-sm">View</a>
          <button class="btn btn-primary btn-sm" onclick="addToCart(${product.id})">🛒 Add</button>
        </div>
      </div>
    </div>
  `;
}

// Close dropdowns on outside click
document.addEventListener('click', function(event) {
  const langMenu = document.getElementById('langMenu');
  if (langMenu && !event.target.closest('.lang-dropdown')) {
    langMenu.classList.remove('active');
  }
});

// Load saved theme
document.addEventListener('DOMContentLoaded', function() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.body.classList.add('dark');
    const btn = document.getElementById('themeBtn');
    if (btn) btn.textContent = '☀️';
  }
  
  // Sticky header on scroll
  const header = document.querySelector('.header');
  if (header) {
    window.addEventListener('scroll', function() {
      header.classList.toggle('scrolled', window.sc