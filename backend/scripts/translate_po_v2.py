import re

po_path = "backend/locale/en/LC_MESSAGES/django.po"
with open(po_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Map of common Thai strings to English
translations = {
    # Navbar & Header
    "มหาวิทยาลัยสงขลานครินทร์ วิทยาเขตภูเก็ต": "Prince of Songkla University, Phuket Campus",
    "ระบบรับสมัครและติดตามทุนการศึกษา มหาวิทยาลัยสงขลานครินทร์ วิทยาเขตภูเก็ต": "Scholarship Application System, PSU Phuket",
    "ทุนการศึกษาที่ใช่": "The Right Scholarship",
    "เพื่ออนาคตที่ไกลกว่า ณ ม.อ. ภูเก็ต": "For a brighter future at PSU Phuket",
    "ศูนย์รวมข้อมูลทุนการศึกษาและสวัสดิการ สำหรับนักศึกษา ม.อ. ทุกคณะ สะดวก รวดเร็ว สมัครและติดตามผลแบบครบวงจรผ่านระบบออนไลน์": "Scholarship and welfare center for PSU students. Easy, fast, online.",
    "ดูทุนการศึกษาที่เปิดรับทั้งหมด": "View All Open Scholarships",
    
    # Categories
    "ทุนการศึกษาทั่วไป": "General Scholarships",
    "ทุนสนับสนุนการศึกษาสำหรับนักศึกษาทั่วไป ทุนขาดแคลนทุนทรัพย์": "Financial support for general students and those in need.",
    "ค้นหาทุนหมวดนี้": "Explore this category",
    "ทุนศึกษาแลกเปลี่ยน": "Exchange Scholarships",
    "ทุนสนับสนุนการแลกเปลี่ยนต่างประเทศและโครงการระดับนานาชาติ": "Support for international exchange and global programs.",
    "ทุนยกเว้นค่าธรรมเนียม": "Fee Waiver Scholarships",
    "ทุนยกเว้นค่าธรรมเนียมการศึกษาตามเกณฑ์ผลการเรียนและกิจกรรม": "Tuition fee waivers based on academic and extracurricular performance.",
    "ทุนอาหารกลางวัน": "Lunch Scholarships",
    "ทุนสวัสดิการอาหารกลางวันเพื่อสุขภาวะและการใช้ชีวิตในรั้วมหาวิทยาลัย": "Lunch welfare for student well-being on campus.",
    "ทุนเปิดรับ": "Open Scholarships",
    "ทุน": "Scholarships",
    
    # Other Dashboard & Common
    "สถานะ": "Status",
    "รอการพิจารณา": "Pending",
    "อนุมัติแล้ว": "Approved",
    "ไม่ผ่านการพิจารณา": "Rejected",
    "ยื่นสมัครแล้ว": "Applied",
    "เกรดไม่ถึง": "GPAX Unmet",
    "สมัครเลย": "Apply Now",
    "ดูรายละเอียด": "View Details",
    "แดชบอร์ดทุนการศึกษา": "Scholarship Dashboard",
    "จำนวนทุนทั้งหมด": "Total Scholarships",
    "มูลค่ารวม": "Total Value",
    "บาท": "THB",
    "เปิดรับสมัครอยู่": "Currently Open",
    "การสมัครทั้งหมด": "Total Applications",
    
    # Footer
    "หน้าแรก": "Home",
    "ติดต่อเรา": "Contact Us",
}

for thai, eng in translations.items():
    # If the msgid exists with empty or fuzzy msgstr
    # First remove fuzzy tag just in case
    pattern_fuzzy = rf'#, fuzzy\n(#\| msgid "{thai}"\n)?msgid "{thai}"'
    content = re.sub(pattern_fuzzy, f'msgid "{thai}"', content)
    
    pattern = rf'msgid "{thai}"\nmsgstr ".*?"'
    replacement = f'msgid "{thai}"\nmsgstr "{eng}"'
    content = re.sub(pattern, replacement, content)

with open(po_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("PO file updated.")
