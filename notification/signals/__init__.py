from django.dispatch import Signal

user_registered = Signal()
reset_password_request = Signal()
order_status_changed = Signal()

# Order signals
order_created = Signal()
order_confirmed = Signal()
order_canceled = Signal()
order_delivered = Signal()
order_ready_to_deliver = Signal()
