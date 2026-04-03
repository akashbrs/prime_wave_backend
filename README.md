# PrimeWave Contact Backend

A Django-based backend to handle contact form submissions with automated email responses using Google SMTP and environment variables for configuration.

## Features
- **Automation Email**: Sends a confirmation email to the person who submitted the form.
- **Environment Variables**: Sensitive configuration handled via `.env` file.
- **CORS Support**: Ready to be integrated with modern frontend frameworks.

## Setup Instructions

### 1. Configure the Environment
- Rename `.env.example` to `.env`.
- Fill in your Google SMTP details.

**How to get a Google App Password?**
1.  Go to your [Google Account Settings](https://myaccount.google.com/).
2.  Enabled **2-Step Verification**.
3.  Search for **"App Passwords"** in the search bar.
4.  Create a new app (e.g., "Contact Form Backend").
5.  Copy the 16-character password and paste it into `EMAIL_HOST_PASSWORD` in your `.env`.

### 2. Install Dependencies
```bash
pip install Django python-dotenv django-cors-headers
```

### 3. Run Migrations (Optional)
```bash
python manage.py migrate
```

### 4. Start the Server
```bash
python manage.py runserver 8005
```

## API Endpoint
**URL**: `http://127.0.0.1:8005/api/contact/`  
**Method**: `POST`  
**Body (JSON)**:
```json
{
    "full_name": "John Doe",
    "email": "john@example.com",
    "message": "Hello, how can we help you?"
}
```
