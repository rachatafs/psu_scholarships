import os
import sys
import random
from datetime import date, datetime, timedelta

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from scholarships.models import StudentProfile, Scholarship, Application, Document, FavoriteScholarship


def seed_data():
    print("🌱 Starting Comprehensive Database Seeding...")

    # 1. Get or create Admin user
    admin_user, _ = User.objects.get_or_create(
        username='rachata',
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'rachata@phuket.psu.ac.th'}
    )
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()

    # 2. Student User Definitions
    students_info = [
        {
            'username': 's6630613014',
            'full_name': 'รชต ไผ่สังข์ (Rachata Faisang)',
            'student_id': '6630613014',
            'faculty': 'computing',
            'major': 'Digital Engineering (DE)',
            'phone_number': '080-717-2609',
            'gpax': 3.65,
        },
        {
            'username': 's6630613001',
            'full_name': 'นายชลน่าน ภูเก็ตดี',
            'student_id': '6630613001',
            'faculty': 'computing',
            'major': 'Computer Science (CS)',
            'phone_number': '081-234-5678',
            'gpax': 3.85,
        },
        {
            'username': 's6630613002',
            'full_name': 'นางสาวสุพิชชา อันดามัน',
            'student_id': '6630613002',
            'faculty': 'management',
            'major': 'Hospitality Management (HPM)',
            'phone_number': '082-345-6789',
            'gpax': 3.42,
        },
        {
            'username': 's6630613003',
            'full_name': 'นายปรมินทร์ วงศ์สุวรรณ',
            'student_id': '6630613003',
            'faculty': 'engineering',
            'major': 'Computer Engineering (CPE)',
            'phone_number': '083-456-7890',
            'gpax': 2.85,
        },
        {
            'username': 's6630613004',
            'full_name': 'นางสาวกานต์พิชชา รัตนากร',
            'student_id': '6630613004',
            'faculty': 'computing',
            'major': 'Information Technology (IT)',
            'phone_number': '084-567-8901',
            'gpax': 3.92,
        },
        {
            'username': 's6630613005',
            'full_name': 'นายณัฐภัทร ศรีวิชัย',
            'student_id': '6630613005',
            'faculty': 'science',
            'major': 'Technology and Environment (TE)',
            'phone_number': '085-678-9012',
            'gpax': 2.45,
        },
        {
            'username': 's6630613006',
            'full_name': 'นางสาวปรียาภรณ์ ทองดี',
            'student_id': '6630613006',
            'faculty': 'management',
            'major': 'Tourism Management (TRM)',
            'phone_number': '086-789-0123',
            'gpax': 3.10,
        },
        {
            'username': 's6630613007',
            'full_name': 'นายวรเมธ เกียรติไพบูลย์',
            'student_id': '6630613007',
            'faculty': 'other',
            'major': 'International Studies (FIS)',
            'phone_number': '087-890-1234',
            'gpax': 3.55,
        },
        {
            'username': 's6630613008',
            'full_name': 'นางสาวชิดชนก วงศ์ประเสริฐ',
            'student_id': '6630613008',
            'faculty': 'computing',
            'major': 'Electronic Business (EB)',
            'phone_number': '088-901-2345',
            'gpax': 2.60,
        },
        {
            'username': 's6630613009',
            'full_name': 'นายธนกฤต ชัยมงคล',
            'student_id': '6630613009',
            'faculty': 'engineering',
            'major': 'Environmental Engineering',
            'phone_number': '089-012-3456',
            'gpax': 3.20,
        },
        {
            'username': 's6630613010',
            'full_name': 'นางสาวอภิญญา วัฒนศิลป์',
            'student_id': '6630613010',
            'faculty': 'other',
            'major': 'Chinese Studies (Chinese)',
            'phone_number': '080-123-4567',
            'gpax': 3.78,
        },
        {
            'username': 's6630613011',
            'full_name': 'นายภานุพงศ์ บุญประเสริฐ',
            'student_id': '6630613011',
            'faculty': 'computing',
            'major': 'Software Engineering',
            'phone_number': '081-345-6789',
            'gpax': 2.30,
        },
        {
            'username': 's6630613012',
            'full_name': 'นางสาวมนัสวี โรจนะสิริ',
            'student_id': '6630613012',
            'faculty': 'management',
            'major': 'Service Industry and Event Management',
            'phone_number': '082-456-7890',
            'gpax': 3.48,
        },
        {
            'username': 's6630613013',
            'full_name': 'นายสิทธิชัย เมธาวี',
            'student_id': '6630613013',
            'faculty': 'science',
            'major': 'Environmental Technology',
            'phone_number': '083-567-8901',
            'gpax': 3.05,
        },
    ]

    # Clean up any orphaned users without profile if they collide from previous runs
    User.objects.filter(username__in=[s['username'] for s in students_info], profile__isnull=True).delete()

    profiles = []
    for info in students_info:
        # Check if profile already exists by student_id
        profile = StudentProfile.objects.filter(student_id=info['student_id']).first()
        if profile:
            user = profile.user
        else:
            user, _ = User.objects.get_or_create(
                username=info['username'],
                defaults={'email': f"{info['username']}@phuket.psu.ac.th"}
            )
            profile, _ = StudentProfile.objects.get_or_create(
                user=user,
                defaults={'student_id': info['student_id']}
            )

        user.set_password('psu12345')
        user.save()

        profile.student_id = info['student_id']
        profile.full_name = info['full_name']
        profile.faculty = info['faculty']
        profile.major = info['major']
        profile.phone_number = info['phone_number']
        profile.gpax = info['gpax']
        profile.save()
        profiles.append(profile)

    print(f"✅ Created/Updated {len(profiles)} Student Profiles.")

    # 3. Scholarships Data (Covering all 4 categories & 3 statuses)
    today = timezone.now().date()
    scholarships_specs = [
        # --- General Scholarships (general) ---
        {
            'title': 'ทุนเรียนดีเด่น มหาวิทยาลัยสงขลานครินทร์ วิทยาเขตภูเก็ต ประจำปีการศึกษา 2567',
            'category': 'general',
            'description': 'ทุนส่งเสริมและเชิดชูเกียรตินักศึกษาที่มีผลการเรียนยอดเยี่ยม มีความประพฤติเรียบร้อย และสร้างชื่อเสียงทางวิชาการให้แก่มหาวิทยาลัย',
            'requirements': '1. เป็นนักศึกษาระดับปริญญาตรีทุกคณะ\n2. มีผลการเรียนสะสม (GPAX) ตั้งแต่ 3.50 ขึ้นไป\n3. ไม่เคยได้รับโทษทางวินัยนักศึกษา',
            'amount_per_semester': 35000.00,
            'capacity': 10,
            'start_date': today - timedelta(days=60),
            'end_date': today + timedelta(days=30),
            'status': 'active',
        },
        {
            'title': 'ทุนพัฒนาศักยภาพทางวิชาการและนวัตกรรมดิจิทัล (Digital Innovation Grant)',
            'category': 'general',
            'description': 'ทุนสนับสนุนนักศึกษาที่มีความสนใจและผลงานด้านการพัฒนานวัตกรรม เทคโนโลยี และการเขียนโปรแกรมเชิงประยุกต์',
            'requirements': '1. นักศึกษาคณะวิทยาการคำนวณ หรือสาขาที่เกี่ยวข้อง\n2. GPAX ไม่ต่ำกว่า 3.00\n3. มีแฟ้มสะสมผลงาน (Portfolio) ด้านนวัตกรรมหรือซอฟต์แวร์',
            'amount_per_semester': 25000.00,
            'capacity': 15,
            'start_date': today - timedelta(days=45),
            'end_date': today + timedelta(days=20),
            'status': 'active',
        },
        {
            'title': 'ทุนอุดหนุนการศึกษาเพื่อนักศึกษาเรียนดีแต่ขาดแคลนทุนทรัพย์ (รอบทั่วไป)',
            'category': 'general',
            'description': 'ทุนให้เปล่าเพื่อช่วยเหลือนักศึกษาที่มีความตั้งใจในการศึกษาเล่าเรียนแต่ครอบครัวมีรายได้น้อยหรือประสบวิกฤตเศรษฐกิจ',
            'requirements': '1. นักศึกษาปริญญาตรีชั้นปีที่ 1-4\n2. GPAX ไม่ต่ำกว่า 2.50\n3. หนังสือรับรองรายได้ครอบครัวและรูปถ่ายบ้านพักอาศัย',
            'amount_per_semester': 20000.00,
            'capacity': 25,
            'start_date': today - timedelta(days=30),
            'end_date': today + timedelta(days=40),
            'status': 'active',
        },
        {
            'title': 'ทุนศิษย์เก่า ม.อ. ภูเก็ต ร่วมใจสร้างอนาคต (รอบเปิดภาคการศึกษา)',
            'category': 'general',
            'description': 'ทุนการศึกษาจากสมาคมศิษย์เก่า มหาวิทยาลัยสงขลานครินทร์ วิทยาเขตภูเก็ต เพื่อมอบให้แก่นักศึกษารุ่นน้อง',
            'requirements': '1. นักศึกษาปริญญาตรีที่มีความประพฤติดี\n2. GPAX 2.50 ขึ้นไป',
            'amount_per_semester': 15000.00,
            'capacity': 8,
            'start_date': today - timedelta(days=120),
            'end_date': today - timedelta(days=10),
            'status': 'closed',
        },
        {
            'title': 'ทุนวิจัยและปัญญาประดิษฐ์ระดับปริญญาตรี (AI & Data Science Excellence) 2568',
            'category': 'general',
            'description': 'ทุนสนับสนุนการทำวิจัยและโครงงานพิเศษด้าน Generative AI, Data Science และ Machine Learning สำหรับภาคการศึกษาหน้า',
            'requirements': '1. นักศึกษาชั้นปีที่ 3-4\n2. GPAX ไม่ต่ำกว่า 3.25\n3. ข้อเสนอโครงการวิจัย (Proposal)',
            'amount_per_semester': 40000.00,
            'capacity': 5,
            'start_date': today + timedelta(days=15),
            'end_date': today + timedelta(days=90),
            'status': 'draft',
        },

        # --- Exchange Scholarships (exchange) ---
        {
            'title': 'ทุนแลกเปลี่ยนนักศึกษานานาชาติ ณ มหาวิทยาลัยคิวชู (Kyushu University, Japan)',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนค่าตั๋วเครื่องบินและค่าครองชีพสำหรับการศึกษาแลกเปลี่ยน 1 ภาคการศึกษา ณ ประเทศญี่ปุ่น',
            'requirements': '1. นักศึกษาชั้นปีที่ 2 ขึ้นไป\n2. GPAX ไม่ต่ำกว่า 3.25\n3. คะแนนภาษาอังกฤษ TOEIC 650+ หรือ IELTS 6.0+',
            'amount_per_semester': 85000.00,
            'capacity': 4,
            'start_date': today - timedelta(days=40),
            'end_date': today + timedelta(days=15),
            'status': 'active',
        },
        {
            'title': 'ทุนสหกิจศึกษานานาชาติและฝึกงานด้านเทคโนโลยี ณ ประเทศสิงคโปร์ (Tech Internship)',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนค่าใช้จ่ายสำหรับนักศึกษาที่ได้รับตอบรับเข้าฝึกงานในบริษัทเทคโนโลยีชั้นนำ ณ ประเทศสิงคโปร์',
            'requirements': '1. นักศึกษาชั้นปีที่ 3 หรือ 4\n2. GPAX ไม่ต่ำกว่า 3.00\n3. หนังสือตอบรับการฝึกงานจากบริษัทปลายทาง',
            'amount_per_semester': 60000.00,
            'capacity': 6,
            'start_date': today - timedelta(days=20),
            'end_date': today + timedelta(days=35),
            'status': 'active',
        },
        {
            'title': 'ทุนแลกเปลี่ยนภาษาและวัฒนธรรมยุโรป (Erasmus+ Mobility Programme)',
            'category': 'exchange',
            'description': 'โครงการแลกเปลี่ยนนักศึกษาระหว่าง ม.อ. ภูเก็ต กับสถาบันคู่สัญญาในสหภาพยุโรป',
            'requirements': '1. GPAX 3.50 ขึ้นไป\n2. มีผลสอบภาษาอังกฤษ IELTS 6.5 ขึ้นไป\n3. ผ่านการสัมภาษณ์จากคณะกรรมการนานาชาติ',
            'amount_per_semester': 110000.00,
            'capacity': 2,
            'start_date': today - timedelta(days=90),
            'end_date': today - timedelta(days=5),
            'status': 'closed',
        },
        {
            'title': 'ทุนแลกเปลี่ยนนักศึกษาอาเซียน AIMS Programme (Malaysia & Indonesia)',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนการแลกเปลี่ยนนักศึกษาภายใต้กรอบความร่วมมือกลุ่มประเทศอาเซียน',
            'requirements': '1. นักศึกษาชั้นปีที่ 2-3\n2. GPAX 2.80 ขึ้นไป\n3. มีความพร้อมในการปรับตัวเข้ากับสิ่งแวดล้อมพหุวัฒนธรรม',
            'amount_per_semester': 45000.00,
            'capacity': 6,
            'start_date': today + timedelta(days=10),
            'end_date': today + timedelta(days=60),
            'status': 'draft',
        },

        # --- Fee Waiver Scholarships (fee_waiver) ---
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษา 100% สำหรับผู้นำนักศึกษาและนักกิจกรรมดีเด่น',
            'category': 'fee_waiver',
            'description': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาเต็มจำนวน (100%) เพื่อเป็นขวัญกำลังใจแก่ผู้บำเพ็ญประโยชน์ต่อส่วนรวม สโมสรนักศึกษา และสภานักศึกษา',
            'requirements': '1. เป็นกรรมการสโมสรนักศึกษา/สภานักศึกษา หรือผู้นำชมรม\n2. GPAX ไม่ต่ำกว่า 2.50\n3. ผ่านการรับรองจากกองกิจการนักศึกษา',
            'amount_per_semester': 32000.00,
            'capacity': 10,
            'start_date': today - timedelta(days=50),
            'end_date': today + timedelta(days=25),
            'status': 'active',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษา 50% สำหรับนักกีฬาตัวแทนมหาวิทยาลัย',
            'category': 'fee_waiver',
            'description': 'ทุนยกเว้นค่าเล่าเรียนครึ่งจำนวน (50%) สำหรับนักกีฬาที่สร้างชื่อเสียงในการแข่งขันกีฬามหาวิทยาลัยแห่งประเทศไทย',
            'requirements': '1. เป็นนักกีฬาตัวแทน ม.อ. หรือระดับเยาวชนทีมชาติ\n2. GPAX ไม่ต่ำกว่า 2.20\n3. มีหนังสือรับรองจากศูนย์กีฬา',
            'amount_per_semester': 16000.00,
            'capacity': 12,
            'start_date': today - timedelta(days=35),
            'end_date': today + timedelta(days=40),
            'status': 'active',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาสำหรับผู้มีความสามารถพิเศษด้านศิลปวัฒนธรรมและดนตรี',
            'category': 'fee_waiver',
            'description': 'ทุนส่งเสริมผู้มีความสามารถโดดเด่นด้านนาฏศิลป์ ดนตรีสากล ดนตรีไทย หรือศิลปะร่วมสมัย',
            'requirements': '1. มีประวัติผลงานการแสดงหรือประกวดระดับจังหวัดขึ้นไป\n2. GPAX ไม่ต่ำกว่า 2.50',
            'amount_per_semester': 16000.00,
            'capacity': 6,
            'start_date': today - timedelta(days=70),
            'end_date': today - timedelta(days=2),
            'status': 'closed',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาประเภทพิเศษ ภาคการศึกษา 2/2567',
            'category': 'fee_waiver',
            'description': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาเต็มจำนวน สำหรับผู้ผ่านการคัดเลือกเป็นติวเตอร์วิชาการของมหาวิทยาลัย',
            'requirements': '1. GPAX 3.50 ขึ้นไป\n2. ผ่านการทดสอบคัดเลือกติวเตอร์ประจำศูนย์การเรียนรู้',
            'amount_per_semester': 32000.00,
            'capacity': 8,
            'start_date': today + timedelta(days=20),
            'end_date': today + timedelta(days=75),
            'status': 'draft',
        },

        # --- Lunch Scholarships (lunch) ---
        {
            'title': 'ทุนอาหารกลางวันเพื่อน้อง ม.อ. ภูเก็ต ประจำภาคการศึกษาที่ 1/2567',
            'category': 'lunch',
            'description': 'ทุนคูปองอาหารมูลค่าวันละ 100 บาท เพื่อสวัสดิการอาหารกลางวันและลดค่าใช้จ่ายประจำวันของนักศึกษา',
            'requirements': '1. นักศึกษาปริญญาตรีทุกชั้นปี\n2. มีความเดือดร้อนด้านค่าครองชีพ\n3. GPAX ไม่ต่ำกว่า 2.00',
            'amount_per_semester': 7500.00,
            'capacity': 35,
            'start_date': today - timedelta(days=60),
            'end_date': today + timedelta(days=30),
            'status': 'active',
        },
        {
            'title': 'ทุนสนับสนุนค่าครองชีพและอาหารกลางวันสำหรับนักศึกษาหอพักในมหาวิทยาลัย',
            'category': 'lunch',
            'description': 'ทุนช่วยเหลืออาหารและของใช้อุปโภคบริโภคจำเป็นสำหรับนักศึกษาที่พักอาศัยในหอพัก ม.อ. ภูเก็ต',
            'requirements': '1. เป็นผู้พักอาศัยในหอพักนักศึกษา ม.อ. ภูเก็ต\n2. GPAX 2.00 ขึ้นไป\n3. มีหนังสือรับรองจากอาจารย์ที่ปรึกษา',
            'amount_per_semester': 6000.00,
            'capacity': 25,
            'start_date': today - timedelta(days=30),
            'end_date': today + timedelta(days=45),
            'status': 'active',
        },
        {
            'title': 'ทุนอาหารกลางวันฉุกเฉินสู้ภัยเศรษฐกิจ (รอบช่วยเหลือเร่งด่วน)',
            'category': 'lunch',
            'description': 'ทุนสวัสดิการอาหารแบบเร่งด่วนพิจารณาผลภายใน 3 วันทำการ เพื่อช่วยเหลือนักศึกษาที่ประสบปัญหาเฉียบพลัน',
            'requirements': '1. นักศึกษาที่มีความจำเป็นเร่งด่วนด้านค่าอาหาร\n2. ไม่จำกัดเกรดเฉลี่ยขั้นต่ำ',
            'amount_per_semester': 5000.00,
            'capacity': 20,
            'start_date': today - timedelta(days=80),
            'end_date': today - timedelta(days=15),
            'status': 'closed',
        },
        {
            'title': 'ทุนคูปองอาหารกลางวันและโภชนาการนักศึกษา ภาคการศึกษา 2/2567',
            'category': 'lunch',
            'description': 'ทุนจัดสรรคูปองอาหารประจำโรงอาหารกลาง ม.อ. ภูเก็ต สำหรับภาคการศึกษาถัดไป',
            'requirements': '1. นักศึกษาปริญญาตรีทุกคณะ\n2. GPAX ไม่ต่ำกว่า 2.00',
            'amount_per_semester': 8000.00,
            'capacity': 40,
            'start_date': today + timedelta(days=25),
            'end_date': today + timedelta(days=80),
            'status': 'draft',
        },
    ]

    scholarships = []
    for spec in scholarships_specs:
        s, _ = Scholarship.objects.update_or_create(
            title=spec['title'],
            defaults={
                'category': spec['category'],
                'description': spec['description'],
                'requirements': spec['requirements'],
                'amount_per_semester': spec['amount_per_semester'],
                'capacity': spec['capacity'],
                'start_date': spec['start_date'],
                'end_date': spec['end_date'],
                'status': spec['status'],
                'created_by': admin_user,
            }
        )
        scholarships.append(s)

    print(f"✅ Created/Updated {len(scholarships)} Scholarships (all categories & statuses).")

    # 4. Applications Data (Covering ALL 7 statuses: pending, in_progress, interview, approved, rejected, completed, cancelled)
    all_statuses = ['pending', 'in_progress', 'interview', 'approved', 'rejected', 'completed', 'cancelled']
    status_notes = {
        'pending': 'ใบสมัครเข้าสู่ระบบเรียบร้อย รอเจ้าหน้าที่ตรวจความถูกต้องของเอกสารแนบ',
        'in_progress': 'เอกสารถูกต้องตามเกณฑ์ขั้นต้น กำลังอยู่ระหว่างการประเมินของคณะกรรมการทุนการศึกษา',
        'interview': 'ผ่านการคัดเลือกเบื้องต้น นัดหมายสัมภาษณ์ออนไลน์ผ่าน Zoom ในวันที่ 18 พ.ย. เวลา 10:00 น.',
        'approved': 'คณะกรรมการมีมติอนุมัติทุนการศึกษา กรุณารายงานตัวและยืนยันสิทธิ์ตามกำหนดเวลา',
        'rejected': 'เกรดเฉลี่ยสะสมหรือคุณสมบัติไม่ตรงตามประกาศรับสมัคร หรือโควตาทุนของรอบนี้ได้รับการจัดสรรเต็มแล้ว',
        'completed': 'โอนเงินทุนการศึกษาเข้าบัญชีพร้อมเพย์นักศึกษาเรียบร้อยแล้ว หรือตัดลดหย่อนค่าเทอมสำเร็จ',
        'cancelled': 'นักศึกษายกเลิกคำขอ หรือสละสิทธิ์เนื่องจากได้รับทุนการศึกษาอื่นซ้ำซ้อน',
    }

    # Available sample documents
    doc_dir = 'documents/'
    doc_files = [
        'Certificate.pdf',
        'Rubric_-_Sheet1.pdf',
        'SIS-Grade_Report_6630613014_EN.pdf',
        'Template_Report_DE_Project2_v3.pdf',
    ]

    active_scholarships = [s for s in scholarships if s.status in ['active', 'closed']]
    app_count = 0

    # Ensure Rachata's student account (s6630613014) has applications across multiple statuses to test personal profile view
    rachata_profile = next((p for p in profiles if p.student_id == '6630613014'), profiles[0])
    n_act = len(active_scholarships)
    rachata_apps_data = [
        (active_scholarships[0 % n_act], 'approved', 'อนุมัติทุนเรียบร้อย ผลการเรียนโดดเด่น GPAX 3.65'),
        (active_scholarships[1 % n_act], 'in_progress', 'อยู่ระหว่างการสัมภาษณ์รอบสุดท้าย'),
        (active_scholarships[3 % n_act], 'interview', 'กำหนดการสัมภาษณ์ทุนญี่ปุ่น วันศุกร์ที่ 21 พ.ย.'),
        (active_scholarships[4 % n_act], 'completed', 'เบิกจ่ายทุนค่าธรรมเนียมการศึกษาเรียบร้อยแล้ว'),
        (active_scholarships[6 % n_act], 'pending', 'ส่งใบสมัครแล้ว รอกรรมการตรวจสอบเอกสาร'),
    ]

    for sch, st, note in rachata_apps_data:
        app, created = Application.objects.update_or_create(
            student=rachata_profile,
            scholarship=sch,
            defaults={'status': st, 'note': note}
        )
        if created or not app.documents.exists():
            for doc_type in ['transcript', 'recommendation']:
                chosen_file = random.choice(doc_files)
                Document.objects.create(
                    application=app,
                    doc_type=doc_type,
                    file=f"{doc_dir}{chosen_file}"
                )
        app_count += 1

    # Also seed applications for admin user's profile (rachata) if present
    admin_profile = getattr(admin_user, 'profile', None)
    if admin_profile and admin_profile != rachata_profile:
        admin_apps_data = [
            (active_scholarships[2 % n_act], 'approved', 'อนุมัติทุนการศึกษาเรียบร้อย'),
            (active_scholarships[5 % n_act], 'in_progress', 'เอกสารถูกต้องตามเกณฑ์ขั้นต้น กำลังประเมิน'),
            (active_scholarships[7 % n_act], 'interview', 'นัดสัมภาษณ์ทุนสิงคโปร์ วันพุธที่ 19 พ.ย.'),
            (active_scholarships[8 % n_act], 'rejected', 'ไม่ผ่านเกณฑ์คุณสมบัติด้านรายได้'),
            (active_scholarships[10 % n_act], 'completed', 'โอนเงินทุนเข้าบัญชีเรียบร้อย'),
        ]
        for sch, st, note in admin_apps_data:
            app, created = Application.objects.update_or_create(
                student=admin_profile,
                scholarship=sch,
                defaults={'status': st, 'note': note}
            )
            if created or not app.documents.exists():
                for doc_type in ['transcript', 'recommendation']:
                    chosen_file = random.choice(doc_files)
                    Document.objects.create(
                        application=app,
                        doc_type=doc_type,
                        file=f"{doc_dir}{chosen_file}"
                    )
            app_count += 1

    # Distribute applications for other students to guarantee ALL 7 statuses are richly populated
    status_index = 0
    for profile in profiles:
        if profile == rachata_profile:
            continue

        # Choose 2-4 scholarships per student
        num_apps = random.randint(2, 4)
        chosen_scholarships = random.sample(active_scholarships, min(num_apps, len(active_scholarships)))

        for sch in chosen_scholarships:
            assigned_status = all_statuses[status_index % len(all_statuses)]
            status_index += 1

            app, created = Application.objects.update_or_create(
                student=profile,
                scholarship=sch,
                defaults={
                    'status': assigned_status,
                    'note': status_notes[assigned_status]
                }
            )

            # Create sample documents if none
            if created or not app.documents.exists():
                for doc_type in ['transcript', 'recommendation']:
                    chosen_file = random.choice(doc_files)
                    Document.objects.create(
                        application=app,
                        doc_type=doc_type,
                        file=f"{doc_dir}{chosen_file}"
                    )
            app_count += 1

    print(f"✅ Created/Updated {app_count} Applications covering all 7 statuses.")

    # 5. Seed Favorite Scholarships
    fav_count = 0
    for profile in profiles[:6]:
        fav_schs = random.sample(active_scholarships, 3)
        for f_sch in fav_schs:
            FavoriteScholarship.objects.get_or_create(
                user=profile.user,
                scholarship=f_sch
            )
            fav_count += 1

    # Also favorite for admin rachata user
    for f_sch in active_scholarships[:4]:
        FavoriteScholarship.objects.get_or_create(
            user=admin_user,
            scholarship=f_sch
        )
        fav_count += 1

    print(f"✅ Seeded {fav_count} Favorites.")

    # Summary Output
    print("\n================ DATABASE SEEDING SUMMARY ================")
    print(f"Scholarships Total:  {Scholarship.objects.count()}")
    for cat, name in Scholarship.CATEGORY_CHOICES:
        print(f"  • Category '{cat}': {Scholarship.objects.filter(category=cat).count()}")
    for st, name in Scholarship.STATUS_CHOICES:
        print(f"  • Status '{st}': {Scholarship.objects.filter(status=st).count()}")

    print(f"\nApplications Total:  {Application.objects.count()}")
    for st, name in Application.STATUS_CHOICES:
        print(f"  • Status '{st}': {Application.objects.filter(status=st).count()}")

    print(f"\nStudent Profiles:    {StudentProfile.objects.count()}")
    print(f"Documents Attached:  {Document.objects.count()}")
    print(f"Favorites:           {FavoriteScholarship.objects.count()}")
    print("==========================================================")
    print("✨ Database Seeding Completed Successfully! ✨")


if __name__ == '__main__':
    seed_data()
