from firebase_admin.messaging import Message, Notification


class PushNotificationDataBuilder:
    def __init__(self):
        self.title = None
        self.body = None
        self.data = None
        self.topic = None
        self.token = None

    def set_title(self, title):
        self.title = title
        return self

    def set_body(self, body):
        self.body = body
        return self

    def set_data(self, data):
        self.data = data
        return self

    def set_topic(self, topic):
        self.topic = topic
        return self

    def set_token(self, token):
        self.token = token
        return self

    def build(self) -> Message:
        if self.title is None or self.body is None:
            raise ValueError("Title and body are required for notification")

        message = Message(notification=Notification(title=self.title, body=self.body))
        if self.data:
            message.data = self.data
        if self.topic:
            message.topic = self.topic
        if self.token:
            message.token = self.token

        return message
