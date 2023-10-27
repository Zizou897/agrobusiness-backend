from datetime import datetime, timedelta
import uuid


def calculDeliveryDateByNumberOfDays(numberOfDays: int):
    return datetime.now() + timedelta(days=numberOfDays)


def generate_product_order_reference():
    return f'PO-{uuid.uuid4().hex[:6].upper()}'