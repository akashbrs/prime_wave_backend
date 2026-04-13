import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('full_name')
            email = data.get('email')
            message = data.get('message')

            if not full_name or not email or not message:
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Send automated confirmation email to the person who submitted the form
            subject = 'Thank you for getting in touch with PrimeWave'
            
            # Plain text fallback
            body = f'Hi {full_name},\n\nThank you for reaching out. We have received your inquiry and will get back to you shortly.\n\nYour message:\n"{message}"\n\nBest regards,\nPrimeWave Team'
            
            # Rich HTML Email Content matching the screenshot
            html_content = f"""
            <div style="font-family: sans-serif; color: #444; max-width: 600px; margin: 0 auto; line-height: 1.6;">
                <h2 style="color: #4fc3f7; margin-bottom: 24px;">Hello {full_name},</h2>
                <p>Thank you for getting in touch with <strong>PrimeWave Lifestyle & Electronics</strong>.</p>
                <p>This is an automated confirmation that we've successfully received your inquiry. Our team will contact within 48hrs.</p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <p><strong>Here is a summary of your message:</strong></p>
                <div style="background: #f8f9fa; border-left: 4px solid #4fc3f7; padding: 20px; font-style: italic; color: #555; margin: 20px 0;">
                   "{message}"
                </div>
                
                <p style="margin-top: 40px;">Best Regards,</p>
                <p style="margin-bottom: 0;"><strong>PrimeWave Team</strong></p>
                <a href="mailto:primewavelifestyle@gmail.com" style="color: #ff8a65; text-decoration: none;">primewavelifestyle@gmail.com</a>
            </div>
            """
            
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=html_content,
            )

            return JsonResponse({'message': 'Confirmation email sent!'}, status=200)

        except Exception as e:
            print(f"Error in contact_view: {str(e)}")
            return JsonResponse({'error': f'Failed to send email: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
