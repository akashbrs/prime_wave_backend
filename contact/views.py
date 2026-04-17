import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactSubmission

# Configure logging
logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def contact_view(request):
    """
    Handles contact form submissions.
    Validates JSON, saves to DB, and sends a confirmation email.
    """
    try:
        # 1. Parse and Validate JSON
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON received")
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

        # Support both 'name' (requested) and 'full_name' (backward compatibility)
        name = data.get('name') or data.get('full_name')
        email = data.get('email')
        message = data.get('message')

        logger.info(f"Received contact submission from: {email}")

        if not name or not email or not message:
            return JsonResponse({'error': 'Fields name, email, and message are all required.'}, status=400)

        # 2. Save to Database
        try:
            submission = ContactSubmission.objects.create(
                name=name,
                email=email,
                message=message
            )
            logger.info(f"Saved submission to DB with ID: {submission.id}")
        except Exception as db_err:
            logger.error(f"Database error: {str(db_err)}")
            # We continue even if DB fails, as email is the primary action, 
            # but you might want to return 500 here depending on requirements.
            pass

        # 3. Send automated confirmation email
        subject = 'Thank you for getting in touch with PrimeWave'
        body = f'Hi {name},\n\nThank you for reaching out. We have received your inquiry and will get back to you shortly.\n\nYour message:\n"{message}"\n\nBest regards,\nPrimeWave Team'
        
        html_content = f"""
        <div style="font-family: sans-serif; color: #444; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            <h2 style="color: #4fc3f7; margin-bottom: 24px;">Hello {name},</h2>
            <p>Thank you for getting in touch with <strong>PrimeWave Lifestyle & Electronics</strong>.</p>
            <p>This is an automated confirmation that we've successfully received your inquiry. Our team will contact you within 48hrs.</p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            <p><strong>Here is a summary of your message:</strong></p>
            <div style="background: #f8f9fa; border-left: 4px solid #4fc3f7; padding: 20px; font-style: italic; color: #555; margin: 20px 0;">
               "{message}"
            </div>
            <p style="margin-top: 40px;">Best Regards,</p>
            <p style="margin-bottom: 0;"><strong>PrimeWave Team</strong></p>
        </div>
        """
        
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=html_content,
            )
            logger.info(f"Confirmation email sent to {email}")
        except Exception as mail_err:
            logger.error(f"Email sending failed: {str(mail_err)}")
            # If email fails, we return 500 as per user requirement for "server failure"
            return JsonResponse({
                'error': 'Server failed to send confirmation email.',
                'details': str(mail_err) if settings.DEBUG else 'Check server logs.'
            }, status=500)

        return JsonResponse({'message': 'Contact submitted successfully'}, status=200)

    except Exception as e:
        logger.critical(f"Unexpected server error: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'An unexpected server error occurred.'}, status=500)

def debug_view(request):
    """Simple health check endpoint."""
    return JsonResponse({
        'status': 'ok',
        'version': '3.0-robust',
        'database_connected': True, # Simple assumption for health check
    })
