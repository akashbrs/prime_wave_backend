import os
import django
from django.core.mail import send_mail
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    print("Attempting to send test email...")
    sent = send_mail(
        'Test Email from PrimeWave',
        'Hi! This is a test email sent from your new Django backend.',
        settings.DEFAULT_FROM_EMAIL,
        ['primewavelifestyle@gmail.com'],
        fail_silently=False,
    )
    if sent:
        print("Success! Email sent successfully.")
    else:
        print("Error: Email was not sent.")
except Exception as e:
    print(f"Error: {e}")
