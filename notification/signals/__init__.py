from django.dispatch import Signal

user_registered = Signal()
reset_password_request = Signal()
order_created = Signal()
order_status_changed = Signal()
