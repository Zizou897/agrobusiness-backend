from django.core.mail import send_mail
from jinja2 import Template
from core import settings


class SendMailAlertPaymentUseCase:
    @staticmethod
    def execute(**kwargs):
        parent_email = kwargs.get('parent_email')
        parent_name = kwargs.get('parent_first_name')
        date_payment = kwargs.get('date_payment')
        amount = kwargs.get('amount')
        student_name = kwargs.get('student_name')
        message = kwargs.get('message')

        template = Template(message)
        mail = template.render(
            PARENT_NAME=parent_name,
            DATE_PAYMENT=date_payment,
            MONTANT=amount,
            STUDENT_NAME=student_name
        )

        subject = 'Alerte de paiement'

        send_mail(
            subject=subject,
            message=mail,
            html_message=mail,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[parent_email],
            fail_silently=False,
        )
