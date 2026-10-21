from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_application_received_email(application):
    """
    Sends an email to the student when their application is successfully submitted.
    """
    student = application.student
    scholarship = application.scholarship
    
    subject = f'[PSU Phuket Scholarships] ยืนยันการสมัครทุน {scholarship.title}'
    
    # We can use templates or simple strings, going with simple string for testing
    html_message = f"""
    <h2>เรียนคุณ {student.full_name},</h2>
    <p>ระบบได้รับใบสมัครทุนการศึกษา <strong>{scholarship.title}</strong> ของคุณเรียบร้อยแล้ว</p>
    <p>รหัสนักศึกษา: {student.student_id}</p>
    <p>โปรดรอประกาศผลการพิจารณาผ่านทางอีเมลนี้</p>
    <br>
    <p>ด้วยความเคารพ,</p>
    <p>หน่วยกิจการนักศึกษา ม.อ.ภูเก็ต</p>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[student.user.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_status_update_email(application, custom_subject=None, custom_message=None, is_notice=False):
    """
    Sends an email to the student when the admin updates their application status or sends a custom notice.
    Supports optional custom_subject, custom_message, and is_notice flag.
    """
    student = application.student
    scholarship = application.scholarship
    status = application.get_status_display()
    
    if custom_subject and custom_subject.strip():
        subject = custom_subject.strip()
    elif is_notice:
        subject = f'[PSU Phuket Scholarships] แจ้งเตือน/ข้อมูลเพิ่มเติม ทุน {scholarship.title}'
    else:
        subject = f'[PSU Phuket Scholarships] แจ้งผลการพิจารณาทุน {scholarship.title}'
    
    if custom_message and custom_message.strip():
        # Clean and preserve paragraph/line breaks
        import html
        escaped_text = html.escape(custom_message.strip())
        formatted_message = escaped_text.replace('\n', '<br>')
        
        status_line = (
            f"<p>ข้อความแจ้งเตือนเกี่ยวกับใบสมัครทุน <strong>{scholarship.title}</strong> ของคุณ (สถานะปัจจุบัน: <span style='display:inline-block; padding: 2px 8px; border-radius: 4px; font-weight: bold; background: #e0f2fe; color: #0369a1;'>{status}</span>):</p>"
            if is_notice else
            f"<p>สถานะใบสมัครทุน <strong>{scholarship.title}</strong> ของคุณได้รับการอัปเดตเป็น: <span style='display:inline-block; padding: 2px 8px; border-radius: 4px; font-weight: bold; background: #e0f2fe; color: #0369a1;'>{status}</span></p>"
        )
        
        content = f"""
        {status_line}
        <div style="background-color: #f8fafc; border-left: 4px solid #1e40af; padding: 14px 18px; margin: 18px 0; border-radius: 6px; font-size: 15px; color: #1e293b; line-height: 1.7;">
            {formatted_message}
        </div>
        """
    else:
        # Default message based on status
        content = f"<p>สถานะใบสมัครทุน <strong>{scholarship.title}</strong> ของคุณได้รับการอัปเดตเป็น: <strong>{status}</strong></p>"
        if application.status == 'approved':
            content += "<p>ขอแสดงความยินดีด้วยครับ! คุณได้รับทุนการศึกษานี้ โปรดรอการติดต่อกลับจากเจ้าหน้าที่เพื่อดำเนินการต่อไป</p>"
        elif application.status == 'rejected':
            content += "<p>ขอแสดงความเสียใจด้วยครับ คุณไม่ผ่านการพิจารณาสำหรับทุนการศึกษานี้ในครั้งนี้ ขอเป็นกำลังใจให้ในโอกาสหน้านะครับ</p>"
        elif application.status == 'interview':
            content += "<p>คุณผ่านการคัดเลือกเบื้องต้นและมีกำหนดการ <strong>นัดสัมภาษณ์</strong> เจ้าหน้าที่จะติดต่อกลับเพื่อแจ้งวันและเวลาอีกครั้งครับ</p>"
        
    html_message = f"""
    <div style="font-family: 'Sarabun', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #334155;">
        <h2 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px;">เรียนคุณ {student.full_name},</h2>
        {content}
        <br>
        <div style="border-top: 1px solid #e2e8f0; padding-top: 14px; font-size: 0.88rem; color: #64748b; line-height: 1.5;">
            <p style="margin: 0;">ด้วยความเคารพ,</p>
            <p style="margin: 4px 0 0; font-weight: bold; color: #1e293b;">หน่วยกิจการนักศึกษา มหาวิทยาลัยสงขลานครินทร์ วิทยาเขตภูเก็ต</p>
            <p style="margin: 2px 0 0; font-size: 0.8rem; color: #94a3b8;">Prince of Songkla University, Phuket Campus</p>
        </div>
    </div>
    """
    
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[student.user.email],
        html_message=html_message,
        fail_silently=False,
    )
