function switchAdminTab(tabName, autoStatusFilter = null) {
    const tabBtnApps = document.getElementById('tabBtnApps');
    const tabBtnSch = document.getElementById('tabBtnSch');
    const tabBtnHistory = document.getElementById('tabBtnHistory');
    
    const sectionApps = document.getElementById('sectionApps');
    const sectionScholarships = document.getElementById('sectionScholarships');
    const sectionHistory = document.getElementById('sectionHistory');
    
    const statusSelect = document.getElementById('adminStatusSelect');

    // Reset all tabs
    if(tabBtnApps) tabBtnApps.classList.remove('active');
    if(tabBtnSch) tabBtnSch.classList.remove('active');
    if(tabBtnHistory) tabBtnHistory.classList.remove('active');
    
    if(sectionApps) sectionApps.style.display = 'none';
    if(sectionScholarships) sectionScholarships.style.display = 'none';
    if(sectionHistory) sectionHistory.style.display = 'none';

    if (tabName === 'scholarships') {
        if(tabBtnSch) tabBtnSch.classList.add('active');
        if(sectionScholarships) sectionScholarships.style.display = 'block';
        
        const url = new URL(window.location);
        url.hash = 'scholarships';
        window.history.replaceState(null, '', url);
    } else if (tabName === 'history') {
        if(tabBtnHistory) tabBtnHistory.classList.add('active');
        if(sectionHistory) sectionHistory.style.display = 'block';
        
        const url = new URL(window.location);
        url.hash = 'history';
        window.history.replaceState(null, '', url);
    } else {
        if(tabBtnApps) tabBtnApps.classList.add('active');
        if(sectionApps) sectionApps.style.display = 'block';
        
        const url = new URL(window.location);
        url.hash = 'apps';
        window.history.replaceState(null, '', url);

        if (autoStatusFilter && statusSelect) {
            statusSelect.value = autoStatusFilter;
            statusSelect.dispatchEvent(new Event('change'));
        }
    }
}

// Global function to easily jump from Scholarship tab to Applications tab and filter
window.viewApplicantsForSch = function(schTitle) {
    // Set search input to scholarship title
    const searchInput = document.getElementById('adminSearchInput');
    if (searchInput) {
        searchInput.value = schTitle;
        
        // Push state so the Back button works
        const url = new URL(window.location);
        url.hash = 'apps';
        url.searchParams.set('q', schTitle);
        // If there is category or status, we can leave them or reset them
        url.searchParams.set('category', 'all');
        url.searchParams.set('status', 'all');
        window.history.pushState(null, '', url);
        
        // Make sure we are on apps tab
        switchAdminTab('apps');
        
        // Trigger filter
        searchInput.dispatchEvent(new Event('input'));
        
        // Also update the hidden category and tabs visually
        const categoryTabs = document.querySelectorAll('#categoryTabs .admin-cat-tab');
        categoryTabs.forEach(t => t.classList.remove('active'));
        const allTab = document.querySelector('#categoryTabs .admin-cat-tab[data-category="all"]');
        if(allTab) allTab.classList.add('active');
        
        const statusSelect = document.getElementById('adminStatusSelect');
        if(statusSelect) statusSelect.value = 'all';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Check URL hash for initial tab state
    if (window.location.hash.startsWith('#scholarships')) {
        switchAdminTab('scholarships');
    } else if (window.location.hash.startsWith('#history')) {
        switchAdminTab('history');
    } else if (window.location.hash.startsWith('#apps')) {
        switchAdminTab('apps');
    }

    // Handle browser Back/Forward buttons properly
    window.addEventListener('popstate', function() {
        if (window.location.hash.startsWith('#scholarships')) {
            switchAdminTab('scholarships');
        } else if (window.location.hash.startsWith('#history')) {
            switchAdminTab('history');
        } else {
            switchAdminTab('apps');
        }
        
        // Sync search input with URL
        const urlParams = new URLSearchParams(window.location.search);
        const searchInput = document.getElementById('adminSearchInput');
        if (searchInput) {
            searchInput.value = urlParams.get('q') || '';
            searchInput.dispatchEvent(new Event('input'));
        }
    });

    // 1. Applications Live Filtering
    const searchInput = document.getElementById('adminSearchInput');
    const statusSelect = document.getElementById('adminStatusSelect');
    const categoryTabs = document.querySelectorAll('#categoryTabs .admin-cat-tab');
    const hiddenCategory = document.getElementById('hiddenCategory');
    const appRows = document.querySelectorAll('.app-row');
    const visibleCountEl = document.getElementById('visibleCount');
    const noMatchesRow = document.getElementById('noMatchesRow');

    let currentCategory = hiddenCategory ? (hiddenCategory.value || 'all') : 'all';

    function applyAppFilters() {
        const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
        const selectedStatus = statusSelect ? statusSelect.value : 'all';
        let matchCount = 0;

        appRows.forEach(row => {
            const name = row.getAttribute('data-name') || '';
            const studentId = row.getAttribute('data-id') || '';
            const schTitle = row.getAttribute('data-sch') || '';
            const rowCat = row.getAttribute('data-category') || '';
            const rowStatus = row.getAttribute('data-status') || '';

            const matchesQuery = !query || 
                name.includes(query) || 
                studentId.includes(query) || 
                schTitle.includes(query);

            const matchesCat = (currentCategory === 'all') || (rowCat === currentCategory);
            const matchesStatus = (selectedStatus === 'all') || (rowStatus === selectedStatus);

            if (matchesQuery && matchesCat && matchesStatus) {
                row.style.display = '';
                matchCount++;
            } else {
                row.style.display = 'none';
            }
        });

        if (visibleCountEl) visibleCountEl.textContent = matchCount;
        if (noMatchesRow) noMatchesRow.style.display = (matchCount === 0 && appRows.length > 0) ? '' : 'none';
    }

    if (searchInput) searchInput.addEventListener('input', applyAppFilters);
    if (statusSelect) statusSelect.addEventListener('change', applyAppFilters);

    categoryTabs.forEach(tab => {
        tab.addEventListener('click', function (e) {
            e.preventDefault();
            categoryTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            currentCategory = this.getAttribute('data-category') || 'all';
            if (hiddenCategory) hiddenCategory.value = currentCategory;
            applyAppFilters();

            const url = new URL(window.location);
            url.searchParams.set('category', currentCategory);
            if (statusSelect) url.searchParams.set('status', statusSelect.value);
            if (searchInput && searchInput.value) url.searchParams.set('q', searchInput.value);
            else url.searchParams.delete('q');
            window.history.replaceState({}, '', url);
        });
    });

    applyAppFilters();

    // 2. Scholarships Table Live Filtering
    const schSearchInput = document.getElementById('schSearchInput');
    const schRows = document.querySelectorAll('.sch-row');
    const schVisibleCount = document.getElementById('schVisibleCount');
    const noSchMatchesRow = document.getElementById('noSchMatchesRow');
    const schCategoryTabs = document.querySelectorAll('#schCategoryTabs .admin-cat-tab');

    let currentSchCategory = 'all';

    function applySchFilters() {
        const query = schSearchInput ? schSearchInput.value.trim().toLowerCase() : '';
        let matchCount = 0;

        schRows.forEach(row => {
            const title = row.getAttribute('data-sch-title') || '';
            const cat = row.getAttribute('data-sch-cat') || '';
            const desc = row.getAttribute('data-sch-desc') || '';

            const matchesQuery = !query || title.includes(query) || cat.includes(query) || desc.includes(query);
            const matchesCat = (currentSchCategory === 'all') || (cat === currentSchCategory);

            if (matchesQuery && matchesCat) {
                row.style.display = '';
                matchCount++;
            } else {
                row.style.display = 'none';
            }
        });

        if (schVisibleCount) schVisibleCount.textContent = matchCount;
        if (noSchMatchesRow) noSchMatchesRow.style.display = (matchCount === 0 && schRows.length > 0) ? '' : 'none';
    }

    if (schSearchInput) {
        schSearchInput.addEventListener('input', applySchFilters);
    }

    if (schCategoryTabs) {
        schCategoryTabs.forEach(tab => {
            tab.addEventListener('click', function(e) {
                e.preventDefault();
                schCategoryTabs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                currentSchCategory = this.getAttribute('data-sch-cat-filter') || 'all';
                applySchFilters();
            });
        });
    }

    // 2.5 History Table Live Filtering
    const histSearchInput = document.getElementById('histSearchInput');
    const histRows = document.querySelectorAll('.hist-row');
    const noHistMatchesRow = document.getElementById('noHistMatchesRow');

    function applyHistFilters() {
        const query = histSearchInput ? histSearchInput.value.trim().toLowerCase() : '';
        let matchCount = 0;

        histRows.forEach(row => {
            const title = row.getAttribute('data-hist-title') || '';
            const cat = row.getAttribute('data-hist-cat') || '';
            const desc = row.getAttribute('data-hist-desc') || '';

            const matchesQuery = !query || title.includes(query) || cat.includes(query) || desc.includes(query);

            if (matchesQuery) {
                row.style.display = '';
                matchCount++;
            } else {
                row.style.display = 'none';
            }
        });

        if (noHistMatchesRow) noHistMatchesRow.style.display = (matchCount === 0 && histRows.length > 0) ? '' : 'none';
    }

    if (histSearchInput) {
        histSearchInput.addEventListener('input', applyHistFilters);
    }

    // ===== MODAL EMAIL & STATUS CUSTOMIZATION LOGIC =====
    const statusModal = document.getElementById('statusEmailModal');
    const statusForm = document.getElementById('statusEmailForm');
    const modalTargetStatus = document.getElementById('modalTargetStatus');
    const modalIsNotice = document.getElementById('modalIsNotice');
    const modalAppId = document.getElementById('modalAppId');
    const modalStudentName = document.getElementById('modalStudentName');
    const modalStudentId = document.getElementById('modalStudentId');
    const modalStudentEmail = document.getElementById('modalStudentEmail');
    const modalSchTitle = document.getElementById('modalSchTitle');
    const modalStatusBadge = document.getElementById('modalStatusBadge');
    const modalStatusLabelPrefix = document.getElementById('modalStatusLabelPrefix');
    const modalSendEmailCheck = document.getElementById('modalSendEmailCheck');
    const emailEditorSection = document.getElementById('emailEditorSection');
    const modalEmailSubject = document.getElementById('modalEmailSubject');
    const modalEmailMessage = document.getElementById('modalEmailMessage');
    const modalTemplateSelector = document.getElementById('modalTemplateSelector');
    const modalAppNote = document.getElementById('modalAppNote');
    const btnConfirmStatusSubmit = document.getElementById('btnConfirmStatusSubmit');
    const btnSubmitText = document.getElementById('btnSubmitText');

    let currentActionContext = null;

    // Toggle email editor when checkbox changes
    if (modalSendEmailCheck) {
        modalSendEmailCheck.addEventListener('change', function() {
            if (emailEditorSection) {
                emailEditorSection.style.display = this.checked ? 'block' : 'none';
            }
            if (btnSubmitText) {
                btnSubmitText.textContent = this.checked ? 'บันทึกและส่งอีเมล' : 'บันทึกสถานะ (ไม่ส่งอีเมล)';
            }
        });
    }

    // Template selector change event
    window.onTemplateSelectChange = function(key) {
        if (!currentActionContext) return;
        const studentName = currentActionContext.studentName;
        const schTitle = currentActionContext.schTitle;
        let subject = '';
        let message = '';

        if (key === 'request_docs') {
            subject = `[PSU Phuket Scholarships] แจ้งขอเอกสารประกอบการสมัครเพิ่มเติม ทุน ${schTitle}`;
            message = `เรียนคุณ ${studentName},\n\nตามที่คุณได้ยื่นสมัครทุนการศึกษา "${schTitle}" นั้น\nจากการตรวจสอบเอกสารเบื้องต้น ทางหน่วยกิจการนักศึกษาพบว่าเอกสารบางรายการยังไม่ครบถ้วนหรือไม่สมบูรณ์\n\nจึงขอความอนุเคราะห์ส่งเอกสารเพิ่มเติม ดังนี้:\n1. [ระบุชื่อเอกสารที่ต้องการ เช่น หนังสือรับรองรายได้ครอบครัว / สำเนาใบแสดงผลการเรียน]\n2. กำหนดส่งภายในวันที่: [ระบุวันที่ เช่น ภายใน 3 วันทำการ]\n3. ช่องทางการส่ง: [ส่งตอบกลับทางอีเมลนี้ หรือนำส่งที่ห้องกิจการนักศึกษา]\n\nหากพ้นกำหนดเวลาดังกล่าว ทางคณะกรรมการขอสงวนสิทธิ์ในการพิจารณาใบสมัครในรอบนี้ครับ\nขอบคุณครับ`;
        } else if (key === 'interview') {
            subject = `[PSU Phuket Scholarships] แจ้งนัดสัมภาษณ์ทุนการศึกษา ${schTitle}`;
            message = `เรียนคุณ ${studentName},\n\nขอแสดงความยินดีที่คุณผ่านการคัดเลือกคุณสมบัติเบื้องต้น สำหรับทุนการศึกษา "${schTitle}"\nหน่วยกิจการนักศึกษาขอเชิญคุณเข้ารับการสัมภาษณ์ โดยมีรายละเอียดดังนี้:\n\n- วันที่สัมภาษณ์: [ระบุวันที่ เช่น 28 ตุลาคม 2569]\n- เวลา: [ระบุเวลา เช่น 09:30 - 10:00 น.]\n- สถานที่ / ช่องทาง: [ระบุห้อง เช่น ห้องประชุม 5204 หรือ ลิงก์ Zoom/Google Meet]\n- สิ่งที่ต้องเตรียมมา: [เช่น แฟ้มสะสมผลงาน (Portfolio), บัตรนักศึกษา]\n\nหากมีข้อสงสัยหรือติดขัดเรื่องเวลา กรุณาติดต่อหน่วยกิจการนักศึกษาโดยเร็วครับ`;
        } else if (key === 'reschedule') {
            subject = `[PSU Phuket Scholarships] แจ้งเปลี่ยนแปลงกำหนดการสัมภาษณ์ทุน ${schTitle}`;
            message = `เรียนคุณ ${studentName},\n\nหน่วยกิจการนักศึกษาขอแจ้งเปลี่ยนแปลงกำหนดการสัมภาษณ์ สำหรับทุนการศึกษา "${schTitle}" ดังนี้:\n\n- วันที่ใหม่: [ระบุวันที่ เช่น 30 ตุลาคม 2569]\n- เวลาใหม่: [ระบุเวลา เช่น 13:30 น.]\n- สถานที่ / ช่องทาง: [ระบุห้อง หรือ ลิงก์ออนไลน์]\n\nขออภัยในความไม่สะดวก หากติดขัดหรือไม่สามารถมาตามเวลาดังกล่าวได้ กรุณาติดต่อกลับทันทีครับ`;
        } else if (key === 'approved') {
            subject = `[PSU Phuket Scholarships] แจ้งผลการอนุมัติทุนการศึกษา ${schTitle}`;
            message = `เรียนคุณ ${studentName},\n\nขอแสดงความยินดีด้วยเป็นอย่างยิ่ง! คุณผ่านการพิจารณาคัดเลือกและได้รับทุนการศึกษา "${schTitle}"\n\nขั้นตอนการยืนยันสิทธิ์และการรับมอบทุน:\n1. กรุณานำสำเนาหน้าสมุดบัญชีธนาคาร (ชื่อบัญชีตรงกับนักศึกษา) มาส่งที่หน่วยกิจการนักศึกษา\n2. กำหนดส่งเอกสารยืนยันสิทธิ์ภายในวันที่: [ระบุวันที่ เช่น 5 พฤศจิกายน 2569]\n3. เจ้าหน้าที่จะดำเนินการโอนเงินทุนหลังจากตรวจสอบเอกสารเรียบร้อยแล้ว\n\nขอแสดงความยินดีอีกครั้ง และขอให้มุ่งมั่นตั้งใจศึกษาเล่าเรียนต่อไปครับ`;
        } else if (key === 'rejected') {
            subject = `[PSU Phuket Scholarships] แจ้งผลการพิจารณาทุนการศึกษา ${schTitle}`;
            message = `เรียนคุณ ${studentName},\n\nตามที่คุณได้ยื่นสมัครทุนการศึกษา "${schTitle}" นั้น\nคณะกรรมการได้พิจารณาคุณสมบัติอย่างละเอียดแล้ว และขอแจ้งให้ทราบว่า ในครั้งนี้คุณยังไม่ผ่านการคัดเลือก เนื่องจากมีผู้สมัครจำนวนมากและโควตาทุนการศึกษามีจำกัด\n\n[ข้อเสนอแนะ: นักศึกษาสามารถติดตามและยื่นขอรับทุนการศึกษาประเภทอื่นๆ ในรอบถัดไปได้ครับ]\n\nขอเป็นกำลังใจให้ในการศึกษาเล่าเรียน และขอขอบคุณที่ให้ความสนใจสมัครทุนการศึกษาของมหาวิทยาลัยครับ`;
        } else if (key === 'general') {
            subject = `[PSU Phuket Scholarships] แจ้งข้อมูลเพิ่มเติม ทุน ${schTitle}`;
            message = `เรียนคุณ ${studentName},\n\nหน่วยกิจการนักศึกษา มหาวิทยาลัยสงขลานครินทร์ วิทยาเขตภูเก็ต มีข้อความแจ้งเกี่ยวกับทุนการศึกษา "${schTitle}" ของคุณ ดังนี้:\n\n[พิมพ์ข้อความหรือหมายเหตุที่ต้องการแจ้งที่นี่...]\n\nหากมีข้อสงสัยเพิ่มเติม สามารถติดต่อสอบถามได้ที่หน่วยกิจการนักศึกษาครับ`;
        }

        if (subject && modalEmailSubject) modalEmailSubject.value = subject;
        if (message && modalEmailMessage) modalEmailMessage.value = message;
    };

    window.resetEmailTemplate = function() {
        if (!currentActionContext) return;
        const currentKey = modalTemplateSelector ? modalTemplateSelector.value : 'custom';
        if (currentKey && currentKey !== 'custom') {
            window.onTemplateSelectChange(currentKey);
        } else {
            const fallbackKey = currentActionContext.isNoticeOnly ? 'request_docs' : currentActionContext.targetStatus;
            window.onTemplateSelectChange(fallbackKey);
        }
    };

    window.openStatusEmailModal = function(context) {
        currentActionContext = context;
        if (statusForm) statusForm.action = context.actionUrl;
        if (modalTargetStatus) modalTargetStatus.value = context.targetStatus || 'keep';
        if (modalIsNotice) modalIsNotice.value = context.isNoticeOnly ? 'true' : 'false';
        if (modalAppId) modalAppId.value = context.appId;
        if (modalStudentName) modalStudentName.textContent = context.studentName;
        if (modalStudentId) modalStudentId.textContent = `(${context.studentId})`;
        if (modalStudentEmail) modalStudentEmail.textContent = context.studentEmail || 'ไม่มีอีเมลในระบบ';
        if (modalSchTitle) modalSchTitle.textContent = context.schTitle;
        if (modalAppNote) modalAppNote.value = context.existingNote || '';

        // Status badge color & prefix text
        if (modalStatusLabelPrefix) {
            modalStatusLabelPrefix.textContent = context.isNoticeOnly ? 'สถานะปัจจุบัน: ' : 'เปลี่ยนสถานะเป็น: ';
        }

        if (modalStatusBadge) {
            modalStatusBadge.textContent = context.statusLabel;
            const s = context.isNoticeOnly ? context.currentStatus : context.targetStatus;
            if (s === 'interview') {
                modalStatusBadge.style.background = '#e0f2fe';
                modalStatusBadge.style.color = '#0369a1';
            } else if (s === 'approved') {
                modalStatusBadge.style.background = '#dcfce7';
                modalStatusBadge.style.color = '#15803d';
            } else if (s === 'rejected') {
                modalStatusBadge.style.background = '#fee2e2';
                modalStatusBadge.style.color = '#b91c1c';
            } else {
                modalStatusBadge.style.background = '#fef3c7';
                modalStatusBadge.style.color = '#b45309';
            }
        }

        // Set matching template in dropdown and populate text
        let initialTmplKey = 'general';
        if (!context.isNoticeOnly) {
            if (context.targetStatus === 'interview') initialTmplKey = 'interview';
            else if (context.targetStatus === 'approved') initialTmplKey = 'approved';
            else if (context.targetStatus === 'rejected') initialTmplKey = 'rejected';
        } else {
            initialTmplKey = 'request_docs';
        }

        if (modalTemplateSelector) {
            modalTemplateSelector.value = initialTmplKey;
        }
        window.onTemplateSelectChange(initialTmplKey);

        if (modalSendEmailCheck) {
            modalSendEmailCheck.checked = true;
            if (emailEditorSection) emailEditorSection.style.display = 'block';
        }
        if (btnSubmitText) {
            btnSubmitText.textContent = context.isNoticeOnly ? 'ส่งข้อความแจ้งเตือน' : 'บันทึกและส่งอีเมล';
        }

        if (statusModal) {
            statusModal.classList.add('open', 'active');
            document.body.style.overflow = 'hidden';
        }
    };

    // Open direct notice modal from button
    window.openDirectNoticeModal = function(btn) {
        const row = btn.closest('tr.app-row');
        if (!row) return;

        const appId = row.getAttribute('data-app-id') || '';
        const studentName = row.getAttribute('data-student-name') || '';
        const studentId = row.getAttribute('data-student-id') || '';
        const studentEmail = row.getAttribute('data-student-email') || '';
        const schTitle = row.getAttribute('data-sch-title') || '';
        const existingNote = row.getAttribute('data-note') || '';
        const currentStatus = row.getAttribute('data-status') || 'pending';

        let statusLabel = 'รอพิจารณา';
        if (currentStatus === 'interview') statusLabel = 'รอสัมภาษณ์';
        else if (currentStatus === 'approved') statusLabel = 'ผ่านการอนุมัติ';
        else if (currentStatus === 'rejected') statusLabel = 'ไม่อนุมัติ';

        openStatusEmailModal({
            formElement: null,
            actionUrl: `/application/${appId}/update/`,
            targetStatus: 'keep',
            currentStatus: currentStatus,
            statusLabel: statusLabel,
            appId: appId,
            studentName: studentName,
            studentId: studentId,
            studentEmail: studentEmail,
            schTitle: schTitle,
            existingNote: existingNote,
            rowElement: row,
            isNoticeOnly: true
        });
    };

    window.closeStatusEmailModal = function() {
        if (statusModal) {
            statusModal.classList.remove('open', 'active');
            document.body.style.overflow = '';
        }
    };

    window.handleStatusModalBackdrop = function(e) {
        if (e.target === statusModal) {
            closeStatusEmailModal();
        }
    };

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && statusModal && statusModal.classList.contains('active')) {
            closeStatusEmailModal();
        }
    });

    // Handle Click on Action Buttons in Application Table
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.action-btn-group button');
        if (!btn) return;

        // Skip if it's the direct notice button
        if (btn.classList.contains('btn-act-notice')) return;

        const form = btn.closest('form');
        if (!form) return;

        const statusInput = form.querySelector('input[name="status"]');
        if (!statusInput) return;

        const targetStatus = statusInput.value;
        const row = form.closest('tr.app-row');
        if (!row) return;

        // If target status is "pending" (Reset back):
        if (targetStatus === 'pending') {
            if (!confirm('คุณต้องการย้อนกลับสถานะใบสมัครนี้เป็น "รอพิจารณา" ใช่หรือไม่?')) {
                e.preventDefault();
                return;
            }
            e.preventDefault();
            const originalBtnText = btn.innerHTML;
            btn.innerHTML = '...';
            btn.disabled = true;

            const formData = new FormData(form);
            formData.set('send_email', 'false');

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    row.setAttribute('data-status', 'pending');
                    const statusCell = row.cells ? row.cells[5] : row.querySelector('td:nth-child(6)');
                    if (statusCell) {
                        statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: #d97706;"></span><span style="color: #b45309;">รอพิจารณา</span></div>';
                    }
                    const btnGroup = form.closest('.action-btn-group');
                    const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
                    const actionUrl = form.action;

                    btnGroup.innerHTML = `
                        <form method="post" action="${actionUrl}" style="width: 100%;">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <input type="hidden" name="status" value="interview">
                            <button type="submit" class="btn-table-action btn-act-interview" style="width: 100%;" title="นัดสัมภาษณ์">เรียกสัมภาษณ์</button>
                        </form>
                        <form method="post" action="${actionUrl}" style="width: 100%;">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <input type="hidden" name="status" value="approved">
                            <button type="submit" class="btn-table-action btn-act-approve" style="width: 100%;" title="อนุมัติใบสมัคร">อนุมัติให้ทุนเลย</button>
                        </form>
                        <form method="post" action="${actionUrl}" style="width: 100%;">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <input type="hidden" name="status" value="rejected">
                            <button type="submit" class="btn-table-action btn-act-reject" style="width: 100%;" title="ปฏิเสธใบสมัคร">ไม่อนุมัติ</button>
                        </form>
                        <button type="button" class="btn-table-action btn-act-notice" style="width: 100%; background: #f0f9ff; color: #0284c7; border: 1px solid #bae6fd; font-weight: 600; font-size: 0.76rem; padding: 5px 6px; margin-top: 2px; border-radius: 6px; cursor: pointer; transition: background 0.15s;" title="ส่งข้อความ/ขอเอกสาร/แจ้งเตือนนักศึกษา" onclick="openDirectNoticeModal(this)">
                            เพิ่มเติม
                        </button>
                    `;
                }
            })
            .catch(err => {
                console.error(err);
                btn.innerHTML = originalBtnText;
                btn.disabled = false;
                alert('เกิดข้อผิดพลาดในการย้อนกลับสถานะ');
            });
            return;
        }

        // For interview, approved, rejected: Open the Email & Status Modal!
        e.preventDefault();
        e.stopPropagation();

        const appId = row.getAttribute('data-app-id') || form.action.split('/').filter(Boolean).slice(-2, -1)[0];
        const studentName = row.getAttribute('data-student-name') || row.querySelector('td:nth-child(1) .font-bold')?.textContent.trim() || '';
        const studentId = row.getAttribute('data-student-id') || row.querySelector('.id-badge')?.textContent.trim() || '';
        const studentEmail = row.getAttribute('data-student-email') || '';
        const schTitle = row.getAttribute('data-sch-title') || row.querySelector('.table-sch-title')?.textContent.trim() || '';
        const existingNote = row.getAttribute('data-note') || '';

        let statusLabel = 'รอพิจารณา';
        if (targetStatus === 'interview') statusLabel = 'เรียกสัมภาษณ์';
        else if (targetStatus === 'approved') statusLabel = 'ผ่านการอนุมัติ';
        else if (targetStatus === 'rejected') statusLabel = 'ไม่อนุมัติ';

        openStatusEmailModal({
            formElement: form,
            actionUrl: form.action,
            targetStatus: targetStatus,
            statusLabel: statusLabel,
            appId: appId,
            studentName: studentName,
            studentId: studentId,
            studentEmail: studentEmail,
            schTitle: schTitle,
            existingNote: existingNote,
            rowElement: row,
            isNoticeOnly: false
        });
    });

    // Handle Modal Form Submission via AJAX
    if (statusForm) {
        statusForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const submitBtn = document.getElementById('btnConfirmStatusSubmit');
            const submitText = document.getElementById('btnSubmitText');
            const originalText = submitText ? submitText.textContent : 'บันทึก';

            if (submitBtn) submitBtn.disabled = true;
            if (submitText) submitText.textContent = 'กำลังส่งข้อมูล...';

            const formData = new FormData(statusForm);

            fetch(statusForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    closeStatusEmailModal();

                    if (currentActionContext && currentActionContext.rowElement) {
                        const row = currentActionContext.rowElement;
                        if (data.note) row.setAttribute('data-note', data.note);

                        // If status actually changed, update row visual state
                        if (data.status_changed) {
                            row.setAttribute('data-status', data.status);

                            // Update Status Badge cell (column 6)
                            const statusCell = row.cells ? row.cells[5] : row.querySelector('td:nth-child(6)');
                            if (statusCell) {
                                if (data.status === 'pending') {
                                    statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: #d97706;"></span><span style="color: #b45309;">รอพิจารณา</span></div>';
                                } else if (data.status === 'interview') {
                                    statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: var(--psu-blue-500);"></span><span style="color: var(--psu-blue-700);">รอสัมภาษณ์</span></div>';
                                } else if (data.status === 'approved') {
                                    statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: #059669;"></span><span style="color: #047857;">อนุมัติแล้ว</span></div>';
                                } else {
                                    statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: #dc2626;"></span><span style="color: #b91c1c;">ไม่อนุมัติ</span></div>';
                                }
                            }

                            // Update Action Buttons
                            const btnGroup = row.querySelector('.action-btn-group');
                            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                            const actionUrl = statusForm.action;

                            const noticeBtnHtml = `
                                <button type="button" class="btn-table-action btn-act-notice" style="width: 100%; background: #f0f9ff; color: #0284c7; border: 1px solid #bae6fd; font-weight: 600; font-size: 0.76rem; padding: 5px 6px; margin-top: 2px; border-radius: 6px; cursor: pointer; transition: background 0.15s;" title="ส่งข้อความ/ขอเอกสาร/แจ้งเตือนนักศึกษา" onclick="openDirectNoticeModal(this)">
                                    เพิ่มเติม
                                </button>
                            `;

                            let newButtons = '';
                            if (data.status === 'pending') {
                                newButtons += `
                                    <form method="post" action="${actionUrl}" style="width: 100%;">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="interview">
                                        <button type="submit" class="btn-table-action btn-act-interview" style="width: 100%;" title="นัดสัมภาษณ์">เรียกสัมภาษณ์</button>
                                    </form>
                                    <form method="post" action="${actionUrl}" style="width: 100%;">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="approved">
                                        <button type="submit" class="btn-table-action btn-act-approve" style="width: 100%;" title="อนุมัติใบสมัคร">อนุมัติให้ทุนเลย</button>
                                    </form>
                                    <form method="post" action="${actionUrl}" style="width: 100%;">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="rejected">
                                        <button type="submit" class="btn-table-action btn-act-reject" style="width: 100%;" title="ปฏิเสธใบสมัคร">ไม่อนุมัติ</button>
                                    </form>
                                `;
                            } else if (data.status === 'interview') {
                                newButtons += `
                                    <form method="post" action="${actionUrl}" style="width: 100%;">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="approved">
                                        <button type="submit" class="btn-table-action btn-act-approve" style="width: 100%;" title="อนุมัติใบสมัคร">ผ่านสัมภาษณ์ (ให้ทุน)</button>
                                    </form>
                                    <form method="post" action="${actionUrl}" style="width: 100%;">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="rejected">
                                        <button type="submit" class="btn-table-action btn-act-reject" style="width: 100%;" title="ปฏิเสธใบสมัคร">ไม่ผ่านสัมภาษณ์</button>
                                    </form>
                                `;
                            } else if (data.status === 'approved' || data.status === 'rejected') {
                                newButtons += `
                                    <form method="post" action="${actionUrl}" style="width: 100%;">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="pending">
                                        <button type="submit" class="btn-table-action" style="background-color: transparent; border: 1px solid #ccc; color: #666; font-size: 0.75rem; width: 100%;" title="รีเซ็ตสถานะ">ย้อนกลับ</button>
                                    </form>
                                `;
                            }

                            if (btnGroup) {
                                btnGroup.innerHTML = newButtons + noticeBtnHtml;
                            }
                        }
                    }

                    if (data.email_sent) {
                        alert('✅ ดำเนินการสำเร็จ และส่งอีเมลแจ้งนักศึกษาเรียบร้อยแล้ว!');
                    } else if (data.email_error) {
                        alert('⚠️ บันทึกข้อมูลสำเร็จ (แต่ไม่สามารถส่งอีเมลได้: ' + data.email_error + ')');
                    } else {
                        alert('✅ บันทึกข้อมูลในระบบเรียบร้อยแล้ว');
                    }
                } else {
                    alert('เกิดข้อผิดพลาดในการอัปเดตข้อมูล');
                }
            })
            .catch(err => {
                console.error(err);
                alert('เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์');
            })
            .finally(() => {
                if (submitBtn) submitBtn.disabled = false;
                if (submitText) submitText.textContent = originalText;
            });
        });
    }
});
