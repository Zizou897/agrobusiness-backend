from notification.utils.send_notification import Notification
import environ
from infobip_channels.sms.channel import SMSChannel

env = environ.Env()
environ.Env.read_env()


class SendSMSNotification(Notification):
    def __init__(self, sender: str):
        self.sender = sender
        self.channel = SMSChannel.from_auth_params(
            {"base_url": env.str("BASE_URL"), "api_key": env.str("API_KEY")}
        )

    def send(self, **kwargs):
        to = kwargs.get("to")
        text = kwargs.get("text")
        return self.channel.send_sms_message(
            {
                "messages": [
                    {
                        "from": self.sender,
                        "destinations": [{"to": to}],
                        "text": text,
                    }
                ]
            }
        )

