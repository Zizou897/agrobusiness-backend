from typing import Union, List
from templated_mail.mail import BaseEmailMessage


class SendNotification:
    @staticmethod
    def send_mail(**kwargs):
        context: dict[str, Union[str, int]] = kwargs.get('context')
        template_name = kwargs.get('template_name')
        to: List[str] = kwargs.get('to')

        # Send mail
        html_message = BaseEmailMessage(
            template_name=template_name + '.html',
            context=context,
        )
        return html_message.send(to=to)

    @staticmethod
    def send_sms(self, **kwargs):
        pass

    @staticmethod
    def send_push_notification(self, **kwargs):
        pass
