from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_password_reset_otp(user, otp_code):
    """
    Send password reset OTP to user's email
    """
    subject = 'Password Reset OTP -  Blog'
    
    html_message = f"""
    <html>
    <body>
        <h2>Password Reset Request</h2>
        <p>Hello {user.first_name or user.username},</p>
        <p>You have requested to reset your password. Use the following OTP to reset your password:</p>
        <h3 style="color: #007bff; font-size: 24px; letter-spacing: 3px;">{otp_code}</h3>
        <p>This OTP will expire in {getattr(settings, 'OTP_EXPIRY_MINUTES', 10)} minutes.</p>
        <p>If you did not request this password reset, please ignore this email.</p>
        <br>
        <p>Best regards,<br>Blog API Team</p>
    </body>
    </html>
    """
    
    plain_message = f"""
    Password Reset Request
    
    Hello {user.first_name or user.username},
    
    You have requested to reset your password. Use the following OTP to reset your password:
    
    {otp_code}
    
    This OTP will expire in {getattr(settings, 'OTP_EXPIRY_MINUTES', 10)} minutes.
    
    If you did not request this password reset, please ignore this email.
    
    Best regards,
     Blog Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
