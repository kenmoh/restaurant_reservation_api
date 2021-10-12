from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from schemas.reservation_schemas import ServingPeriodEnum
from schemas.user_schemas import TitleEnum


class User(models.Model):
    id = fields.UUIDField(pk=True)
    title: TitleEnum = fields.CharField(max_length=255, default='Mrs')
    username = fields.CharField(max_length=255, unique=True)
    full_name = fields.CharField(max_length=255)
    phone = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    is_admin = fields.BooleanField(default=False, description='Manager')
    is_staff = fields.BooleanField(default=False, description='Supervisor')
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    reservation: fields.ReverseRelation['Reservation']

    class Meta:
        table = 'users'


class Reservation(models.Model):
    reservation_id = fields.UUIDField(pk=True)
    number_of_seat_adults = fields.IntField(
        null=False, default=0, description='Starting from Zero(0)')
    number_of_seat_children = fields.IntField(
        null=False, default=0, description='Starting from Zero(0)')
    serving_period: ServingPeriodEnum = fields.CharField(
        max_length=255, default="Breakfast")
    deposit = fields.BooleanField(default=False)
    additional_info = fields.TextField(null=True, blank=True)
    is_complete = fields.BooleanField(default=False)
    cancel_reservation = fields.BooleanField(default=False)
    arrival_date = fields.CharField(max_length=255)
    date_booked = fields.DatetimeField(auto_now_add=True)
    date_modified = fields.DatetimeField(auto_now=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField('models.User',
                                                                   on_delete=fields.CASCADE, related_name='reservations', to_field='username')

    class Meta:
        table = 'reservations'

    # @property
    # def grand_total(self):
    #     return (self.number_of_seat_adults * self.adult_price) + (self.number_of_seat_children * self.kid_price)


User_Pydantic = pydantic_model_creator(User, name='User')
Reservation_Pydantic = pydantic_model_creator(
    Reservation, name='Reservation', exclude=('date_booked',))
