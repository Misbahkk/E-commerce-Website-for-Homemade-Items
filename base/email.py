
from django.conf import settings
from django.core.mail import send_mail


def send_accout_activatio_email(email,email_token):
    try:
        subject = 'your ACoount need to be verofied '
        email_form = settings.EMAIL_HOST_USER
        message = f"Hi Click the link to activate your account https://e-commerce-website-for-homemade-production.up.railway.app/account/activate/{email_token}/"
        send_mail(subject, message,email_form,[email],fail_silently=False)
        print("email: ",email)
        print("Email sent successfully!")
    except Exception as e:
        print(e)
