import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address
from email.utils import parseaddr


class BrevoEmailBackend(BaseEmailBackend):
    """
    Django email backend that sends via Brevo's HTTPS API (port 443).
    Needed because Render's free tier blocks outbound SMTP ports (25/465/587).
    Requires env var BREVO_API_KEY and a verified sender (DEFAULT_FROM_EMAIL).
    """
    API_URL = 'https://api.brevo.com/v3/smtp/email'

    def send_messages(self, email_messages):
        sent = 0
        for message in email_messages:
            try:
                if self._send(message):
                    sent += 1
            except Exception:
                if not self.fail_silently:
                    raise
        return sent

    def _send(self, message):
        if not message.recipients():
            return False

        raw_from = message.from_email or getattr(settings, 'DEFAULT_FROM_EMAIL', '')
        name, addr = parseaddr(raw_from)
        if not name:
            name = getattr(settings, 'DEFAULT_FROM_NAME', 'PSU Phuket Scholarships')

        payload = {
            'sender': {'email': addr, 'name': name},
            'to': [{'email': r} for r in message.to],
            'subject': message.subject,
        }
        if message.cc:
            payload['cc'] = [{'email': r} for r in message.cc]
        if message.bcc:
            payload['bcc'] = [{'email': r} for r in message.bcc]

        html = None
        for content, mimetype in getattr(message, 'alternatives', []):
            if mimetype == 'text/html':
                html = content
        if html:
            payload['htmlContent'] = html
            payload['textContent'] = message.body
        else:
            payload['textContent'] = message.body

        resp = requests.post(
            self.API_URL,
            json=payload,
            headers={
                'api-key': settings.BREVO_API_KEY,
                'accept': 'application/json',
                'content-type': 'application/json',
            },
            timeout=10,
        )
        if resp.status_code >= 400:
            raise RuntimeError(f'Brevo API error {resp.status_code}: {resp.text[:300]}')
        return True
