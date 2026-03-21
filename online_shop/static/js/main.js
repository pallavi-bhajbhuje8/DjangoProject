// ========================================
// ONLINE SHOP - MAIN JAVASCRIPT
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.messages-container .alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Add slideOut animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);

    // Dashboard sidebar toggle for mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('dashboardSidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(e) {
            if (window.innerWidth < 992 && sidebar.classList.contains('show')) {
                if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                    sidebar.classList.remove('show');
                }
            }
        });
    }

    // Quantity increment/decrement buttons
    document.querySelectorAll('.qty-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const input = this.closest('.qty-group').querySelector('.qty-input');
            let val = parseInt(input.value) || 1;
            
            if (this.dataset.action === 'increase') {
                val++;
            } else if (this.dataset.action === 'decrease' && val > 1) {
                val--;
            }
            
            input.value = val;
        });
    });

    // Confirm delete dialogs
    document.querySelectorAll('[data-confirm]').forEach(function(el) {
        el.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // Product image zoom effect
    const productMainImg = document.querySelector('.product-detail-img');
    if (productMainImg) {
        productMainImg.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.02)';
            this.style.transition = 'transform 0.3s ease';
        });
        productMainImg.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
        });
    }

    // Slug auto-generation
    const nameInput = document.querySelector('input[name="product_name"], input[name="name"]');
    const slugInput = document.querySelector('input[name="slug"]');
    
    if (nameInput && slugInput && !slugInput.value) {
        nameInput.addEventListener('input', function() {
            slugInput.value = this.value
                .toLowerCase()
                .replace(/[^a-z0-9]+/g, '-')
                .replace(/(^-|-$)/g, '');
        });
    }
});