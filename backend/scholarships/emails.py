from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.utils import translation
import html


def send_application_received_email(application):
    """
    Sends an email to the student when their application is successfully submitted,
    localized according to their preferred language.
    """
    student = application.student
    scholarship = application.scholarship
    lang = getattr(student, 'preferred_language', 'th') or 'th'

    with translation.override(lang):
        sch_title = scholarship.localized_title if hasattr(scholarship, 'localized_title') else scholarship.title
        
        if lang == 'en':
            subject = f'[PSU Phuket Scholarships] Application Received: {sch_title}'
            html_message = f"""
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #334155;">
                <h2 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px;">Dear {student.full_name},</h2>
                <p>We have successfully received your scholarship application for <strong>{sch_title}</strong>.</p>
                <p><strong>Student ID:</strong> {student.student_id}</p>
                <p>Please await further evaluation updates and announcements via this email.</p>
                <br>
                <div style="border-top: 1px solid #e2e8f0; padding-top: 14px; font-size: 0.88rem; color: #64748b; line-height: 1.5;">
                    <p style="margin: 0;">Sincerely,</p>
                    <p style="margin: 4px 0 0; font-weight: bold; color: #1e293b;">Student Affairs &amp; Scholarships Division</p>
                    <p style="margin: 2px 0 0; font-size: 0.8rem; color: #94a3b8;">Prince of Songkla University, Phuket Campus</p>
                </div>
            </div>
            """
        else:
            subject = f'[PSU Phuket Scholarships] ยืนยันการสมัครทุน {sch_title}'
            html_message = f"""
            <div style="font-family: 'Sarabun', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #334155;">
                <h2 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px;">เรียนคุณ {student.full_name},</h2>
                <p>ระบบได้รับใบสมัครทุนการศึกษา <strong>{sch_title}</strong> ของคุณเรียบร้อยแล้ว</p>
                <p><strong>รหัสนักศึกษา:</strong> {student.student_id}</p>
                <p>โปรดรอประกาศผลการพิจารณาผ่านทางอีเมลนี้</p>
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
            fail_silently=True,
        )


def send_status_update_email(application, custom_subject=None, custom_message=None, is_notice=False):
    """
    Sends an email to the student when the admin updates their application status or sends a custom notice,
    localized according to their preferred language.
    """
    student = application.student
    scholarship = application.scholarship
    lang = getattr(student, 'preferred_language', 'th') or 'th'

    with translation.override(lang):
        sch_title = scholarship.localized_title if hasattr(scholarship, 'localized_title') else scholarship.title
        status_display = application.get_status_display()

        if lang == 'en':
            if custom_subject and custom_subject.strip():
                subject = custom_subject.strip()
            elif is_notice:
                subject = f'[PSU Phuket Scholarships] Notice / Additional Info Required: {sch_title}'
            else:
                subject = f'[PSU Phuket Scholarships] Application Status Update: {sch_title}'

            if custom_message and custom_message.strip():
                escaped_text = html.escape(custom_message.strip())
                formatted_message = escaped_text.replace('\n', '<br>')
                status_line = (
                    f"<p>Notification regarding your application for <strong>{sch_title}</strong> (Current status: <span style='display:inline-block; padding: 2px 8px; border-radius: 4px; font-weight: bold; background: #e0f2fe; color: #0369a1;'>{status_display}</span>):</p>"
                    if is_notice else
                    f"<p>The review status of your application for <strong>{sch_title}</strong> has been updated to: <span style='display:inline-block; padding: 2px 8px; border-radius: 4px; font-weight: bold; background: #e0f2fe; color: #0369a1;'>{status_display}</span></p>"
                )
                content = f"""
                {status_line}
                <div style="background-color: #f8fafc; border-left: 4px solid #1e40af; padding: 14px 18px; margin: 18px 0; border-radius: 6px; font-size: 15px; color: #1e293b; line-height: 1.7;">
                    {formatted_message}
                </div>
                """
            else:
                content = f"<p>The review status of your application for <strong>{sch_title}</strong> has been updated to: <strong>{status_display}</strong></p>"
                if application.status == 'approved':
                    content += "<p>Congratulations! Your scholarship application has been approved. Please await instructions from the scholarship committee.</p>"
                elif application.status == 'completed':
                    content += "<p>Scholarship disbursement and onboarding procedures are fully completed. We wish you continued success in your studies.</p>"
                elif application.status == 'in_progress':
                    content += "<p>Your application is actively undergoing review and document verification by the committee. Please monitor updates regularly.</p>"
                elif application.status == 'rejected':
                    content += "<p>We regret to inform you that your application was not selected for this cycle. We encourage you to apply for other available scholarships.</p>"
                elif application.status == 'cancelled':
                    content += "<p>Your scholarship application has been cancelled. For inquiries, please contact the Student Affairs Division.</p>"
                elif application.status == 'interview':
                    content += "<p>You have been shortlisted for an <strong>interview</strong>. Our team will contact you shortly with the schedule.</p>"

            html_message = f"""
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #334155;">
                <h2 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 12px;">Dear {student.full_name},</h2>
                {content}
                <br>
                <div style="border-top: 1px solid #e2e8f0; padding-top: 14px; font-size: 0.88rem; color: #64748b; line-height: 1.5;">
                    <p style="margin: 0;">Sincerely,</p>
                    <p style="margin: 4px 0 0; font-weight: bold; color: #1e293b;">Student Affairs &amp; Scholarships Division</p>
                    <p style="margin: 2px 0 0; font-size: 0.8rem; color: #94a3b8;">Prince of Songkla University, Phuket Campus</p>
                </div>
            </div>
            """
        else:
            if custom_subject and custom_subject.strip():
                subject = custom_subject.strip()
            elif is_notice:
                subject = f'[PSU Phuket Scholarships] แจ้งเตือน/ข้อมูลเพิ่มเติม ทุน {sch_title}'
            else:
                subject = f'[PSU Phuket Scholarships] แจ้งผลการพิจารณาทุน {sch_title}'

            if custom_message and custom_message.strip():
                escaped_text = html.escape(custom_message.strip())
                formatted_message = escaped_text.replace('\n', '<br>')
                status_line = (
                    f"<p>ข้อความแจ้งเตือนเกี่ยวกับใบสมัครทุน <strong>{sch_title}</strong> ของคุณ (สถานะปัจจุบัน: <span style='display:inline-block; padding: 2px 8px; border-radius: 4px; font-weight: bold; background: #e0f2fe; color: #0369a1;'>{status_display}</span>):</p>"
                    if is_notice else
                    f"<p>สถานะใบสมัครทุน <strong>{sch_title}</strong> ของคุณได้รับการอัปเดตเป็น: <span style='display:inline-block; padding: 2px 8px; border-radius: 4px; font-weight: bold; background: #e0f2fe; color: #0369a1;'>{status_display}</span></p>"
                )
                content = f"""
                {status_line}
                <div style="background-color: #f8fafc; border-left: 4px solid #1e40af; padding: 14px 18px; margin: 18px 0; border-radius: 6px; font-size: 15px; color: #1e293b; line-height: 1.7;">
                    {formatted_message}
                </div>
                """
            else:
                content = f"<p>สถานะใบสมัครทุน <strong>{sch_title}</strong> ของคุณได้รับการอัปเดตเป็น: <strong>{status_display}</strong></p>"
                if application.status == 'approved':
                    content += "<p>ขอแสดงความยินดีด้วยครับ! คุณได้รับทุนการศึกษานี้ โปรดรอการติดต่อกลับจากเจ้าหน้าที่เพื่อดำเนินการต่อไป</p>"
                elif application.status == 'completed':
                    content += "<p>กระบวนการรับมอบทุนการศึกษาและการดำเนินการที่เกี่ยวข้องเสร็จสมบูรณ์เรียบร้อยแล้ว ขอขอบคุณและขอให้ตั้งใจศึกษาเล่าเรียนครับ</p>"
                elif application.status == 'in_progress':
                    content += "<p>ใบสมัครของคุณอยู่ระหว่างการดำเนินการและตรวจสอบข้อมูล/เอกสารโดยคณะกรรมการ โปรดติดตามความคืบหน้าอย่างต่อเนื่องครับ</p>"
                elif application.status == 'rejected':
                    content += "<p>ขอแสดงความเสียใจด้วยครับ คุณไม่ผ่านการพิจารณาสำหรับทุนการศึกษานี้ในครั้งนี้ ขอเป็นกำลังใจให้ในโอกาสหน้านะครับ</p>"
                elif application.status == 'cancelled':
                    content += "<p>ใบสมัครทุนการศึกษานี้ของคุณได้รับการยกเลิกแล้ว หากมีข้อสงสัยสามารถติดต่อหน่วยกิจการนักศึกษาได้ครับ</p>"
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
            fail_silently=True,
        )
