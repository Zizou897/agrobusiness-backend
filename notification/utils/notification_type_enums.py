from core.base_enum import ExtendedEnum


class NotificationTypeEnum(ExtendedEnum):
    order_created = "order_created"
    order_confirmed = "order_confirmed"
    order_delivered = "order_delivered"
    order_canceled = "order_canceled"
    order_ready_to_deliver = "order_ready_to_deliver"
