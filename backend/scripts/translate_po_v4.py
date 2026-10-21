import re

po_path = "backend/locale/en/LC_MESSAGES/django.po"
with open(po_path, 'r', encoding='utf-8') as f:
    content = f.read()

translations = {
    "ทุนการศึกษาทั่วไป": "General Scholarships",
    "ทุนสนับสนุนการศึกษาสำหรับนักศึกษาทั่วไป ทุนขาดแคลนทุนทรัพย์": "Financial support for general students and those in need.",
    "ทุนศึกษาแลกเปลี่ยน": "Exchange Scholarships",
    "ทุนสนับสนุนการแลกเปลี่ยนต่างประเทศและโครงการระดับนานาชาติ": "Support for international exchange and global programs.",
    "ทุนยกเว้นค่าธรรมเนียม": "Fee Waiver Scholarships",
    "ทุนยกเว้นค่าธรรมเนียมการศึกษาตามเกณฑ์ผลการเรียนและกิจกรรม": "Tuition fee waivers based on academic and extracurricular performance.",
    "ทุนอาหารกลางวัน": "Lunch Scholarships",
    "ทุนสวัสดิการอาหารกลางวันเพื่อสุขภาวะและการใช้ชีวิตในรั้วมหาวิทยาลัย": "Lunch welfare for student well-being on campus.",
    "ดูทุนการศึกษาที่เปิดรับทั้งหมด": "View All Open Scholarships",
}

for thai, eng in translations.items():
    pattern = rf'^msgid "{re.escape(thai)}"\nmsgstr ".*?"'
    replacement = f'msgid "{thai}"\nmsgstr "{eng}"'
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

with open(po_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed translations.")
