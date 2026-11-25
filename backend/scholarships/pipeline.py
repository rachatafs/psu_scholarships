from social_core.exceptions import AuthForbidden
from django.contrib.auth.models import User
from scholarships.models import StudentProfile, Application, FavoriteScholarship


def check_email_domain(backend, details, uid, user=None, *args, **kwargs):
    """
    Custom pipeline to restrict login to:
    1. Emails ending with @phuket.psu.ac.th
    """
    email = details.get('email', '')
    if not email:
        raise AuthForbidden(backend)

    if email.lower().endswith('@phuket.psu.ac.th'):
        return

    raise AuthForbidden(backend)


def associate_by_email_or_student_id(backend, details, user=None, *args, **kwargs):
    """
    Associate Google login with an existing User if one already exists
    with the same email or username (e.g. seeded s6630613014 or rachata).
    Prevents Python Social Auth from appending random UUID hashes!
    """
    if user:
        return {'user': user}

    email = details.get('email', '').strip().lower()
    if not email:
        return None

    prefix = email.split('@')[0] if '@' in email else ''

    # 1. Try finding by email
    existing = User.objects.filter(email__iexact=email).first()

    # 2. Try finding by username prefix (e.g. 's6630613014' or 'rachata')
    if not existing and prefix:
        existing = User.objects.filter(username__iexact=prefix).first()

    # 3. Try finding any previously hashed username for this student
    if not existing and prefix:
        existing = User.objects.filter(username__istartswith=prefix).first()

    if existing:
        return {'user': existing, 'is_new': False}

    return None


def setup_user_and_profile(backend, details, user=None, is_new=False, *args, **kwargs):
    """
    Ensures:
    1. Username is clean without UUID hash (e.g. s6630613014 instead of s6630613014db1ea...)
    2. StudentProfile exists with student_id and full_name
    3. Merges any placeholder student profile or applications
    """
    if not user:
        return

    email = details.get('email', '').strip().lower()
    prefix = email.split('@')[0] if '@' in email else user.username

    # Clean up hashed username if needed
    if user.username != prefix and prefix:
        other_user = User.objects.filter(username__iexact=prefix).exclude(pk=user.pk).first()
        if other_user:
            if hasattr(other_user, 'profile'):
                other_profile = other_user.profile
                if not hasattr(user, 'profile'):
                    other_profile.user = user
                    other_profile.save()
                else:
                    Application.objects.filter(student=other_profile).update(student=user.profile)
                    other_profile.delete()

            FavoriteScholarship.objects.filter(user=other_user).update(user=user)
            other_user.delete()

        user.username = prefix
        user.email = email
        user.save()

    # Ensure StudentProfile exists
    profile, _ = StudentProfile.objects.get_or_create(user=user)
    student_id = prefix[1:] if (prefix.startswith('s') and prefix[1:].isdigit()) else prefix
    if not profile.student_id:
        profile.student_id = student_id

    # Populate full_name from Google OAuth if empty
    if not profile.full_name:
        first = details.get('first_name', '').strip()
        last = details.get('last_name', '').strip()
        full = f"{first} {last}".strip()
        if full:
            profile.full_name = full
        elif prefix == 's6630613014':
            profile.full_name = 'รชต ไผ่สังข์ (Rachata Faisang)'

    profile.save()
