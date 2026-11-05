from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0004_favoritescholarship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending (รอตรวจสอบ)'),
                    ('in_progress', 'In Progress (กำลังดำเนินการ)'),
                    ('interview', 'Interview (รอสัมภาษณ์)'),
                    ('approved', 'Approve (อนุมัติ)'),
                    ('rejected', 'Reject (ไม่อนุมัติ)'),
                    ('completed', 'Complete (เสร็จสิ้น)'),
                    ('cancelled', 'Cancel (ยกเลิก)'),
                ],
                default='pending',
                max_length=20,
            ),
        ),
    ]

