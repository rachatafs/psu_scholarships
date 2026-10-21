import re
import os

po_path = "backend/locale/en/LC_MESSAGES/django.po"
with open(po_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove fuzzy flags
content = re.sub(r'^#, fuzzy\n(#\| msgid ".*"\n)?', '', content, flags=re.MULTILINE)

# Map of common Thai strings to English
translations = {
    "หน้าแรก": "Home",
    "ทุนการศึกษา": "Scholarships",
    "ข้อมูลทุน": "Scholarship Info",
    "ทุนทั่วไป": "General",
    "ทุนแลกเปลี่ยน": "Exchange",
    "ทุนยกเว้นค่าธรรมเนียม": "Fee Waiver",
    "ทุนอาหารกลางวัน": "Lunch",
    "ติดต่อเรา": "Contact Us",
    "แดชบอร์ดสถิติ": "Analytics",
    "จัดการระบบ": "Admin Panel",
    "ข้อมูลส่วนตัว": "Profile",
    "ทุนที่บันทึกไว้": "Favorites",
    "ออกจากระบบ": "Logout",
    "ลงชื่อเข้าใช้": "Login",
    "เข้าสู่ระบบ": "Login",
    "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง": "Invalid username or password",
    "ค้นหาทุนการศึกษา...": "Search scholarships...",
    "ค้นหา": "Search",
    "ระบบรับสมัครและติดตามทุนการศึกษา มหาวิทยาลัยสงขลานครินทร์ วิทยาเขตภูเก็ต": "Scholarship Application System, PSU Phuket",
    "ทุนการศึกษาที่ใช่": "The Right Scholarship",
    "เพื่ออนาคตที่ไกลกว่า ณ ม.อ. ภูเก็ต": "For a brighter future at PSU Phuket",
    "ศูนย์รวมข้อมูลทุนการศึกษาและสวัสดิการ สำหรับนักศึกษา ม.อ. ทุกคณะ สะดวก รวดเร็ว สมัครและติดตามผลแบบครบวงจรผ่านระบบออนไลน์": "Scholarship and welfare center for PSU students. Easy, fast, online.",
    "ดูทุนการศึกษาที่เปิดรับทั้งหมด": "View All Open Scholarships",
}

for thai, eng in translations.items():
    # Find msgid "thai" and replace the following msgstr "" with msgstr "eng"
    pattern = rf'msgid "{thai}"\nmsgstr ""'
    replacement = f'msgid "{thai}"\nmsgstr "{eng}"'
    content = re.sub(pattern, replacement, content)
    
    # Also handle if msgstr already has something but we want to ensure it's translated
    pattern2 = rf'msgid "{thai}"\nmsgstr ".*"'
    content = re.sub(pattern2, replacement, content)

with open(po_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("PO file updated.")
