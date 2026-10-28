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
    const errorBox = document.getElementById('modalLoginError');
    if (errorBox) errorBox.style.display = 'none';
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

// ─── AJAX Login Form Submission (ไม่เปลี่ยนหน้าเมื่อกรอกรหัสผิด) ────────
document.addEventListener("DOMContentLoaded", function() {
    const loginForms = document.querySelectorAll('#modalLoginForm, #pageLoginForm');
    loginForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const isModal = form.id === 'modalLoginForm';
            const errorBox = isModal ? document.getElementById('modalLoginError') : document.getElementById('pageLoginError');
            const submitBtn = form.querySelector('button[type="submit"]');
            const passwordInput = form.querySelector('input[name="password"]');
            const originalBtnText = submitBtn ? submitBtn.textContent : 'เข้าสู่ระบบ';

            if (errorBox) errorBox.style.display = 'none';
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'กำลังตรวจสอบ...';
            }

            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
            .then(res => res.json().then(data => ({ ok: res.ok, status: res.status, data: data })))
            .then(result => {
                if (result.ok && result.data.success) {
                    if (submitBtn) submitBtn.textContent = 'เข้าสู่ระบบสำเร็จ!';
                    window.location.href = result.data.redirect_url || '/';
                } else {
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.textContent = originalBtnText;
                    }
                    if (errorBox) {
                        errorBox.textContent = result.data.message || 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง กรุณาตรวจสอบและลองใหม่อีกครั้ง';
                        errorBox.style.display = 'block';
                    }
                    if (passwordInput) {
                        passwordInput.value = '';
                        passwordInput.focus();
                    }
                }
            })
            .catch(err => {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalBtnText;
                }
                if (errorBox) {
                    errorBox.textContent = 'เกิดข้อผิดพลาดในการเชื่อมต่อ กรุณาลองใหม่อีกครั้ง';
                    errorBox.style.display = 'block';
                }
            });
        });
    });
});