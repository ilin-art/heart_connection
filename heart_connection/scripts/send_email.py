from django.core.mail import send_mail

def send_notification(to_email, message):
    subject = 'Уведомление приложения "Heart connection"'
    from_email = 'email@heart_connection.com'  # Отправитель (может отличаться от DEFAULT_FROM_EMAIL)
    send_mail(subject, message, from_email, [to_email])
