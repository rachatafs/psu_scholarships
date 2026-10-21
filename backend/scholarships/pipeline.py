from social_core.exceptions import AuthForbidden

def check_email_domain(backend, details, uid, user=None, *args, **kwargs):
    """
    Custom pipeline to restrict login to:
    1. Emails ending with @phuket.psu.ac.th
    """
    email = details.get('email')
    
    if not email:
        raise AuthForbidden(backend)
    
    # Allow ONLY @phuket.psu.ac.th
    if email.endswith('@phuket.psu.ac.th'):
        return
        
    raise AuthForbidden(backend)
