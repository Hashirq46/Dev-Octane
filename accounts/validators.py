import os
from django.core.exceptions import ValidationError

FREE_EMAIL_DOMAINS = {
    'gmail.com', 'googlemail.com', 'yahoo.com', 'yahoo.co.uk', 'hotmail.com',
    'outlook.com', 'live.com', 'msn.com', 'icloud.com', 'aol.com', 'proton.me',
    'protonmail.com', 'mail.com', 'gmx.com', 'yandex.com', 'zoho.com', 'rocketmail.com',
}


def validate_office_email(value):
    if not value or '@' not in value:
        raise ValidationError('Enter a valid email address.')
    domain = value.rsplit('@', 1)[-1].lower()
    if domain in FREE_EMAIL_DOMAINS:
        raise ValidationError('Please use your official company email address.')


ALLOWED_EXT = ('.pdf', '.docx', '.jpg', '.jpeg', '.png')
SIGNATURES = {
    '.pdf': b'%PDF',
    '.docx': b'PK',
    '.jpg': b'\xff\xd8',
    '.jpeg': b'\xff\xd8',
    '.png': b'\x89PNG',
}


def validate_upload(f):
    ext = os.path.splitext(f.name.lower())[1]
    if ext not in ALLOWED_EXT:
        raise ValidationError('Allowed file types: PDF, DOCX, JPG, PNG.')
    if f.size > 5 * 1024 * 1024:
        raise ValidationError('File must be under 5 MB.')
    head = f.read(8)
    f.seek(0)
    sig = SIGNATURES.get(ext)
    if not sig or not head.startswith(sig):
        raise ValidationError('File content does not match its extension.')
