import re

po_path = "backend/locale/en/LC_MESSAGES/django.po"
with open(po_path, 'r', encoding='utf-8') as f:
    content = f.read()

translations = {
    "หมวดหมู่ทุนการศึกษา": "Scholarship Categories",
    "เลือกประเภททุนที่ตรงกับเกณฑ์และเป้าหมายของคุณ": "Choose the scholarship type that fits your goals and criteria",
    "ทุนเปิดรับ": "Open Scholarships",
    "ค้นหาทุนหมวดนี้": "Explore this category",
    "ทุนที่ใกล้หมดเขต": "Expiring Soon",
    "รีบตรวจสอบคุณสมบัติและส่งใบสมัครก่อนหมดเขต": "Check your eligibility and apply before the deadline",
    "ด่วน! หมดเขต": "Urgent! Deadline",
}

for thai, eng in translations.items():
    pattern_fuzzy = rf'#, fuzzy\n(#\| msgid "{thai}"\n)?msgid "{thai}"'
    content = re.sub(pattern_fuzzy, f'msgid "{thai}"', content)
    
    pattern = rf'msgid "{thai}"\nmsgstr ".*?"'
    replacement = f'msgid "{thai}"\nmsgstr "{eng}"'
    content = re.sub(pattern, replacement, content)

with open(po_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("PO file updated.")
