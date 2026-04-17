import json
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import ContactSubmission

@csrf_exempt
def contact_view(request):
    if request.method == "POST":
        try:
            # Handle both JSON (React) and Form Data (Curl/Standard)
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                name = data.get("name") or data.get("full_name")
                email = data.get("email")
                message = data.get("message")
            else:
                name = request.POST.get("name") or request.POST.get("full_name")
                email = request.POST.get("email")
                message = request.POST.get("message")

            # Save to Database first (to ensure we don't lose the data)
            try:
                ContactSubmission.objects.create(name=name, email=email, message=message)
            except Exception as db_e:
                print("DATABASE ERROR:", db_e)

            # Try sending email
            try:
                # Use your specific send_mail structure
                send_mail(
                    "New Contact Submission",
                    f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL], # Sending to yourself
                    fail_silently=False,
                )
            except Exception as e:
                print("EMAIL ERROR:", e)   # 👈 this prevents crash

            return JsonResponse({
                "status": "success",
                "message": "Message received successfully"
            })

        except Exception as e:
            print("API ERROR:", e)
            return JsonResponse({
                "status": "error",
                "message": "Something went wrong"
            }, status=500)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

def debug_view(request):
    return JsonResponse({"status": "ok", "version": "4.0-user-custom"})
