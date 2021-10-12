import datetime
from decimal import Decimal
from enum import Enum, IntEnum
from typing import Optional
from pydantic import BaseModel


class ServingPeriodEnum(str, Enum):
    BREAKFAST: str = 'Breakfast',
    LUNCH: str = 'Lunch',
    DINNER: str = 'Dinner'


class ReservationSchema(BaseModel):
    number_of_seat_adults: Optional[int]
    number_of_seat_children: Optional[int]
    serving_period: ServingPeriodEnum
    deposit: Optional[bool]
    additional_info: Optional[str]
    is_complete: Optional[bool]
    cancel_reservation: Optional[bool]
    arrival_date: Optional[str]
    # arrival_date: datetime.date


class UpdateReservationSchema(BaseModel):
    number_of_seat_adults: Optional[int]
    number_of_seat_children: Optional[int]
    serving_period: ServingPeriodEnum
    deposit: Optional[bool]
    additional_info: Optional[str]
    cancel_reservation: Optional[bool]
    arrival_date: Optional[str]


class UpdateReservationIsCompleteSchema(BaseModel):
    is_complete: Optional[bool]
