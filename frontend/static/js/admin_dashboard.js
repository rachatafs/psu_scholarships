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
                btnSubmitText.textContent = this.checked ? 'Save & Send Email' : 'Save Status (No Email)';
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
            subject = `[PSU Phuket Scholarships] Additional Documents Required for ${schTitle}`;
            message = `Dear ${studentName},\n\nRegarding your application for the "${schTitle}" scholarship:\nUpon reviewing your application, additional documentation is required to complete the verification process.\n\nPlease submit the following documents:\n1. [Specify required documents, e.g. official transcript / household income certificate]\n2. Submission deadline: [e.g. Within 3 business days]\n3. Submission channel: [Reply to this email or submit to Student Affairs Office]\n\nThank you,\nStudent Affairs Division, PSU Phuket`;
        } else if (key === 'in_progress') {
            subject = `[PSU Phuket Scholarships] Application Status: In Progress for ${schTitle}`;
            message = `Dear ${studentName},\n\nYour application for "${schTitle}" is currently under review by the scholarship committee.\n\nPlease monitor your profile dashboard or email for further updates.\n\nBest regards,\nStudent Affairs Division, PSU Phuket`;
        } else if (key === 'interview') {
            subject = `[PSU Phuket Scholarships] Interview Invitation for ${schTitle}`;
            message = `Dear ${studentName},\n\nCongratulations! You have passed the preliminary screening for "${schTitle}".\nYou are invited to attend an interview with details as follows:\n\n- Date: [Specify date, e.g. Oct 28, 2026]\n- Time: [Specify time, e.g. 09:30 - 10:00 AM]\n- Location / Link: [Specify room or Zoom/Google Meet link]\n- Items to bring: [e.g. Student ID card, Portfolio]\n\nIf you have any scheduling conflicts, please contact Student Affairs promptly.\n\nBest regards,\nStudent Affairs Division, PSU Phuket`;
        } else if (key === 'reschedule') {
            subject = `[PSU Phuket Scholarships] Interview Rescheduled for ${schTitle}`;
            message = `Dear ${studentName},\n\nPlease be informed that your interview for "${schTitle}" has been rescheduled:\n\n- New Date: [Specify date]\n- New Time: [Specify time]\n- Location / Link: [Room or online link]\n\nWe apologize for the inconvenience.\n\nBest regards,\nStudent Affairs Division, PSU Phuket`;
        } else if (key === 'approved') {
            subject = `[PSU Phuket Scholarships] Congratulations! Scholarship Approved for ${schTitle}`;
            message = `Dear ${studentName},\n\nCongratulations! We are pleased to inform you that your application for "${schTitle}" has been APPROVED.\n\nNext steps for grant confirmation:\n1. Submit a copy of your bank passbook (account holder name must match student) to Student Affairs.\n2. Submission deadline: [Specify date]\n3. The scholarship funds will be transferred upon verification.\n\nCongratulations once again on your achievement!\n\nBest regards,\nStudent Affairs Division, PSU Phuket`;
        } else if (key === 'completed') {
            subject = `[PSU Phuket Scholarships] Scholarship Completed for ${schTitle}`;
            message = `Dear ${studentName},\n\nWe would like to inform you that the scholarship disbursement process for "${schTitle}" is now complete.\n\nWe wish you all the best in your continued studies at PSU Phuket.\n\nBest regards,\nStudent Affairs Division, PSU Phuket`;
        } else if (key === 'rejected') {
            subject = `[PSU Phuket Scholarships] Application Outcome for ${schTitle}`;
            message = `Dear ${studentName},\n\nThank you for applying for the "${schTitle}" scholarship.\nAfter careful review by the scholarship committee, we regret to inform you that we are unable to offer you a scholarship this round due to high applicant volume and limited quotas.\n\nWe encourage you to apply for upcoming scholarship opportunities in future terms.\n\nBest regards,\nStudent Affairs Division, PSU Phuket`;
        } else if (key === 'cancelled') {
            subject = `[PSU Phuket Scholarships] Application Cancelled for ${schTitle}`;
            message = `Dear ${studentName},\n\nYour application for "${schTitle}" has been cancelled.\nIf you did not request this cancellation or have any questions, please contact the Student Affairs Division.\n\nBest regards,\nStudent Affairs Division, PSU Phuket`;
        } else if (key === 'general') {
            subject = `[PSU Phuket Scholarships] Notification Regarding ${schTitle}`;
            message = `Dear ${studentName},\n\nStudent Affairs Division, Prince of Songkla University, Phuket Campus would like to share the following update regarding your application for "${schTitle}":\n\n[Write your message here...]\n\nBest regards,\nStudent Affairs Division, PSU Phuket`;
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
        if (modalStudentEmail) modalStudentEmail.textContent = context.studentEmail || 'No email in system';
        if (modalSchTitle) modalSchTitle.textContent = context.schTitle;
        if (modalAppNote) modalAppNote.value = context.existingNote || '';

        // Status badge color & prefix text
        if (modalStatusLabelPrefix) {
            modalStatusLabelPrefix.textContent = context.isNoticeOnly ? 'Current Status: ' : 'Change Status to: ';
        }

        if (modalStatusBadge) {
            modalStatusBadge.textContent = context.statusLabel;
            const s = context.isNoticeOnly ? context.currentStatus : context.targetStatus;
            if (s === 'interview' || s === 'in_progress') {
                modalStatusBadge.style.background = '#e0f2fe';
                modalStatusBadge.style.color = '#0369a1';
            } else if (s === 'approved') {
                modalStatusBadge.style.background = '#dcfce7';
                modalStatusBadge.style.color = '#15803d';
            } else if (s === 'completed') {
                modalStatusBadge.style.background = '#f3e8ff';
                modalStatusBadge.style.color = '#7e22ce';
            } else if (s === 'rejected') {
                modalStatusBadge.style.background = '#fee2e2';
                modalStatusBadge.style.color = '#b91c1c';
            } else if (s === 'cancelled') {
                modalStatusBadge.style.background = '#f1f5f9';
                modalStatusBadge.style.color = '#475569';
            } else {
                modalStatusBadge.style.background = '#fef3c7';
                modalStatusBadge.style.color = '#b45309';
            }
        }

        // Set matching template in dropdown and populate text
        let initialTmplKey = 'general';
        if (!context.isNoticeOnly) {
            if (context.targetStatus === 'in_progress') initialTmplKey = 'in_progress';
            else if (context.targetStatus === 'interview') initialTmplKey = 'interview';
            else if (context.targetStatus === 'approved') initialTmplKey = 'approved';
            else if (context.targetStatus === 'completed') initialTmplKey = 'completed';
            else if (context.targetStatus === 'rejected') initialTmplKey = 'rejected';
            else if (context.targetStatus === 'cancelled') initialTmplKey = 'cancelled';
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
            btnSubmitText.textContent = context.isNoticeOnly ? 'Send Notice' : 'Save & Send Email';
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

        let statusLabel = 'Pending';
        if (currentStatus === 'in_progress') statusLabel = 'In Progress';
        else if (currentStatus === 'interview') statusLabel = 'Interview';
        else if (currentStatus === 'approved') statusLabel = 'Approve';
        else if (currentStatus === 'completed') statusLabel = 'Complete';
        else if (currentStatus === 'rejected') statusLabel = 'Reject';
        else if (currentStatus === 'cancelled') statusLabel = 'Cancel';

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
            if (!confirm('Are you sure you want to reset this application status to "Pending"?')) {
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
                        statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: #d97706;"></span><span style="color: #b45309;">Pending</span></div>';
                    }
                    const btnGroup = form.closest('.action-btn-group');
                    const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;
                    const actionUrl = form.action;

                    btnGroup.innerHTML = `
                        <form method="post" action="${actionUrl}">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <input type="hidden" name="status" value="in_progress">
                            <button type="submit" class="btn-table-action btn-act-inprogress" title="Change to In Progress">In Progress</button>
                        </form>
                        <form method="post" action="${actionUrl}">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <input type="hidden" name="status" value="approved">
                            <button type="submit" class="btn-table-action btn-act-approve" title="Approve application">Approve</button>
                        </form>
                        <form method="post" action="${actionUrl}">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <input type="hidden" name="status" value="rejected">
                            <button type="submit" class="btn-table-action btn-act-reject" title="Reject application">Reject</button>
                        </form>
                        <form method="post" action="${actionUrl}">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <input type="hidden" name="status" value="cancelled">
                            <button type="submit" class="btn-table-action btn-act-cancel" title="Cancel application">Cancel</button>
                        </form>
                        <button type="button" class="btn-table-action btn-act-notice" title="Send notice / Request additional documents" onclick="openDirectNoticeModal(this)">
                            Additional Docs
                        </button>
                    `;
                }
            })
            .catch(err => {
                console.error(err);
                btn.innerHTML = originalBtnText;
                btn.disabled = false;
                alert('Error resetting application status.');
            });
            return;
        }

        // For in_progress, interview, approved, completed, rejected, cancelled: Open the Email & Status Modal!
        e.preventDefault();
        e.stopPropagation();

        const appId = row.getAttribute('data-app-id') || form.action.split('/').filter(Boolean).slice(-2, -1)[0];
        const studentName = row.getAttribute('data-student-name') || row.querySelector('td:nth-child(1) .font-bold')?.textContent.trim() || '';
        const studentId = row.getAttribute('data-student-id') || row.querySelector('.id-badge')?.textContent.trim() || '';
        const studentEmail = row.getAttribute('data-student-email') || '';
        const schTitle = row.getAttribute('data-sch-title') || row.querySelector('.table-sch-title')?.textContent.trim() || '';
        const existingNote = row.getAttribute('data-note') || '';

        let statusLabel = 'Pending';
        if (targetStatus === 'in_progress') statusLabel = 'In Progress';
        else if (targetStatus === 'interview') statusLabel = 'Interview';
        else if (targetStatus === 'approved') statusLabel = 'Approve';
        else if (targetStatus === 'completed') statusLabel = 'Complete';
        else if (targetStatus === 'rejected') statusLabel = 'Reject';
        else if (targetStatus === 'cancelled') statusLabel = 'Cancel';

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
                                    statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: #d97706;"></span><span style="color: #b45309;">Pending</span></div>';
                                } else if (data.status === 'in_progress' || data.status === 'interview') {
                                    statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: #0284c7;"></span><span style="color: #0369a1;">In Progress</span></div>';
                                } else if (data.status === 'approved') {
                                    statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: #059669;"></span><span style="color: #047857;">Approve</span></div>';
                                } else if (data.status === 'completed') {
                                    statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: #7e22ce;"></span><span style="color: #6b21a8;">Complete</span></div>';
                                } else if (data.status === 'cancelled') {
                                    statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: #64748b;"></span><span style="color: #475569;">Cancel</span></div>';
                                } else {
                                    statusCell.innerHTML = '<div style="display: flex; align-items: center; gap: 6px; font-size: 0.85rem; font-weight: 600;"><span class="dot-live" style="background: #dc2626;"></span><span style="color: #b91c1c;">Reject</span></div>';
                                }
                            }

                            // Update Action Buttons
                            const btnGroup = row.querySelector('.action-btn-group');
                            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
                            const actionUrl = statusForm.action;

                            const noticeBtnHtml = `
                                <button type="button" class="btn-table-action btn-act-notice" title="Send notice / Request additional documents" onclick="openDirectNoticeModal(this)">
                                    Additional Docs
                                </button>
                            `;

                            let newButtons = '';
                            if (data.status === 'pending') {
                                newButtons += `
                                    <form method="post" action="${actionUrl}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="in_progress">
                                        <button type="submit" class="btn-table-action btn-act-inprogress" title="Change to In Progress">In Progress</button>
                                    </form>
                                    <form method="post" action="${actionUrl}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="approved">
                                        <button type="submit" class="btn-table-action btn-act-approve" title="Approve application">Approve</button>
                                    </form>
                                    <form method="post" action="${actionUrl}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="rejected">
                                        <button type="submit" class="btn-table-action btn-act-reject" title="Reject application">Reject</button>
                                    </form>
                                    <form method="post" action="${actionUrl}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="cancelled">
                                        <button type="submit" class="btn-table-action btn-act-cancel" title="Cancel application">Cancel</button>
                                    </form>
                                `;
                            } else if (data.status === 'in_progress' || data.status === 'interview') {
                                newButtons += `
                                    <form method="post" action="${actionUrl}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="approved">
                                        <button type="submit" class="btn-table-action btn-act-approve" title="Approve application">Approve</button>
                                    </form>
                                    <form method="post" action="${actionUrl}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="rejected">
                                        <button type="submit" class="btn-table-action btn-act-reject" title="Reject application">Reject</button>
                                    </form>
                                    <form method="post" action="${actionUrl}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="cancelled">
                                        <button type="submit" class="btn-table-action btn-act-cancel" title="Cancel application">Cancel</button>
                                    </form>
                                `;
                            } else if (data.status === 'approved') {
                                newButtons += `
                                    <form method="post" action="${actionUrl}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="completed">
                                        <button type="submit" class="btn-table-action btn-act-complete" title="Complete scholarship process">Complete</button>
                                    </form>
                                    <form method="post" action="${actionUrl}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="pending">
                                        <button type="submit" class="btn-table-action btn-act-reset" title="Reset status to Pending">Reset to Pending</button>
                                    </form>
                                `;
                            } else if (data.status === 'completed') {
                                newButtons += `
                                    <form method="post" action="${actionUrl}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="pending">
                                        <button type="submit" class="btn-table-action btn-act-reset" title="Reset status to Pending">Reset to Pending</button>
                                    </form>
                                `;
                            } else if (data.status === 'rejected' || data.status === 'cancelled') {
                                newButtons += `
                                    <form method="post" action="${actionUrl}">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                                        <input type="hidden" name="status" value="pending">
                                        <button type="submit" class="btn-table-action btn-act-reset" title="Reset status to Pending">Reset to Pending</button>
                                    </form>
                                `;
                            }

                            if (btnGroup) {
                                btnGroup.innerHTML = newButtons + noticeBtnHtml;
                            }
                        }
                    }

                    if (data.email_sent) {
                        alert('Operation completed and notification email sent successfully.');
                    } else if (data.email_error) {
                        alert('Data saved successfully (Email error: ' + data.email_error + ')');
                    } else {
                        alert('Data saved successfully in system.');
                    }
                } else {
                    alert('Error updating application data.');
                }
            })
            .catch(err => {
                console.error(err);
                alert('Server connection error.');
            })
            .finally(() => {
                if (submitBtn) submitBtn.disabled = false;
                if (submitText) submitText.textContent = originalText;
            });
        });
    }
});
