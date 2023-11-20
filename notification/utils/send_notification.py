from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, **kwargs):
        pass


class SendNotification:
    def __init__(self, notification: Notification):
        self.notification = notification

    def mail(self, context, template_name, to):
        return self.notification.send(
            context=context, template_name=template_name, to=to
        )

    def sms(self, to: str, text: str):
        return self.notification.send(to=to, text=text)

    def push_notification(self, **kwargs):
        self.notification.send(**kwargs)

    def whatsapp_message(self, **kwargs):
        self.notification.send(**kwargs)
