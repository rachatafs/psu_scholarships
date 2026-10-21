/* =============================================
   PSU Phuket Scholarships — Main JS
   =============================================
   Table of Contents:
   1. Mobile Sidebar Toggle
   2. Dropdown Menus
   3. Navbar Scroll Shadow
   4. Login Modal Logic
   ============================================= */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Mobile Sidebar Toggle ────────────────────────────────
    const toggler = document.getElementById('navbarToggler');
    const navbar  = document.querySelector('.navbar');
    const closeBtn = document.getElementById('navbarClose');
    const backdrop = document.getElementById('navbarBackdrop');

    if (toggler && navbar) {
        // Open sidebar
        toggler.addEventListener('click', function (e) {
            e.stopPropagation();
            navbar.classList.add('sidebar-open');
            document.body.style.overflow = 'hidden'; // Prevent scrolling
        });

        // Close sidebar function
        const closeSidebar = () => {
            navbar.classList.remove('sidebar-open');
            document.body.style.overflow = '';
        };

        if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
        if (backdrop) backdrop.addEventListener('click', closeSidebar);
    }

    // ─── Dropdown (click on mobile, hover on desktop) ─────────
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(function (dropdown) {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        if (!toggle) return;

        toggle.addEventListener('click', function (e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                dropdown.classList.toggle('open');
                dropdowns.forEach(function (other) {
                    if (other !== dropdown) other.classList.remove('open');
                });
            }
        });
    });

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.dropdown')) {
            dropdowns.forEach(function (d) { d.classList.remove('open'); });
        }
    });

    // ─── Navbar scroll shadow ─────────────────────────────────
    const nav = document.querySelector('.navbar');
    if (nav) {
        window.addEventListener('scroll', function () {
            nav.style.boxShadow = window.scrollY > 10
                ? '0 4px 20px rgba(0,0,0,0.12)'
                : '0 2px 12px rgba(0,0,0,0.08)';
        });
    }

    // ─── Login Modal: close on Escape ─────────────────────────
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeLoginModal();
    });

});

// ─── Login Modal (global — called from onclick in HTML) ───────
function openLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeLoginModal(event) {
    const modal = document.getElementById('loginModal');
    if (!modal) return;
    if (!event || event.target === modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}