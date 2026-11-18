from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


RETURN_WINDOW_DAYS = 30


@dataclass
class Order:
    status: OrderStatus
    delivered_on: Optional[date] = None


def can_return(order: Order, today: date) -> bool:
    if order.status is not OrderStatus.DELIVERED:
        return False
    if order.delivered_on is None:
        return False
    return (today - order.delivered_on).days <= RETURN_WINDOW_DAYS
