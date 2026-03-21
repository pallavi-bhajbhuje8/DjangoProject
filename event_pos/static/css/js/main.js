// ============================================================
// EVENTPOS — Main JavaScript
// Minimal, vanilla JS for interactivity
// ============================================================

document.addEventListener('DOMContentLoaded', function () {

    // ---------- Mobile Sidebar Toggle ----------
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function () {
            sidebar.classList.toggle('open');
            if (overlay) overlay.classList.toggle('show');
        });

        if (overlay) {
            overlay.addEventListener('click', function () {
                sidebar.classList.remove('open');
                overlay.classList.remove('show');
            });
        }
    }

    // ---------- Auto-dismiss alerts ----------
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert, index) {
        // Stagger delay
        setTimeout(function () {
            alert.style.animation = 'toastOut 0.35s ease forwards';
            setTimeout(function () {
                alert.remove();
            }, 400);
        }, 3500 + index * 500);
    });

    document.querySelectorAll('.alert-close').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const alert = btn.closest('.alert');
            alert.style.animation = 'toastOut 0.35s ease forwards';
            setTimeout(function () { alert.remove(); }, 400);
        });
    });

    // ---------- Add to Cart (AJAX) ----------
    document.querySelectorAll('.ajax-add-to-cart').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const url = form.action;
            const formData = new FormData(form);

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
                body: formData,
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data.success) {
                    // Update cart count badges
                    document.querySelectorAll('.cart-count-badge').forEach(function (el) {
                        el.textContent = data.cart_count;
                        el.style.display = data.cart_count > 0 ? 'flex' : 'none';
                    });

                    showToast('✓ ' + data.message);

                    // Button feedback
                    const btn = form.querySelector('button[type="submit"]');
                    if (btn) {
                        const originalHTML = btn.innerHTML;
                        btn.innerHTML = '✓ Added';
                        btn.style.background = 'var(--color-success)';
                        setTimeout(function () {
                            btn.innerHTML = originalHTML;
                            btn.style.background = '';
                        }, 1200);
                    }
                }
            })
            .catch(function (err) {
                console.error('Cart error:', err);
            });
        });
    });

    // ---------- Wishlist Toggle (AJAX) ----------
    document.querySelectorAll('.ajax-wishlist-toggle').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const url = btn.dataset.url;
            const csrf = btn.dataset.csrf;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrf,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data.success) {
                    if (data.added) {
                        btn.classList.add('wishlisted');
                        btn.innerHTML = '♥';
                        showToast('♥ Added to wishlist');
                    } else {
                        btn.classList.remove('wishlisted');
                        btn.innerHTML = '♡';
                        showToast('Removed from wishlist');
                    }
                }
            });
        });
    });

    // ---------- Product Gallery Thumbs ----------
    const mainImage = document.querySelector('.product-gallery-main img');
    const thumbs = document.querySelectorAll('.product-gallery-thumb');

    thumbs.forEach(function (thumb) {
        thumb.addEventListener('click', function () {
            const src = thumb.dataset.src;
            if (mainImage && src) {
                mainImage.style.opacity = '0';
                setTimeout(function () {
                    mainImage.src = src;
                    mainImage.style.opacity = '1';
                }, 200);
                thumbs.forEach(function (t) { t.classList.remove('active'); });
                thumb.classList.add('active');
            }
        });
    });

    // ---------- Quantity Controls ----------
    document.querySelectorAll('.quantity-control').forEach(function (control) {
        const decreaseBtn = control.querySelector('.qty-decrease');
        const increaseBtn = control.querySelector('.qty-increase');
        const valueEl = control.querySelector('.quantity-value');
        const input = control.querySelector('input[name="quantity"]');

        if (decreaseBtn && increaseBtn && valueEl) {
            decreaseBtn.addEventListener('click', function () {
                let val = parseInt(valueEl.textContent) || 1;
                if (val > 1) {
                    val--;
                    valueEl.textContent = val;
                    if (input) input.value = val;
                }
            });

            increaseBtn.addEventListener('click', function () {
                let val = parseInt(valueEl.textContent) || 1;
                val++;
                valueEl.textContent = val;
                if (input) input.value = val;
            });
        }
    });

    // ---------- Star Rating Selector ----------
    const ratingStars = document.querySelectorAll('.rating-select .star-btn');
    const ratingInput = document.querySelector('input[name="rating"]');

    ratingStars.forEach(function (star) {
        star.addEventListener('click', function () {
            const val = star.dataset.value;
            if (ratingInput) ratingInput.value = val;

            ratingStars.forEach(function (s) {
                if (parseInt(s.dataset.value) <= parseInt(val)) {
                    s.classList.add('active');
                    s.innerHTML = '★';
                } else {
                    s.classList.remove('active');
                    s.innerHTML = '☆';
                }
            });
        });

        star.addEventListener('mouseenter', function () {
            const val = star.dataset.value;
            ratingStars.forEach(function (s) {
                if (parseInt(s.dataset.value) <= parseInt(val)) {
                    s.innerHTML = '★';
                } else {
                    s.innerHTML = '☆';
                }
            });
        });
    });

    const ratingSelectContainer = document.querySelector('.rating-select');
    if (ratingSelectContainer) {
        ratingSelectContainer.addEventListener('mouseleave', function () {
            const currentVal = ratingInput ? parseInt(ratingInput.value) || 0 : 0;
            ratingStars.forEach(function (s) {
                if (parseInt(s.dataset.value) <= currentVal) {
                    s.innerHTML = '★';
                } else {
                    s.innerHTML = '☆';
                }
            });
        });
    }

    // ---------- Scroll Reveal ----------
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal-on-scroll').forEach(function (el) {
        el.style.opacity = '0';
        observer.observe(el);
    });

    // ---------- Toast Helper ----------
    function showToast(message) {
        // Remove existing toasts
        document.querySelectorAll('.toast').forEach(function (t) { t.remove(); });

        var toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = '<span class="toast-icon">🛒</span> ' + message;
        document.body.appendChild(toast);

        setTimeout(function () {
            toast.remove();
        }, 3000);
    }

    // ---------- Search shortcut ----------
    document.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            var searchInput = document.querySelector('.search-input');
            if (searchInput) searchInput.focus();
        }
    });

    // ---------- Image lazy-load error fallback ----------
    document.querySelectorAll('img').forEach(function (img) {
        img.addEventListener('error', function () {
            img.src = 'https://images.unsplash.com/photo-1495195134817-aeb325a55b65?w=400&h=400&fit=crop';
            img.alt = 'Image unavailable';
        });
    });

});