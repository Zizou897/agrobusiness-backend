from notification.utils.send_notification import Notification
from typing import Union, List
from templated_mail.mail import BaseEmailMessage


class SendEmailNotification(Notification):
    def send(self, **kwargs):
        context: dict[str, Union[str, int]] = kwargs.get('context')
        template_name = kwargs.get('template_name')
        to: List[str] = kwargs.get('to')

        html_message = BaseEmailMessage(
            template_name=template_name + '.html',
            context=context,
        )
        return html_message.send(to=to)
