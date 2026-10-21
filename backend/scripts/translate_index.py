import re

with open("frontend/templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    "หมวดหมู่ทุนการศึกษา": "{% trans 'หมวดหมู่ทุนการศึกษา' %}",
    "เลือกประเภททุนที่ตรงกับเกณฑ์และเป้าหมายของคุณ": "{% trans 'เลือกประเภททุนที่ตรงกับเกณฑ์และเป้าหมายของคุณ' %}",
    "ทุนเปิดรับ": "{% trans 'ทุนเปิดรับ' %}",
    "ค้นหาทุนหมวดนี้": "{% trans 'ค้นหาทุนหมวดนี้' %}",
    "ทุนที่ใกล้หมดเขต": "{% trans 'ทุนที่ใกล้หมดเขต' %}",
    "รีบตรวจสอบคุณสมบัติและส่งใบสมัครก่อนหมดเขต": "{% trans 'รีบตรวจสอบคุณสมบัติและส่งใบสมัครก่อนหมดเขต' %}",
    "ด่วน! หมดเขต": "{% trans 'ด่วน! หมดเขต' %}",
}

for thai, eng in replacements.items():
    # Only replace if not already wrapped
    content = re.sub(rf'(?<!{{% trans \'){thai}(?!\' %}})', eng, content)

with open("frontend/templates/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html")
