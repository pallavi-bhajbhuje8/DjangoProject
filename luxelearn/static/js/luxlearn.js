document.addEventListener('DOMContentLoaded', function () {

    // ── Mobile sidebar ──
    var menuBtn = document.querySelector('.menu-toggle');
    var sidebar = document.querySelector('.sidebar');
    var overlay = document.querySelector('.sidebar-overlay');

    if (menuBtn && sidebar) {
        menuBtn.addEventListener('click', function () {
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

    // ── Auto dismiss alerts ──
    document.querySelectorAll('.alert').forEach(function (a, i) {
        setTimeout(function () {
            a.style.animation = 'alertIn 0.3s ease reverse forwards';
            setTimeout(function () { a.remove(); }, 350);
        }, 3500 + i * 400);
    });

    document.querySelectorAll('.alert-close').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var a = btn.closest('.alert');
            a.style.animation = 'alertIn 0.3s ease reverse forwards';
            setTimeout(function () { a.remove(); }, 350);
        });
    });

    // ── Star rating ──
    var stars = document.querySelectorAll('.rating-select .star-btn');
    var ratingInput = document.querySelector('input[name="rating"]');

    stars.forEach(function (s) {
        s.addEventListener('click', function () {
            var v = s.dataset.value;
            if (ratingInput) ratingInput.value = v;
            stars.forEach(function (x) {
                x.classList.toggle('active', parseInt(x.dataset.value) <= parseInt(v));
                x.textContent = parseInt(x.dataset.value) <= parseInt(v) ? '★' : '☆';
            });
        });
        s.addEventListener('mouseenter', function () {
            var v = s.dataset.value;
            stars.forEach(function (x) {
                x.textContent = parseInt(x.dataset.value) <= parseInt(v) ? '★' : '☆';
            });
        });
    });

    var ratingWrap = document.querySelector('.rating-select');
    if (ratingWrap) {
        ratingWrap.addEventListener('mouseleave', function () {
            var cur = ratingInput ? parseInt(ratingInput.value) || 0 : 0;
            stars.forEach(function (x) {
                x.textContent = parseInt(x.dataset.value) <= cur ? '★' : '☆';
            });
        });
    }

    // ── Module toggle ──
    document.querySelectorAll('.module-header').forEach(function (h) {
        h.addEventListener('click', function () {
            var list = h.nextElementSibling;
            if (list && list.classList.contains('lesson-list')) {
                var showing = list.style.display !== 'none';
                list.style.display = showing ? 'none' : 'block';
                h.querySelector('.toggle-ico').textContent = showing ? '▸' : '▾';
            }
        });
    });

    // ── Keyboard shortcut ──
    document.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            var s = document.querySelector('.search-input');
            if (s) s.focus();
        }
    });

    // ── Image fallback ──
    document.querySelectorAll('img').forEach(function (img) {
        img.addEventListener('error', function () {
            img.src = 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=300&fit=crop';
        });
    });

});