class SendNotificationOrderDeliveredUseCase:
    def __init__(self, order_id):
        self.order_id = order_id

    def execute(self):
        # Send notification to buyer
        pass
