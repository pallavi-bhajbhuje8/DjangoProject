// ============================================
// FitTrack - Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', function() {

    // ---- Sidebar Toggle ----
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
            overlay.classList.toggle('show');
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
        });
    }

    // ---- Auto-dismiss alerts ----
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });

    // ---- Confirm Delete ----
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // ---- Active Sidebar Link ----
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');
    navLinks.forEach(function(link) {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        } else if (href === '/' && currentPath === '/') {
            link.classList.add('active');
        }
    });

    // ---- Animate stat cards on scroll ----
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.stat-card, .dashboard-card, .goal-card').forEach(function(el) {
        observer.observe(el);
    });

    // ---- Calorie auto-calculate (basic estimate) ----
    const workoutTypeField = document.getElementById('id_workout_type');
    const durationField = document.getElementById('id_duration');
    const caloriesField = document.getElementById('id_calories_burned');

    if (workoutTypeField && durationField && caloriesField) {
        const calorieRates = {
            'running': 11,
            'cycling': 8,
            'gym': 7,
            'yoga': 4,
            'swimming': 10,
            'walking': 5,
            'hiit': 13,
            'stretching': 3,
            'other': 6
        };

        function estimateCalories() {
            const type = workoutTypeField.value;
            const duration = parseInt(durationField.value) || 0;
            const rate = calorieRates[type] || 6;

            if (duration > 0 && (!caloriesField.value || caloriesField.dataset.autoFilled === 'true')) {
                caloriesField.value = Math.round(rate * duration);
                caloriesField.dataset.autoFilled = 'true';
            }
        }

        workoutTypeField.addEventListener('change', estimateCalories);
        durationField.addEventListener('input', estimateCalories);

        caloriesField.addEventListener('input', function() {
            caloriesField.dataset.autoFilled = 'false';
        });
    }

    // ---- Tooltip init ----
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

});

// ---- Chart Helper Functions ----
function createLineChart(canvasId, labels, data, label, color) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: color,
                backgroundColor: color + '20',
                borderWidth: 2.5,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: color,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 11
                        },
                        color: '#7f8c8d'
                    }
                },
                y: {
                    grid: {
                        color: '#f0f0f0'
                    },
                    ticks: {
                        font: {
                            size: 11
                        },
                        color: '#7f8c8d'
                    }
                }
            }
        }
    });
}

function createBarChart(canvasId, labels, data, label, color) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: color + '90',
                borderColor: color,
                borderWidth: 1.5,
                borderRadius: 6,
                barPercentage: 0.6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 11
                        },
                        color: '#7f8c8d'
                    }
                },
                y: {
                    grid: {
                        color: '#f0f0f0'
                    },
                    ticks: {
                        font: {
                            size: 11
                        },
                        color: '#7f8c8d'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

function createDoughnutChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff',
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 16,
                        usePointStyle: true,
                        pointStyleWidth: 10,
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });
}