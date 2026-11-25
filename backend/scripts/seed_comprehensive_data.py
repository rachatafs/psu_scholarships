import os
import sys
import random
from datetime import timedelta

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
    admin_user.set_password('psu12345')
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

    # Merge/clean any Google OAuth hashed usernames (e.g. s6630613014db1ea...)
    for s_info in students_info:
        clean_uname = s_info['username']
        for hashed_u in User.objects.filter(username__startswith=clean_uname).exclude(username=clean_uname):
            clean_u = User.objects.filter(username=clean_uname).first()
            if clean_u:
                if hasattr(hashed_u, 'social_auth'):
                    hashed_u.social_auth.all().update(user=clean_u)
                if hasattr(hashed_u, 'profile') and hasattr(clean_u, 'profile'):
                    Application.objects.filter(student=hashed_u.profile).update(student=clean_u.profile)
                    hashed_u.profile.delete()
                FavoriteScholarship.objects.filter(user=hashed_u).update(user=clean_u)
                hashed_u.delete()
            else:
                hashed_u.username = clean_uname
                hashed_u.save()

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

    # 3. Scholarships Data (Covering all 4 categories & 3 statuses with comprehensive urgency levels)
    today = timezone.now().date()
    scholarships_specs = [
        # ==============================================================
        # --- General Scholarships (general) ---
        # ==============================================================
        {
            'title': 'ทุนอุดหนุนการศึกษากรณีฉุกเฉิน ม.อ. ภูเก็ต (รอบเร่งด่วนพิเศษ)',
            'title_en': 'PSU Phuket Emergency Student Relief Grant (Express Round)',
            'category': 'general',
            'description': 'ทุนสนับสนุนนักศึกษาที่ประสบเหตุการณ์ฉุกเฉินทางการเงิน หรือได้รับผลกระทบทางเศรษฐกิจเฉียบพลัน เพื่อให้สามารถศึกษาต่อได้อย่างต่อเนื่อง',
            'description_en': 'Emergency financial assistance for students facing unexpected urgent financial hardship to ensure uninterrupted studies.',
            'requirements': '1. นักศึกษาปริญญาตรี ม.อ. ภูเก็ต ทุกคณะและทุกชั้นปี\n2. ประสบเหตุเดือดร้อนทางการเงินเร่งด่วน\n3. มีหนังสือรับรองจากอาจารย์ที่ปรึกษา',
            'requirements_en': '1. Undergraduate students of all faculties\n2. Experiencing acute financial difficulty\n3. Endorsement letter from advisor',
            'amount_per_semester': 15000.00,
            'capacity': 10,
            'start_date': today - timedelta(days=20),
            'end_date': today + timedelta(days=2),
            'status': 'active',
        },
        {
            'title': 'ทุนสนับสนุนโครงงานวิจัยระดับปริญญาตรี คณะวิทยาการคำนวณ (Senior Project Grant)',
            'title_en': 'College of Computing Senior Research Project Grant',
            'category': 'general',
            'description': 'ทุนสนับสนุนการทำโครงงานวิจัยและพัฒนานวัตกรรมซอฟต์แวร์สำหรับนักศึกษาชั้นปีสุดท้าย คณะวิทยาการคำนวณ',
            'description_en': 'Research and development project grant for final-year students in College of Computing.',
            'requirements': '1. นักศึกษาชั้นปีที่ 4 คณะวิทยาการคำนวณ\n2. GPAX ไม่ต่ำกว่า 2.75\n3. ผ่านการเห็นชอบหัวข้อโครงงานจากอาจารย์ที่ปรึกษาโครงงาน',
            'requirements_en': '1. 4th year student in College of Computing\n2. GPAX >= 2.75\n3. Approved project proposal by project advisor',
            'amount_per_semester': 20000.00,
            'capacity': 12,
            'start_date': today - timedelta(days=30),
            'end_date': today + timedelta(days=5),
            'status': 'active',
        },
        {
            'title': 'ทุนพัฒนาทักษะวิชาชีพและภาษาต่างประเทศสำหรับนักศึกษา (PSU Global Skills)',
            'title_en': 'PSU Phuket Global Skills & Language Proficiency Grant',
            'category': 'general',
            'description': 'ทุนสนับสนุนการสอบวัดระดับภาษาอังกฤษสากล (TOEIC, IELTS) และการสอบใบรับรองวิชาชีพมาตรฐานระดับสากล',
            'description_en': 'Financial subsidy for standardized English examinations (TOEIC, IELTS) and international professional certifications.',
            'requirements': '1. นักศึกษาปริญญาตรีชั้นปีที่ 2-4\n2. GPAX ไม่ต่ำกว่า 2.50\n3. มีแผนการสอบใบรับรองหรือทดสอบภาษาภายในภาคการศึกษา',
            'requirements_en': '1. 2nd-4th year undergraduate students\n2. GPAX >= 2.50\n3. Concrete certification/exam plan within semester',
            'amount_per_semester': 18000.00,
            'capacity': 15,
            'start_date': today - timedelta(days=25),
            'end_date': today + timedelta(days=10),
            'status': 'active',
        },
        {
            'title': 'ทุนพัฒนาศักยภาพทางวิชาการและนวัตกรรมดิจิทัล (Digital Innovation Grant)',
            'title_en': 'Digital Innovation and Academic Excellence Grant',
            'category': 'general',
            'description': 'ทุนสนับสนุนนักศึกษาที่มีความสนใจและผลงานด้านการพัฒนานวัตกรรม เทคโนโลยี และการเขียนโปรแกรมเชิงประยุกต์',
            'description_en': 'Grant for students with high potential and innovative portfolio in digital technologies and software applications.',
            'requirements': '1. นักศึกษาคณะวิทยาการคำนวณ หรือสาขาที่เกี่ยวข้อง\n2. GPAX ไม่ต่ำกว่า 3.00\n3. มีแฟ้มสะสมผลงาน (Portfolio) ด้านนวัตกรรมหรือซอฟต์แวร์',
            'requirements_en': '1. College of Computing or related fields\n2. GPAX >= 3.00\n3. Portfolio of innovation or software projects',
            'amount_per_semester': 25000.00,
            'capacity': 15,
            'start_date': today - timedelta(days=45),
            'end_date': today + timedelta(days=18),
            'status': 'active',
        },
        {
            'title': 'ทุนเรียนดีเด่น มหาวิทยาลัยสงขลานครินทร์ วิทยาเขตภูเก็ต ประจำปีการศึกษา 2567',
            'title_en': 'PSU Phuket Academic Honors Scholarship 2024',
            'category': 'general',
            'description': 'ทุนส่งเสริมและเชิดชูเกียรตินักศึกษาที่มีผลการเรียนยอดเยี่ยม มีความประพฤติเรียบร้อย และสร้างชื่อเสียงทางวิชาการให้แก่มหาวิทยาลัย',
            'description_en': 'Honors scholarship recognizing students with outstanding academic achievements and exemplary conduct.',
            'requirements': '1. เป็นนักศึกษาระดับปริญญาตรีทุกคณะ\n2. มีผลการเรียนสะสม (GPAX) ตั้งแต่ 3.50 ขึ้นไป\n3. ไม่เคยได้รับโทษทางวินัยนักศึกษา',
            'requirements_en': '1. Undergraduate students of all faculties\n2. Cumulative GPAX >= 3.50\n3. Good disciplinary standing',
            'amount_per_semester': 35000.00,
            'capacity': 10,
            'start_date': today - timedelta(days=60),
            'end_date': today + timedelta(days=30),
            'status': 'active',
        },
        {
            'title': 'ทุนอุดหนุนการศึกษาเพื่อนักศึกษาเรียนดีแต่ขาดแคลนทุนทรัพย์ (รอบทั่วไป)',
            'title_en': 'Need-Based Undergraduate Education Support Grant',
            'category': 'general',
            'description': 'ทุนให้เปล่าเพื่อช่วยเหลือนักศึกษาที่มีความตั้งใจในการศึกษาเล่าเรียนแต่ครอบครัวมีรายได้น้อยหรือประสบวิกฤตเศรษฐกิจ',
            'description_en': 'Tuition and living stipend support for students with dedicated academic commitment and proven financial need.',
            'requirements': '1. นักศึกษาปริญญาตรีชั้นปีที่ 1-4\n2. GPAX ไม่ต่ำกว่า 2.50\n3. หนังสือรับรองรายได้ครอบครัวและรูปถ่ายบ้านพักอาศัย',
            'requirements_en': '1. 1st-4th year students\n2. GPAX >= 2.50\n3. Family income verification documents',
            'amount_per_semester': 20000.00,
            'capacity': 25,
            'start_date': today - timedelta(days=30),
            'end_date': today + timedelta(days=50),
            'status': 'active',
        },
        {
            'title': 'ทุนศิษย์เก่า ม.อ. ภูเก็ต ร่วมใจสร้างอนาคต (รอบเปิดภาคการศึกษา)',
            'title_en': 'PSU Phuket Alumni Association Future Builder Grant',
            'category': 'general',
            'description': 'ทุนการศึกษาจากสมาคมศิษย์เก่า มหาวิทยาลัยสงขลานครินทร์ วิทยาเขตภูเก็ต เพื่อมอบให้แก่นักศึกษารุ่นน้อง',
            'description_en': 'Generous scholarship contributed by PSU Phuket Alumni Association for current students.',
            'requirements': '1. นักศึกษาปริญญาตรีที่มีความประพฤติดี\n2. GPAX 2.50 ขึ้นไป',
            'requirements_en': '1. Undergraduate students with good conduct\n2. GPAX >= 2.50',
            'amount_per_semester': 15000.00,
            'capacity': 8,
            'start_date': today - timedelta(days=120),
            'end_date': today - timedelta(days=10),
            'status': 'closed',
        },
        {
            'title': 'ทุนวิจัยและปัญญาประดิษฐ์ระดับปริญญาตรี (AI & Data Science Excellence) 2568',
            'title_en': 'AI & Data Science Undergraduate Excellence Scholarship 2025',
            'category': 'general',
            'description': 'ทุนสนับสนุนการทำวิจัยและโครงงานพิเศษด้าน Generative AI, Data Science และ Machine Learning สำหรับภาคการศึกษาหน้า',
            'description_en': 'Special fund for undergraduate research projects in Generative AI, Data Science, and Machine Learning.',
            'requirements': '1. นักศึกษาชั้นปีที่ 3-4\n2. GPAX ไม่ต่ำกว่า 3.25\n3. ข้อเสนอโครงการวิจัย (Proposal)',
            'requirements_en': '1. 3rd-4th year students\n2. GPAX >= 3.25\n3. Comprehensive research project proposal',
            'amount_per_semester': 40000.00,
            'capacity': 5,
            'start_date': today + timedelta(days=15),
            'end_date': today + timedelta(days=90),
            'status': 'draft',
        },

        # ==============================================================
        # --- Exchange Scholarships (exchange) ---
        # ==============================================================
        {
            'title': 'ทุนแลกเปลี่ยนระยะสั้นภาคฤดูร้อน ณ ประเทศเกาหลีใต้ (Korea University Short-term)',
            'title_en': 'Korea University Short-term Summer Exchange Scholarship',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนค่าเดินทางและค่าครองชีพสำหรับการศึกษาวัฒนธรรมและภาษาเกาหลีระยะสั้น 4 สัปดาห์ ณ ประเทศเกาหลีใต้',
            'description_en': 'Stipend and travel support for a 4-week summer language and culture exchange program in South Korea.',
            'requirements': '1. นักศึกษาชั้นปีที่ 2 ขึ้นไป ทุกคณะ\n2. GPAX ไม่ต่ำกว่า 3.00\n3. ผลคะแนนภาษาอังกฤษ TOEIC 600+ หรือเทียบเท่า',
            'requirements_en': '1. 2nd year students and above\n2. GPAX >= 3.00\n3. TOEIC score 600+ or equivalent',
            'amount_per_semester': 75000.00,
            'capacity': 4,
            'start_date': today - timedelta(days=25),
            'end_date': today + timedelta(days=3),
            'status': 'active',
        },
        {
            'title': 'ทุนแลกเปลี่ยนนักศึกษาภาคฤดูร้อน มหาวิทยาลัยแห่งชาติไต้หวัน (NTU Summer Exchange)',
            'title_en': 'National Taiwan University (NTU) Summer Program Scholarship',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนการเข้าร่วมโครงการเรียนรู้นวัตกรรมและภาษาจีน ณ National Taiwan University',
            'description_en': 'Scholarship for summer innovation and Chinese language immersion at National Taiwan University.',
            'requirements': '1. นักศึกษาปริญญาตรีชั้นปีที่ 2-3\n2. GPAX 3.20 ขึ้นไป\n3. ผ่านการสัมภาษณ์ความพร้อมภาษาอังกฤษหรือจีน',
            'requirements_en': '1. 2nd-3rd year students\n2. GPAX >= 3.20\n3. English or Chinese interview qualification',
            'amount_per_semester': 50000.00,
            'capacity': 5,
            'start_date': today - timedelta(days=20),
            'end_date': today + timedelta(days=7),
            'status': 'active',
        },
        {
            'title': 'ทุนแลกเปลี่ยนนักศึกษานานาชาติ ณ มหาวิทยาลัยคิวชู (Kyushu University, Japan)',
            'title_en': 'Kyushu University Japan Student Exchange Program Grant',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนค่าตั๋วเครื่องบินและค่าครองชีพสำหรับการศึกษาแลกเปลี่ยน 1 ภาคการศึกษา ณ ประเทศญี่ปุ่น',
            'description_en': 'Flight and monthly living allowance support for a one-semester academic exchange at Kyushu University, Japan.',
            'requirements': '1. นักศึกษาชั้นปีที่ 2 ขึ้นไป\n2. GPAX ไม่ต่ำกว่า 3.25\n3. คะแนนภาษาอังกฤษ TOEIC 650+ หรือ IELTS 6.0+',
            'requirements_en': '1. 2nd year or above\n2. GPAX >= 3.25\n3. TOEIC 650+ or IELTS 6.0+',
            'amount_per_semester': 85000.00,
            'capacity': 4,
            'start_date': today - timedelta(days=40),
            'end_date': today + timedelta(days=14),
            'status': 'active',
        },
        {
            'title': 'ทุนสหกิจศึกษานานาชาติและฝึกงานด้านเทคโนโลยี ณ ประเทศสิงคโปร์ (Tech Internship)',
            'title_en': 'Singapore Global Tech Internship and Cooperative Education Grant',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนค่าใช้จ่ายสำหรับนักศึกษาที่ได้รับตอบรับเข้าฝึกงานในบริษัทเทคโนโลยีชั้นนำ ณ ประเทศสิงคโปร์',
            'description_en': 'Support grant for students securing approved cooperative internships at tech firms in Singapore.',
            'requirements': '1. นักศึกษาชั้นปีที่ 3 หรือ 4\n2. GPAX ไม่ต่ำกว่า 3.00\n3. หนังสือตอบรับการฝึกงานจากบริษัทปลายทาง',
            'requirements_en': '1. 3rd or 4th year student\n2. GPAX >= 3.00\n3. Official internship acceptance letter',
            'amount_per_semester': 60000.00,
            'capacity': 6,
            'start_date': today - timedelta(days=20),
            'end_date': today + timedelta(days=35),
            'status': 'active',
        },
        {
            'title': 'ทุนแลกเปลี่ยนวัฒนธรรมและการท่องเที่ยว ณ มหาวิทยาลัยฮ่องกง (PolyU Hong Kong)',
            'title_en': 'Hong Kong PolyU Hospitality & Cultural Exchange Grant',
            'category': 'exchange',
            'description': 'ทุนแลกเปลี่ยนทางวิชาการและการจัดการการท่องเที่ยวและการบริการ ณ The Hong Kong Polytechnic University',
            'description_en': 'Academic and hospitality management exchange scholarship at The Hong Kong Polytechnic University.',
            'requirements': '1. นักศึกษาคณะการบริการและการท่องเที่ยว (FHT)\n2. GPAX ไม่ต่ำกว่า 3.20\n3. คะแนนภาษาอังกฤษ IELTS 6.0 ขึ้นไป',
            'requirements_en': '1. Faculty of Hospitality and Tourism students\n2. GPAX >= 3.20\n3. IELTS 6.0+',
            'amount_per_semester': 65000.00,
            'capacity': 4,
            'start_date': today - timedelta(days=30),
            'end_date': today + timedelta(days=60),
            'status': 'active',
        },
        {
            'title': 'ทุนแลกเปลี่ยนภาษาและวัฒนธรรมยุโรป (Erasmus+ Mobility Programme)',
            'title_en': 'European Union Erasmus+ Student Mobility Grant',
            'category': 'exchange',
            'description': 'โครงการแลกเปลี่ยนนักศึกษาระหว่าง ม.อ. ภูเก็ต กับสถาบันคู่สัญญาในสหภาพยุโรป',
            'description_en': 'Comprehensive mobility grant funded under EU Erasmus+ partner university agreements.',
            'requirements': '1. GPAX 3.50 ขึ้นไป\n2. มีผลสอบภาษาอังกฤษ IELTS 6.5 ขึ้นไป\n3. ผ่านการสัมภาษณ์จากคณะกรรมการนานาชาติ',
            'requirements_en': '1. GPAX >= 3.50\n2. IELTS 6.5+\n3. International panel interview qualification',
            'amount_per_semester': 110000.00,
            'capacity': 2,
            'start_date': today - timedelta(days=90),
            'end_date': today - timedelta(days=5),
            'status': 'closed',
        },
        {
            'title': 'ทุนแลกเปลี่ยนนักศึกษาอาเซียน AIMS Programme (Malaysia & Indonesia)',
            'title_en': 'ASEAN International Mobility for Students (AIMS) Programme',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนการแลกเปลี่ยนนักศึกษาภายใต้กรอบความร่วมมือกลุ่มประเทศอาเซียน',
            'description_en': 'ASEAN regional student mobility fund covering participating universities across Southeast Asia.',
            'requirements': '1. นักศึกษาชั้นปีที่ 2-3\n2. GPAX 2.80 ขึ้นไป\n3. มีความพร้อมในการปรับตัวเข้ากับสิ่งแวดล้อมพหุวัฒนธรรม',
            'requirements_en': '1. 2nd-3rd year students\n2. GPAX >= 2.80\n3. Multicultural adaptability profile',
            'amount_per_semester': 45000.00,
            'capacity': 6,
            'start_date': today + timedelta(days=10),
            'end_date': today + timedelta(days=60),
            'status': 'draft',
        },

        # ==============================================================
        # --- Fee Waiver Scholarships (fee_waiver) ---
        # ==============================================================
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาสำหรับผู้มีความสามารถพิเศษด้านดนตรีและศิลปวัฒนธรรม (รอบเร่งรัด)',
            'title_en': 'Express Arts & Music Talent Full Tuition Waiver Scholarship',
            'category': 'fee_waiver',
            'description': 'ทุนยกเว้นค่าเทอมเต็มจำนวนสำหรับนักศึกษาที่มีความสามารถพิเศษและร่วมทำกิจกรรมเผยแพร่วัฒนธรรม ม.อ. ภูเก็ต',
            'description_en': '100% tuition waiver for students demonstrating exceptional musical or cultural arts achievements.',
            'requirements': '1. นักศึกษาทุกคณะและทุกชั้นปี\n2. มีผลงานการแสดงหรือรางวัลระดับจังหวัดขึ้นไป\n3. GPAX ไม่ต่ำกว่า 2.50',
            'requirements_en': '1. Students of all faculties\n2. Provincial or national arts awards\n3. GPAX >= 2.50',
            'amount_per_semester': 20000.00,
            'capacity': 5,
            'start_date': today - timedelta(days=30),
            'end_date': today + timedelta(days=4),
            'status': 'active',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษา 50% สำหรับนักศึกษาจิตอาสาพัฒนาชุมชนภูเก็ต',
            'title_en': '50% Tuition Waiver for Phuket Community Volunteer Leaders',
            'category': 'fee_waiver',
            'description': 'ทุนลดหย่อนค่าธรรมเนียมการศึกษากึ่งหนึ่งสำหรับนักศึกษาที่อุทิศตนช่วยเหลืองานจิตอาสาและพัฒนาชุมชนท้องถิ่นภูเก็ต',
            'description_en': 'Half-tuition waiver for students demonstrating significant volunteer dedication to Phuket communities.',
            'requirements': '1. นักศึกษาชั้นปีที่ 2-4\n2. มีชั่วโมงจิตอาสาไม่น้อยกว่า 50 ชั่วโมงต่อปีการศึกษา\n3. GPAX ไม่ต่ำกว่า 2.40',
            'requirements_en': '1. 2nd-4th year students\n2. Minimum 50 certified volunteer hours\n3. GPAX >= 2.40',
            'amount_per_semester': 16000.00,
            'capacity': 8,
            'start_date': today - timedelta(days=25),
            'end_date': today + timedelta(days=8),
            'status': 'active',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษา 100% สำหรับผู้นำนักศึกษาและนักกิจกรรมดีเด่น',
            'title_en': '100% Full Tuition Waiver for Student Government and Club Leaders',
            'category': 'fee_waiver',
            'description': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาเต็มจำนวน (100%) เพื่อเป็นขวัญกำลังใจแก่ผู้บำเพ็ญประโยชน์ต่อส่วนรวม สโมสรนักศึกษา และสภานักศึกษา',
            'description_en': 'Full tuition waiver honoring executive student council, club officers, and campus leaders.',
            'requirements': '1. เป็นกรรมการสโมสรนักศึกษา/สภานักศึกษา หรือผู้นำชมรม\n2. GPAX ไม่ต่ำกว่า 2.50\n3. ผ่านการรับรองจากกองกิจการนักศึกษา',
            'requirements_en': '1. Student council or club committee member\n2. GPAX >= 2.50\n3. Endorsement from Student Affairs',
            'amount_per_semester': 32000.00,
            'capacity': 10,
            'start_date': today - timedelta(days=50),
            'end_date': today + timedelta(days=21),
            'status': 'active',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษา 50% สำหรับนักกีฬาตัวแทนมหาวิทยาลัย',
            'title_en': '50% Tuition Waiver for University Varsity Athletes',
            'category': 'fee_waiver',
            'description': 'ทุนยกเว้นค่าเล่าเรียนครึ่งจำนวน (50%) สำหรับนักกีฬาที่สร้างชื่อเสียงในการแข่งขันกีฬามหาวิทยาลัยแห่งประเทศไทย',
            'description_en': 'Half tuition waiver honoring athletes representing PSU in national university sporting competitions.',
            'requirements': '1. เป็นนักกีฬาตัวแทน ม.อ. หรือระดับเยาวชนทีมชาติ\n2. GPAX ไม่ต่ำกว่า 2.20\n3. มีหนังสือรับรองจากศูนย์กีฬา',
            'requirements_en': '1. Varsity team member or national youth athlete\n2. GPAX >= 2.20\n3. Certification from Sports Center',
            'amount_per_semester': 16000.00,
            'capacity': 12,
            'start_date': today - timedelta(days=35),
            'end_date': today + timedelta(days=40),
            'status': 'active',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาสำหรับนักศึกษาบุตรผู้มีรายได้น้อย (ทุนเรียนฟรี 100%)',
            'title_en': 'Low-Income Family 100% Tuition Assistance Waiver',
            'category': 'fee_waiver',
            'description': 'ทุนช่วยเหลือครอบครัวนักศึกษาที่มีฐานะยากจนพิเศษ ให้ได้รับการยกเว้นค่าเล่าเรียนตลอดทั้งภาคการศึกษา',
            'description_en': 'Complete semester tuition relief for families undergoing extreme economic hardship.',
            'requirements': '1. รายได้รวมครอบครัวไม่เกิน 200,000 บาท/ปี\n2. มีความตั้งใจเรียนดี GPAX >= 2.30\n3. มีหนังสือรับรองรายได้จากผู้นำชุมชน',
            'requirements_en': '1. Annual family income under 200,000 THB\n2. GPAX >= 2.30\n3. Community leader verification letter',
            'amount_per_semester': 32000.00,
            'capacity': 15,
            'start_date': today - timedelta(days=40),
            'end_date': today + timedelta(days=55),
            'status': 'active',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาสำหรับผู้มีความสามารถพิเศษด้านศิลปวัฒนธรรมและดนตรี',
            'title_en': 'Cultural and Performing Arts Tuition Waiver (Past Round)',
            'category': 'fee_waiver',
            'description': 'ทุนส่งเสริมผู้มีความสามารถโดดเด่นด้านนาฏศิลป์ ดนตรีสากล ดนตรีไทย หรือศิลปะร่วมสมัย',
            'description_en': 'Talent tuition waiver celebrating exceptional stage and musical performers.',
            'requirements': '1. มีประวัติผลงานการแสดงหรือประกวดระดับจังหวัดขึ้นไป\n2. GPAX ไม่ต่ำกว่า 2.50',
            'requirements_en': '1. Provincial competition track record\n2. GPAX >= 2.50',
            'amount_per_semester': 16000.00,
            'capacity': 6,
            'start_date': today - timedelta(days=70),
            'end_date': today - timedelta(days=2),
            'status': 'closed',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาประเภทพิเศษ ภาคการศึกษา 2/2567',
            'title_en': 'Academic Peer Tutor Tuition Waiver Semester 2/2024',
            'category': 'fee_waiver',
            'description': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาเต็มจำนวน สำหรับผู้ผ่านการคัดเลือกเป็นติวเตอร์วิชาการของมหาวิทยาลัย',
            'description_en': 'Full tuition fee waiver for selected peer academic learning center tutors.',
            'requirements': '1. GPAX 3.50 ขึ้นไป\n2. ผ่านการทดสอบคัดเลือกติวเตอร์ประจำศูนย์การเรียนรู้',
            'requirements_en': '1. GPAX >= 3.50\n2. Peer tutoring assessment certification',
            'amount_per_semester': 32000.00,
            'capacity': 8,
            'start_date': today + timedelta(days=20),
            'end_date': today + timedelta(days=75),
            'status': 'draft',
        },

        # ==============================================================
        # --- Lunch Scholarships (lunch) ---
        # ==============================================================
        {
            'title': 'ทุนคูปองอาหารกลางวันเร่งด่วนประจำสัปดาห์ (Quick Relief Meal Voucher)',
            'title_en': 'Weekly Emergency Meal Voucher Assistance Grant',
            'category': 'lunch',
            'description': 'ทุนคูปองอาหารกลางวันแบบเร่งด่วนสำหรับนักศึกษาที่มีปัญหาค่าใช้จ่ายประจำวันเฉียบพลัน รับคูปองได้ทันที',
            'description_en': 'Immediate daily meal vouchers for students encountering sudden living expense shortages.',
            'requirements': '1. นักศึกษาปริญญาตรี ม.อ. ภูเก็ต ทุกคน\n2. ไม่จำกัดเกรดเฉลี่ยสะสม\n3. ยื่นคำขอผ่านระบบหรือติดต่อกองกิจการนักศึกษา',
            'requirements_en': '1. All undergraduate students\n2. No GPA requirement\n3. Verified immediate necessity',
            'amount_per_semester': 3000.00,
            'capacity': 20,
            'start_date': today - timedelta(days=10),
            'end_date': today + timedelta(days=2),
            'status': 'active',
        },
        {
            'title': 'ทุนสวัสดิการอาหารกลางวันเพื่อสุขอนามัยและโภชนาการนักศึกษา (Health & Lunch)',
            'title_en': 'Student Nutrition and Healthy Meal Support Grant',
            'category': 'lunch',
            'description': 'ทุนอาหารกลางวันสำหรับนักศึกษาที่มีความจำเป็นด้านสุขภาพและโภชนาการ พร้อมสิทธิรับประทานอาหาร ณ โรงอาหารกลาง',
            'description_en': 'Subsidized meal support promoting balanced nutrition for students in need.',
            'requirements': '1. นักศึกษาปริญญาตรีชั้นปีที่ 1-4\n2. GPAX ไม่ต่ำกว่า 2.00\n3. มีความต้องการการสนับสนุนอาหารกลางวันอย่างต่อเนื่อง',
            'requirements_en': '1. 1st-4th year students\n2. GPAX >= 2.00\n3. Documented continuous meal support requirement',
            'amount_per_semester': 5000.00,
            'capacity': 25,
            'start_date': today - timedelta(days=20),
            'end_date': today + timedelta(days=6),
            'status': 'active',
        },
        {
            'title': 'ทุนอาหารกลางวันเพื่อน้อง ม.อ. ภูเก็ต ประจำภาคการศึกษาที่ 1/2567',
            'title_en': 'PSU Phuket Campus Lunch Welfare Scholarship Term 1/2024',
            'category': 'lunch',
            'description': 'ทุนคูปองอาหารมูลค่าวันละ 100 บาท เพื่อสวัสดิการอาหารกลางวันและลดค่าใช้จ่ายประจำวันของนักศึกษา',
            'description_en': 'Daily 100 THB meal coupons to alleviate daily student living expenses throughout the semester.',
            'requirements': '1. นักศึกษาปริญญาตรีทุกชั้นปี\n2. มีความเดือดร้อนด้านค่าครองชีพ\n3. GPAX ไม่ต่ำกว่า 2.00',
            'requirements_en': '1. All undergraduate levels\n2. Living cost hardship\n3. GPAX >= 2.00',
            'amount_per_semester': 7500.00,
            'capacity': 35,
            'start_date': today - timedelta(days=60),
            'end_date': today + timedelta(days=25),
            'status': 'active',
        },
        {
            'title': 'ทุนสนับสนุนค่าครองชีพและอาหารกลางวันสำหรับนักศึกษาหอพักในมหาวิทยาลัย',
            'title_en': 'Dormitory Resident Daily Living and Lunch Support Grant',
            'category': 'lunch',
            'description': 'ทุนช่วยเหลืออาหารและของใช้อุปโภคบริโภคจำเป็นสำหรับนักศึกษาที่พักอาศัยในหอพัก ม.อ. ภูเก็ต',
            'description_en': 'Meal and subsistence subsidy for students residing in on-campus university dormitories.',
            'requirements': '1. เป็นผู้พักอาศัยในหอพักนักศึกษา ม.อ. ภูเก็ต\n2. GPAX 2.00 ขึ้นไป\n3. มีหนังสือรับรองจากอาจารย์ที่ปรึกษา',
            'requirements_en': '1. Resident of PSU Phuket dormitories\n2. GPAX >= 2.00\n3. Advisor recommendation note',
            'amount_per_semester': 6000.00,
            'capacity': 25,
            'start_date': today - timedelta(days=30),
            'end_date': today + timedelta(days=45),
            'status': 'active',
        },
        {
            'title': 'ทุนอาหารกลางวันมูลนิธิ ม.อ. เพื่อการพัฒนาคุณภาพชีวิตนักศึกษา',
            'title_en': 'PSU Foundation Quality of Life Lunch Subsidy',
            'category': 'lunch',
            'description': 'ทุนอาหารกลางวันมอบให้แก่นักศึกษาที่มีความประพฤติดีและมุ่งมั่นในการเรียนจากมูลนิธิมหาวิทยาลัยสงขลานครินทร์',
            'description_en': 'Semester-long campus cafeteria dining allowance supported by Prince of Songkla University Foundation.',
            'requirements': '1. นักศึกษาทุกคณะ\n2. GPAX 2.20 ขึ้นไป\n3. เข้าร่วมกิจกรรมบำเพ็ญประโยชน์ต่อมหาวิทยาลัย',
            'requirements_en': '1. Students across all faculties\n2. GPAX >= 2.20\n3. Active campus service participation',
            'amount_per_semester': 8000.00,
            'capacity': 30,
            'start_date': today - timedelta(days=15),
            'end_date': today + timedelta(days=50),
            'status': 'active',
        },
        {
            'title': 'ทุนอาหารกลางวันฉุกเฉินสู้ภัยเศรษฐกิจ (รอบช่วยเหลือเร่งด่วน)',
            'title_en': 'Emergency Campus Food Relief Subsidy (Express Round)',
            'category': 'lunch',
            'description': 'ทุนสวัสดิการอาหารแบบเร่งด่วนพิจารณาผลภายใน 3 วันทำการ เพื่อช่วยเหลือนักศึกษาที่ประสบปัญหาเฉียบพลัน',
            'description_en': 'Rapid-approval emergency meal relief grant for critical living cost situations.',
            'requirements': '1. นักศึกษาที่มีความจำเป็นเร่งด่วนด้านค่าอาหาร\n2. ไม่จำกัดเกรดเฉลี่ยขั้นต่ำ',
            'requirements_en': '1. Critical nutrition need\n2. No minimum GPA requirement',
            'amount_per_semester': 5000.00,
            'capacity': 20,
            'start_date': today - timedelta(days=10),
            'end_date': today + timedelta(days=3),
            'status': 'active',
        },
        {
            'title': 'ทุนคูปองอาหารกลางวันและโภชนาการนักศึกษา ภาคการศึกษา 2/2567',
            'title_en': 'Student Nutrition and Food Coupon Scheme Term 2/2024',
            'category': 'lunch',
            'description': 'ทุนจัดสรรคูปองอาหารประจำโรงอาหารกลาง ม.อ. ภูเก็ต สำหรับภาคการศึกษาปัจจุบัน',
            'description_en': 'Semester meal voucher program at PSU Phuket Central Cafeteria.',
            'requirements': '1. นักศึกษาปริญญาตรีทุกคณะ\n2. GPAX ไม่ต่ำกว่า 2.00',
            'requirements_en': '1. All undergraduate programs\n2. GPAX >= 2.00',
            'amount_per_semester': 8000.00,
            'capacity': 40,
            'start_date': today - timedelta(days=15),
            'end_date': today + timedelta(days=35),
            'status': 'active',
        },
        # ==============================================================
        # --- Additional Rich General Scholarships ---
        # ==============================================================
        {
            'title': 'ทุนเยาวชนคนดีศรี ม.อ. ภูเก็ต (PSU Phuket Moral & Leadership Award)',
            'title_en': 'PSU Phuket Moral and Student Leadership Award',
            'category': 'general',
            'description': 'ทุนเชิดชูเกียรตินักศึกษาผู้มีจิตสาธารณะ เสียสละเพื่อส่วนรวม และเป็นผู้นำกิจกรรมนักศึกษาที่เป็นแบบอย่างที่ดี',
            'description_en': 'Leadership and civic virtue award for students actively engaged in community service and university volunteerism.',
            'requirements': '1. นักศึกษาทุกชั้นปี\n2. มีประวัติการทำกิจกรรมบำเพ็ญประโยชน์ไม่ต่ำกว่า 40 ชั่วโมง\n3. GPAX ไม่ต่ำกว่า 2.50',
            'requirements_en': '1. Undergraduate students of all years\n2. Minimum 40 hours of verified community service\n3. GPAX >= 2.50',
            'amount_per_semester': 25000.00,
            'capacity': 8,
            'start_date': today - timedelta(days=12),
            'end_date': today + timedelta(days=4),
            'status': 'active',
        },
        {
            'title': 'ทุนส่งเสริมความเป็นเลิศด้านนวัตกรรม AI และเทคโนโลยีดิจิทัล',
            'title_en': 'Excellence in AI and Digital Innovation Grant',
            'category': 'general',
            'description': 'ทุนสนับสนุนโครงงานวิจัยและการประยุกต์ใช้เทคโนโลยีปัญญาประดิษฐ์เพื่อแก้ไขปัญหาของจังหวัดภูเก็ตและภูมิภาคอันดามัน',
            'description_en': 'Special funding for student-led projects applying Artificial Intelligence and digital solutions for local societal impact.',
            'requirements': '1. นักศึกษาคณะวิทยาการคำนวณ หรือสาขาวิชาที่เกี่ยวข้อง\n2. มีข้อเสนอโครงงาน AI/Data/IoT ชัดเจน\n3. GPAX ไม่ต่ำกว่า 2.80',
            'requirements_en': '1. College of Computing or tech-related degrees\n2. Concrete AI/IoT project proposal\n3. GPAX >= 2.80',
            'amount_per_semester': 35000.00,
            'capacity': 10,
            'start_date': today - timedelta(days=18),
            'end_date': today + timedelta(days=12),
            'status': 'active',
        },
        {
            'title': 'ทุนส่งเสริมทักษะกีฬาและสุขภาพนักศึกษา ม.อ. ภูเก็ต (Athletic Grant)',
            'title_en': 'PSU Phuket Student Athlete & Wellness Scholarship',
            'category': 'general',
            'description': 'ทุนสนับสนุนนักกีฬาตัวแทนวิทยาเขตและนักศึกษาที่มีความสามารถโดดเด่นทางด้านกีฬาและนันทนาการ',
            'description_en': 'Scholarship supporting university varsity athletes representing PSU Phuket in regional and national collegiate games.',
            'requirements': '1. เป็นนักกีฬาตัวแทนมหาวิทยาลัย หรือมีผลงานแข่งขันระดับจังหวัด/ชาติ\n2. GPAX ไม่ต่ำกว่า 2.00',
            'requirements_en': '1. University varsity athlete or provincial competition medal holder\n2. GPAX >= 2.00',
            'amount_per_semester': 15000.00,
            'capacity': 15,
            'start_date': today - timedelta(days=22),
            'end_date': today + timedelta(days=22),
            'status': 'active',
        },
        {
            'title': 'ทุนสนับสนุนนักศึกษาผู้มีความต้องการพิเศษและการเรียนรู้ที่เท่าเทียม',
            'title_en': 'Equal Opportunity and Inclusive Education Grant',
            'category': 'general',
            'description': 'ทุนช่วยเหลือและจัดสรรอุปกรณ์สนับสนุนการเรียนรู้สำหรับนักศึกษาที่มีความบกพร่องทางร่างกายหรือต้องการการดูแลเป็นพิเศษ',
            'description_en': 'Accessibility and assistive learning equipment grant ensuring equal educational opportunities.',
            'requirements': '1. นักศึกษาที่มีความต้องการพิเศษทุกชั้นปี\n2. มีหนังสือรับรองจากแพทย์หรือศูนย์สนับสนุนนักศึกษาพิการ',
            'requirements_en': '1. Students with special educational needs\n2. Medical certificate or DSS disability verification',
            'amount_per_semester': 30000.00,
            'capacity': 6,
            'start_date': today - timedelta(days=14),
            'end_date': today + timedelta(days=35),
            'status': 'active',
        },
        {
            'title': 'ทุนสมาคมศิษย์เก่า มหาวิทยาลัยสงขลานครินทร์ วิทยาเขตภูเก็ต เพื่อรุ่นน้อง',
            'title_en': 'PSU Phuket Alumni Association Undergrad Grant',
            'category': 'general',
            'description': 'ทุนการศึกษาจากใจศิษย์เก่า ม.อ. ภูเก็ต เพื่อมอบโอกาสทางการศึกษาแก่นักศึกษารุ่นน้องที่มีความมุ่งมั่นและกตัญญูกตเวที',
            'description_en': 'Endowment scholarship funded by alumni to assist promising juniors with their academic journey.',
            'requirements': '1. นักศึกษาชั้นปีที่ 2 ขึ้นไป\n2. GPAX 2.50 ขึ้นไป\n3. เขียนเรียงความความยาว 1 หน้า A4 เรื่องความมุ่งมั่นในการเรียน',
            'requirements_en': '1. 2nd year and above\n2. GPAX >= 2.50\n3. 1-page personal essay on academic commitment',
            'amount_per_semester': 20000.00,
            'capacity': 20,
            'start_date': today - timedelta(days=25),
            'end_date': today + timedelta(days=55),
            'status': 'active',
        },
        {
            'title': 'ทุนส่งเสริมนักศึกษาทำงานพิเศษและผู้ช่วยวิจัย (RA/TA Student Grant)',
            'title_en': 'Research Assistant & Academic Apprenticeship Grant',
            'category': 'general',
            'description': 'ทุนสนับสนุนนักศึกษาที่ช่วยงานวิจัย อาจารย์ หรือห้องปฏิบัติการเพื่อพัฒนาประสบการณ์จริงควบคู่การเรียน',
            'description_en': 'Research apprenticeship grant assisting undergraduate students working on faculty lab research.',
            'requirements': '1. นักศึกษาชั้นปีที่ 3-4\n2. มีอาจารย์ที่ปรึกษางานวิจัยรับรอง\n3. GPAX ไม่ต่ำกว่า 2.75',
            'requirements_en': '1. 3rd-4th year undergraduates\n2. Faculty research supervisor endorsement\n3. GPAX >= 2.75',
            'amount_per_semester': 18000.00,
            'capacity': 15,
            'start_date': today - timedelta(days=30),
            'end_date': today + timedelta(days=70),
            'status': 'active',
        },
        # ==============================================================
        # --- Additional Rich Exchange Scholarships ---
        # ==============================================================
        {
            'title': 'ทุนสนับสนุนการฝึกงานและสหกิจศึกษา ณ ประเทศสิงคโปร์ (Singapore Co-op Internship Grant)',
            'title_en': 'Singapore Co-op and Professional Internship Grant',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนค่าเดินทางและค่าครองชีพระหว่างฝึกงานสหกิจศึกษากับองค์กรชั้นนำในประเทศสิงคโปร์',
            'description_en': 'Travel and subsistence grant for international co-op internship placements in Singapore.',
            'requirements': '1. นักศึกษาชั้นปีที่ 3 หรือ 4 ที่ผ่านการคัดเลือกสหกิจศึกษาต่างประเทศ\n2. ผลสอบภาษาอังกฤษ TOEIC 600 ขึ้นไป\n3. GPAX >= 2.75',
            'requirements_en': '1. 3rd/4th year selected for overseas cooperative education\n2. TOEIC score >= 600\n3. GPAX >= 2.75',
            'amount_per_semester': 45000.00,
            'capacity': 8,
            'start_date': today - timedelta(days=20),
            'end_date': today + timedelta(days=3),
            'status': 'active',
        },
        {
            'title': 'ทุนโครงการแลกเปลี่ยนนักศึกษา มหาวิทยาลัยคู่สัญญาในประเทศเกาหลีใต้ (South Korea Exchange)',
            'title_en': 'South Korea Sister University Exchange Grant',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนการแลกเปลี่ยนทางวิชาการและวัฒนธรรม 1 ภาคการศึกษา ณ มหาวิทยาลัยในสาธารณรัฐเกาหลี',
            'description_en': 'One-semester mobility scholarship to partner institutions in South Korea.',
            'requirements': '1. นักศึกษาชั้นปีที่ 2-3 ทุกสาขาวิชา\n2. มีผลการเรียนดี GPAX >= 3.00\n3. ทักษะภาษาอังกฤษหรือเกาหลีระดับสื่อสารได้',
            'requirements_en': '1. 2nd-3rd year students\n2. Strong academic standing GPAX >= 3.00\n3. English/Korean conversational proficiency',
            'amount_per_semester': 40000.00,
            'capacity': 10,
            'start_date': today - timedelta(days=15),
            'end_date': today + timedelta(days=7),
            'status': 'active',
        },
        {
            'title': 'ทุนแลกเปลี่ยนวัฒนธรรมและภาษา ณ มหาวิทยาลัยในประเทศไต้หวัน (Taiwan Summer Exchange)',
            'title_en': 'Taiwan Cultural Immersion & Language Exchange Grant',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนโครงการศึกษาภาษาและวัฒนธรรมจีนระยะสั้นช่วงปิดภาคเรียน ณ ประเทศไต้หวัน',
            'description_en': 'Short-term Chinese language and cultural immersion grant during summer term in Taiwan.',
            'requirements': '1. นักศึกษาปริญญาตรีทุกคณะ\n2. GPAX ไม่ต่ำกว่า 2.50\n3. ความสนใจในภาษาและวัฒนธรรมเอเชีย',
            'requirements_en': '1. Undergraduate students of all faculties\n2. GPAX >= 2.50\n3. Demonstrated passion for Asian cultures',
            'amount_per_semester': 32000.00,
            'capacity': 12,
            'start_date': today - timedelta(days=18),
            'end_date': today + timedelta(days=16),
            'status': 'active',
        },
        {
            'title': 'ทุนเข้าร่วมการแข่งขันโครงงานระดับนานาชาติในภูมิภาคอาเซียน (ASEAN Youth Summit Grant)',
            'title_en': 'ASEAN Youth Innovation & Competition Travel Grant',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนค่าตั๋วเครื่องบินและค่าลงทะเบียนสำหรับทีมนักศึกษาที่เป็นตัวแทนประเทศไทยเข้าแข่งขันโครงงานนวัตกรรม',
            'description_en': 'Travel stipend and registration fee support for students representing Thailand in regional ASEAN competitions.',
            'requirements': '1. มีหลักฐานการผ่านเข้ารอบการแข่งขันระดับนานาชาติในอาเซียน\n2. หนังสือรับรองจากคณะต้นสังกัด',
            'requirements_en': '1. Acceptance/invitation letter to international ASEAN competition\n2. Faculty endorsement letter',
            'amount_per_semester': 25000.00,
            'capacity': 15,
            'start_date': today - timedelta(days=10),
            'end_date': today + timedelta(days=28),
            'status': 'active',
        },
        {
            'title': 'ทุนโครงการแลกเปลี่ยนนักศึกษา ณ มหาวิทยาลัยในประเทศเยอรมนี (Europe Mobility Grant)',
            'title_en': 'European University Semester Mobility Scholarship',
            'category': 'exchange',
            'description': 'ทุนอุดหนุนการแลกเปลี่ยนเรียนรู้ ณ มหาวิทยาลัยคู่สัญญาในสหภาพยุโรป (เยอรมนี/ออสเตรีย) เป็นเวลา 1 ภาคการศึกษา',
            'description_en': 'Prestigious bilateral semester exchange grant for coursework at partner universities in Europe.',
            'requirements': '1. นักศึกษาชั้นปีที่ 2 หรือ 3\n2. ผลสอบ IELTS 6.0 หรือ TOEFL iBT 78 ขึ้นไป\n3. GPAX >= 3.25',
            'requirements_en': '1. 2nd or 3rd year students\n2. IELTS >= 6.0 or TOEFL iBT >= 78\n3. Cumulative GPAX >= 3.25',
            'amount_per_semester': 50000.00,
            'capacity': 5,
            'start_date': today - timedelta(days=25),
            'end_date': today + timedelta(days=48),
            'status': 'active',
        },
        {
            'title': 'ทุนนำเสนอผลงานวิจัยระดับนานาชาติต่างประเทศสำหรับนักศึกษาปริญญาตรี',
            'title_en': 'Undergraduate International Conference Presentation Grant',
            'category': 'exchange',
            'description': 'ทุนสนับสนุนค่าใช้จ่ายในการเดินทางไปนำเสนอผลงานวิจัยแบบปากเปล่า (Oral Presentation) ในการประชุมวิชาการระดับสากล',
            'description_en': 'Full travel sponsorship for undergraduate primary authors presenting accepted papers at peer-reviewed international conferences.',
            'requirements': '1. มีบทความวิจัยได้รับการตอบรับให้นำเสนอในการประชุมระดับนานาชาติ\n2. เป็นชื่อแรก (First Author)\n3. GPAX >= 3.00',
            'requirements_en': '1. Official acceptance letter for oral presentation\n2. Student is first author\n3. GPAX >= 3.00',
            'amount_per_semester': 35000.00,
            'capacity': 10,
            'start_date': today - timedelta(days=30),
            'end_date': today + timedelta(days=75),
            'status': 'active',
        },
        # ==============================================================
        # --- Additional Rich Fee Waiver Scholarships ---
        # ==============================================================
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษา 100% สำหรับผู้มีความสามารถพิเศษด้านศิลปวัฒนธรรมอันดามัน',
            'title_en': 'Full Tuition Waiver for Andaman Arts and Cultural Talents',
            'category': 'fee_waiver',
            'description': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาเต็มจำนวน 100% สำหรับนักศึกษาที่มีความสามารถโดดเด่นด้านดนตรี นาฏศิลป์ หรือศิลปวัฒนธรรมท้องถิ่น',
            'description_en': '100% tuition exemption celebrating students with remarkable talents in performing arts and Andaman cultural heritage.',
            'requirements': '1. มีแฟ้มสะสมผลงานหรือรางวัลด้านศิลปวัฒนธรรมระดับเขต/ชาติ\n2. เข้าร่วมกิจกรรมแสดงศิลปวัฒนธรรมของมหาวิทยาลัย\n3. GPAX >= 2.25',
            'requirements_en': '1. Proven cultural arts competition awards portfolio\n2. Commitment to university cultural performances\n3. GPAX >= 2.25',
            'amount_per_semester': 28000.00,
            'capacity': 8,
            'start_date': today - timedelta(days=15),
            'end_date': today + timedelta(days=2),
            'status': 'active',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาสำหรับนักเรียนโอลิมปิกวิชาการ (POSN Olympiad Tuition Waiver)',
            'title_en': 'POSN Academic Olympiad Full Tuition Waiver',
            'category': 'fee_waiver',
            'description': 'ทุนยกเว้นค่าเทอมสำหรับนักศึกษาที่เคยผ่านการอบรมค่ายโอลิมปิกวิชาการ สอวน. หรือการแข่งขันโครงงานวิทยาศาสตร์ระดับชาติ',
            'description_en': 'Full semester tuition fee waiver for alumni of POSN Science/Math Olympiad training camps.',
            'requirements': '1. มีเกียรติบัตรผ่านค่าย สอวน. หรือการแข่งขันโครงงานระดับประเทศ\n2. นักศึกษาใหม่หรือนักศึกษาปัจจุบันชั้นปีที่ 1-2\n3. GPAX >= 3.00',
            'requirements_en': '1. POSN camp certificate or national science contest medal\n2. 1st or 2nd year student\n3. GPAX >= 3.00',
            'amount_per_semester': 32000.00,
            'capacity': 6,
            'start_date': today - timedelta(days=14),
            'end_date': today + timedelta(days=6),
            'status': 'active',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษา 50% สำหรับบุตรข้าราชการและบุคลากรทางการศึกษา',
            'title_en': '50% Tuition Waiver for Civil Servants and Educators Children',
            'category': 'fee_waiver',
            'description': 'ทุนสวัสดิการลดหย่อนค่าเล่าเรียน 50% ต่อภาคการศึกษา เพื่อสนับสนุนครอบครัวบุคลากรทางการศึกษาและเจ้าหน้าที่รัฐ',
            'description_en': '50% tuition reduction supporting families of public educators and civil servants.',
            'requirements': '1. บิดาหรือมารดาเป็นข้าราชการ/พนักงานรัฐ/ครูอาจารย์\n2. GPAX ไม่ต่ำกว่า 2.50\n3. มีหนังสือรับรองการทำงานของผู้ปกครอง',
            'requirements_en': '1. Parent is civil servant or school educator\n2. GPAX >= 2.50\n3. Employment verification letter of parent',
            'amount_per_semester': 14000.00,
            'capacity': 20,
            'start_date': today - timedelta(days=25),
            'end_date': today + timedelta(days=19),
            'status': 'active',
        },
        {
            'title': 'ทุนลดหย่อนค่าธรรมเนียมการศึกษาสำหรับพี่น้องเรียนพร้อมกันใน ม.อ. ภูเก็ต (Sibling Discount)',
            'title_en': 'PSU Phuket Sibling Simultaneous Enrollment Tuition Discount',
            'category': 'fee_waiver',
            'description': 'ทุนช่วยเหลือแบ่งเบาภาระครอบครัวที่มีบุตรกำลังศึกษาอยู่ใน ม.อ. ภูเก็ต พร้อมกันตั้งแต่ 2 คนขึ้นไป',
            'description_en': 'Financial discount alleviating tuition burden for parents with two or more siblings studying concurrently at PSU Phuket.',
            'requirements': '1. มีพี่น้องร่วมบิดามารดาเดียวกันกำลังศึกษาใน ม.อ. ภูเก็ต ในภาคการศึกษาปัจจุบัน\n2. GPAX แต่ละคนไม่ต่ำกว่า 2.00',
            'requirements_en': '1. Siblings concurrently enrolled at PSU Phuket\n2. Minimum GPAX 2.00 each',
            'amount_per_semester': 12000.00,
            'capacity': 25,
            'start_date': today - timedelta(days=20),
            'end_date': today + timedelta(days=32),
            'status': 'active',
        },
        {
            'title': 'ทุนสนับสนุนค่าธรรมเนียมการศึกษาโครงการความร่วมมือเครือข่ายโรงเรียนมัธยมภาคใต้',
            'title_en': 'Southern High School Partnership Network Fee Support',
            'category': 'fee_waiver',
            'description': 'ทุนส่งเสริมการเข้าศึกษาต่อสำหรับนักเรียนจากโรงเรียนเครือข่ายความร่วมมือทางวิชาการใน 14 จังหวัดภาคใต้',
            'description_en': 'Special tuition fellowship for graduates admitted from MoA partner secondary schools in Southern Thailand.',
            'requirements': '1. สำเร็จการศึกษาจากโรงเรียนเครือข่าย ม.อ. ใน 14 จังหวัดภาคใต้\n2. GPAX ม.ปลาย หรือในมหาวิทยาลัยไม่ต่ำกว่า 2.75',
            'requirements_en': '1. High school graduate from MOU partner schools in Southern Thailand\n2. GPAX >= 2.75',
            'amount_per_semester': 20000.00,
            'capacity': 15,
            'start_date': today - timedelta(days=30),
            'end_date': today + timedelta(days=52),
            'status': 'active',
        },
        {
            'title': 'ทุนยกเว้นค่าธรรมเนียมการศึกษาภาคฤดูร้อนสำหรับวิชาศึกษาทั่วไปและฝึกงาน',
            'title_en': 'Summer Term General Education & Internship Tuition Waiver',
            'category': 'fee_waiver',
            'description': 'ทุนยกเว้นค่าลงทะเบียนเรียนในภาคฤดูร้อนเพื่อให้นักศึกษาสามารถสำเร็จการศึกษาตามแผนหรือลงวิชาฝึกงานได้อย่างราบรื่น',
            'description_en': 'Summer tuition fee exemption covering prerequisite coursework and required summer internships.',
            'requirements': '1. นักศึกษาชั้นปีที่ 3-4 ที่ต้องลงทะเบียนภาคฤดูร้อนตามแผนการเรียน\n2. GPAX ไม่ต่ำกว่า 2.20',
            'requirements_en': '1. 3rd-4th year students with mandatory summer enrollment\n2. GPAX >= 2.20',
            'amount_per_semester': 9000.00,
            'capacity': 30,
            'start_date': today - timedelta(days=35),
            'end_date': today + timedelta(days=85),
            'status': 'active',
        },
        # ==============================================================
        # --- Additional Rich Lunch & Living Subsidy Scholarships ---
        # ==============================================================
        {
            'title': 'ทุนคูปองอาหารกลางวันโครงการ "อิ่มท้องพร้อมเรียน" ม.อ. ภูเก็ต (Term Lunch Subsidy)',
            'title_en': 'PSU Phuket "Nourished Minds" Campus Lunch Voucher Grant',
            'category': 'lunch',
            'description': 'ทุนจัดสรรคูปองอาหารกลางวันประจำวัน ณ โรงอาหารกลาง เพื่อช่วยเหลือนักศึกษาตลอดภาคการศึกษา',
            'description_en': 'Daily campus cafeteria meal ticket subsidy ensuring wholesome student nutrition throughout the semester.',
            'requirements': '1. นักศึกษาทุกคณะและทุกชั้นปี\n2. มีความเดือดร้อนด้านค่าใช้จ่ายประจำวัน\n3. GPAX >= 2.00',
            'requirements_en': '1. Undergraduate students of all programs\n2. Demonstrated daily living expense constraint\n3. GPAX >= 2.00',
            'amount_per_semester': 6500.00,
            'capacity': 40,
            'start_date': today - timedelta(days=12),
            'end_date': today + timedelta(days=4),
            'status': 'active',
        },
        {
            'title': 'ทุนอาหารกลางวันช่วยเหลือค่าครองชีพนักศึกษาชั้นปีที่ 1 (Freshmen Nutrition Aid)',
            'title_en': 'Freshmen Campus Transition and Nutrition Support Grant',
            'category': 'lunch',
            'description': 'ทุนสวัสดิการอาหารเพื่อช่วยเหลือนักศึกษาใหม่ชั้นปีที่ 1 ในช่วงปรับตัวเข้าสู่รั้วมหาวิทยาลัยและลดค่าใช้จ่ายครอบครัว',
            'description_en': 'Targeted dining subsidy assisting newly admitted first-year students transitioning to university life.',
            'requirements': '1. นักศึกษาชั้นปีที่ 1 ม.อ. ภูเก็ต\n2. ครอบครัวมีภาระค่าใช้จ่ายสูง\n3. มีความตั้งใจศึกษาเล่าเรียน',
            'requirements_en': '1. 1st year PSU Phuket undergraduates\n2. High family dependency ratio\n3. Committed academic enthusiasm',
            'amount_per_semester': 7000.00,
            'capacity': 35,
            'start_date': today - timedelta(days=16),
            'end_date': today + timedelta(days=8),
            'status': 'active',
        },
        {
            'title': 'ทุนอาหารกลางวันและน้ำดื่มสะอาดเพื่อสุขอนามัยนักศึกษา (Campus Healthy Dining)',
            'title_en': 'Healthy Campus Nutrition and Hydration Allowance',
            'category': 'lunch',
            'description': 'ทุนสนับสนุนอาหารสุขภาพและสวัสดิการน้ำดื่มสะอาดในวิทยาเขตภูเก็ตสำหรับนักศึกษาที่มีความจำเป็น',
            'description_en': 'Nutritional wellness allowance providing wholesome cafeteria meals and hydration support.',
            'requirements': '1. นักศึกษาปริญญาตรีทุกชั้นปี\n2. GPAX ไม่ต่ำกว่า 2.00\n3. มีความต้องการการสนับสนุนอาหารเพื่อสุขภาพ',
            'requirements_en': '1. All undergraduate students\n2. GPAX >= 2.00\n3. Expressed nutritional assistance requirement',
            'amount_per_semester': 5500.00,
            'capacity': 30,
            'start_date': today - timedelta(days=20),
            'end_date': today + timedelta(days=15),
            'status': 'active',
        },
        {
            'title': 'ทุนสวัสดิการอาหารมื้อกลางวันและเย็นสำหรับนักศึกษาฝึกงานและปฏิบัติงานในวิทยาเขต',
            'title_en': 'Campus Work-Study & Intern Meal Welfare Allowance',
            'category': 'lunch',
            'description': 'ทุนค่าอาหาร 2 มื้อ (กลางวันและเย็น) สำหรับนักศึกษาที่ช่วยปฏิบัติงานในห้องปฏิบัติการ ศูนย์คอมพิวเตอร์ หรือสำนักงานในวิทยาเขต',
            'description_en': 'Double meal allowance (lunch & dinner) for students engaged in campus laboratory and office work-study programs.',
            'requirements': '1. นักศึกษาที่ช่วยงานหน่วยงานในวิทยาเขตตั้งแต่ 20 ชั่วโมง/เดือน\n2. GPAX ไม่ต่ำกว่า 2.30',
            'requirements_en': '1. Minimum 20 hours/month on-campus work-study commitment\n2. GPAX >= 2.30',
            'amount_per_semester': 9000.00,
            'capacity': 20,
            'start_date': today - timedelta(days=15),
            'end_date': today + timedelta(days=27),
            'status': 'active',
        },
        {
            'title': 'ทุนอาหารกลางวันมูลนิธิมิตรภาพอันดามันเพื่อนักศึกษา ม.อ. ภูเก็ต',
            'title_en': 'Andaman Friendship Foundation Campus Dining Fellowship',
            'category': 'lunch',
            'description': 'ทุนสนับสนุนอาหารกลางวันจากผู้มีจิตศรัทธาในเครือข่ายอันดามัน มอบให้นักศึกษาที่ตั้งใจเรียนแต่ขาดแคลน',
            'description_en': 'Community-endowed lunch fellowship assisting underprivileged students with consistent campus meal funds.',
            'requirements': '1. นักศึกษาทุกคณะและสาขาวิชา\n2. GPAX 2.20 ขึ้นไป\n3. ประพฤติดี ไม่เคยมีประวัติด้านลบทางวินัย',
            'requirements_en': '1. All faculties and majors\n2. GPAX >= 2.20\n3. Exemplary personal conduct',
            'amount_per_semester': 7500.00,
            'capacity': 25,
            'start_date': today - timedelta(days=25),
            'end_date': today + timedelta(days=42),
            'status': 'active',
        },
        {
            'title': 'ทุนคูปองอาหารกลางวันโครงการแบ่งปันน้ำใจเพื่อน้อง ภาคเรียนปัจจุบัน',
            'title_en': 'Shared Kindness Student Meal Coupon Fund',
            'category': 'lunch',
            'description': 'ทุนคูปองอาหารกลางวันสนับสนุนโดยกองทุนพัฒนานักศึกษา ม.อ. ภูเก็ต เพื่อแบ่งเบาภาระค่าครองชีพในชีวิตประจำวัน',
            'description_en': 'Semester-round dining coupon allocation supported by the Student Development Fund.',
            'requirements': '1. นักศึกษาปริญญาตรีทุกชั้นปี\n2. มีความจำเป็นด้านค่าอาหารกลางวัน\n3. ได้รับการรับรองจากอาจารย์ที่ปรึกษา',
            'requirements_en': '1. All undergraduate cohorts\n2. Certified lunch funding need\n3. Academic advisor endorsement note',
            'amount_per_semester': 6000.00,
            'capacity': 35,
            'start_date': today - timedelta(days=30),
            'end_date': today + timedelta(days=65),
            'status': 'active',
        },
    ]

    # Automatically purge / delete any expired scholarships (end_date < today)
    expired_del, _ = Scholarship.objects.filter(end_date__lt=today).delete()
    if expired_del:
        print(f"🧹 Automatically deleted {expired_del} expired scholarship(s) from database.")

    scholarships = []
    for spec in scholarships_specs:
        s, _ = Scholarship.objects.update_or_create(
            title=spec['title'],
            defaults={
                'title_en': spec.get('title_en', spec['title']),
                'category': spec['category'],
                'description': spec['description'],
                'description_en': spec.get('description_en', spec['description']),
                'requirements': spec['requirements'],
                'requirements_en': spec.get('requirements_en', spec['requirements']),
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
