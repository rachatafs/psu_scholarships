import os
import sys
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from scholarships.models import Scholarship
from django.utils import timezone

today = timezone.now().date()

scholarships_data = [
    {
        'title': 'ทุนเรียนดีประจำเดือนกันยายน (พิเศษ)',
        'description': 'ทุนส่งเสริมการศึกษาสำหรับนักศึกษาที่มีผลการเรียนดีเยี่ยมและต้องการทุนสนับสนุนแบบเร่งด่วนในเดือนกันยายนนี้ เพื่อช่วยบรรเทาภาระค่าใช้จ่าย',
        'requirements': '1. เป็นนักศึกษาปริญญาตรี\n2. GPAX 3.50 ขึ้นไป\n3. มีความประพฤติดี',
        'amount_per_semester': 20000.00,
        'capacity': 10,
        'category': 'general',
        'status': 'active',
        'start_date': today - timedelta(days=15),
        'end_date': today + timedelta(days=2),
    },
    {
        'title': 'ทุนฉุกเฉินช่วยเหลือนักศึกษา',
        'description': 'ทุนสำหรับนักศึกษาที่ประสบปัญหาทางการเงินฉุกเฉิน ต้องการความช่วยเหลือเร่งด่วน เปิดรับสมัครถึงสิ้นเดือนนี้เท่านั้น',
        'requirements': '1. เป็นนักศึกษาปริญญาตรี\n2. ประสบปัญหาทางการเงินกะทันหัน',
        'amount_per_semester': 10000.00,
        'capacity': 20,
        'category': 'lunch',
        'status': 'active',
        'start_date': today - timedelta(days=5),
        'end_date': today + timedelta(days=4),
    },
    {
        'title': 'ทุนกิจกรรมดีเด่น (รอบเก็บตก)',
        'description': 'ทุนสนับสนุนนักศึกษาที่สร้างชื่อเสียงให้มหาวิทยาลัย ด้านกีฬา ศิลปวัฒนธรรม หรือวิชาการ รอบพิเศษ',
        'requirements': '1. มีผลงานระดับชาติหรือนานาชาติ\n2. เกรดเฉลี่ยไม่ต่ำกว่า 2.50',
        'amount_per_semester': 15000.00,
        'capacity': 5,
        'category': 'fee_waiver',
        'status': 'active',
        'start_date': today - timedelta(days=20),
        'end_date': today + timedelta(days=5),
    }
]

for data in scholarships_data:
    Scholarship.objects.create(**data)

print(f"Seeded {len(scholarships_data)} scholarships expiring this month.")
