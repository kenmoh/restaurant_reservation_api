from typing import List, Optional
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi_jwt_auth.auth_jwt import AuthJWT
from starlette.status import HTTP_401_UNAUTHORIZED
from models.models import Reservation, Reservation_Pydantic, User, User_Pydantic

from schemas.reservation_schemas import ReservationSchema, UpdateReservationIsCompleteSchema, UpdateReservationSchema

reservations_router = APIRouter(
    prefix='/reservations',
    tags=['Reservation'],
)


@reservations_router.post('/make_reservation', status_code=status.HTTP_201_CREATED)
async def make_reservation(reservation: ReservationSchema, Authorize: AuthJWT = Depends()):
    """
    This endpoint allows all registered and logged in users to make reservation(s)
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    current_user = Authorize.get_jwt_subject()
    reservations = await Reservation.all()
    if len(reservations) == 15:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="We're fully booked at the moment, please try later.")
    else:
        user = await User.get(email=current_user)
        new_reservation = await Reservation(
            number_of_seat_adults=reservation.number_of_seat_adults,
            number_of_seat_children=reservation.number_of_seat_children,
            serving_period=reservation.serving_period,
            deposit=reservation.deposit,
            additional_info=reservation.additional_info,
            is_complete=reservation.is_complete,
            cancel_reservation=reservation.cancel_reservation,
            arrival_date=reservation.arrival_date,
        )

        new_reservation.user = user
        await new_reservation.save()
        response = {
            "user": user.full_name,
            "reservation": new_reservation,
        }
        return jsonable_encoder(response)


@ reservations_router.get('/')
async def list_reservations(Authorize: AuthJWT = Depends()):
    '''
    This endpoint returns a list of
    all available reservations.
    Only staff or admin users are allowed to access this endpoint.

    '''
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    current_user = Authorize.get_jwt_subject()
    user = await User.get(email=current_user).first()

    if user.is_staff or user.is_admin:
        users_reservation = await Reservation.all().prefetch_related("user")
        response = {
            "total_reservations": len(users_reservation),
            "users_reservation": users_reservation
        }
        return jsonable_encoder(response)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Access denied !')


@ reservations_router.get('/reservation_details/{reservation_id}')
async def reservation_details(reservation_id: str, Authorize: AuthJWT = Depends()):
    '''
    This endpoint returns a single reservation details of a user.
    Only staff or admin users are allowed to access this endpoint.
    '''

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    current_user = Authorize.get_jwt_subject()
    user = await User.get(email=current_user).first()
    print(list(user))

    if user.is_staff or user.is_admin:
        reservation = await Reservation.get(reservation_id=reservation_id)
        return reservation
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Access error!')


@reservations_router.get('/user_reservations')
async def reservation_details(Authorize: AuthJWT = Depends()):
    '''
    This endpoint returns a single reservation details of a current logged in user
    '''

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    current_user = Authorize.get_jwt_subject()
    user = await User.get(email=current_user).first()
    reservations = await Reservation.all().filter(user=user.username)
    response = {
        "number_of_reservations": len(reservations),
        "reservations": reservations,
    }
    return jsonable_encoder(response)


@ reservations_router.put('/update_reservation/{reservation_id}', response_model=Reservation_Pydantic)
async def update_reservations(reservation_id: str, reservation: UpdateReservationSchema, Authorize: AuthJWT = Depends()):
    '''
    Update user reservation.
    Returns an updated reservation.
    Logged in user can update their reservation.
    Admin user can update their reservation or user reservation
    '''
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    current_user = Authorize.get_jwt_subject()
    user = await User.get(email=current_user).first()

    if user or user.is_admin:
        db_reservation = await Reservation.get(reservation_id=reservation_id)
        reservation = reservation.dict(exclude_unset=True)
        db_reservation.number_of_seat_adults = reservation['number_of_seat_adults']
        db_reservation.number_of_seat_children = reservation['number_of_seat_children']
        db_reservation.serving_period = reservation['serving_period']
        db_reservation.deposit = reservation['deposit']
        db_reservation.additional_info = reservation['additional_info']
        db_reservation.cancel_reservation = reservation['cancel_reservation']
        db_reservation.arrival_date = reservation['arrival_date']
        await db_reservation.save()
        return db_reservation
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Access denied !')


@ reservations_router.put('/update_reservation_is_complete/{reservation_id}', response_model=Reservation_Pydantic)
async def update_reservations_is_complete(reservation_id: str, reservation: UpdateReservationIsCompleteSchema, Authorize: AuthJWT = Depends()):
    '''
    This endpoint allows admin user(s) to update the status of a reservation i.e if the reservation is 
    is completed.
    '''
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    current_user = Authorize.get_jwt_subject()
    user = await User.get(email=current_user).first()

    if user.is_staff or user.is_admin:
        db_reservation = await Reservation.get(reservation_id=reservation_id)
        reservation = reservation.dict(exclude_unset=True)
        db_reservation.is_complete = reservation['is_complete']
        await db_reservation.save()
        return db_reservation
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='You are NOT Authorize to carry out this action!')


@ reservations_router.delete('/delete_reservation_is_complete/{reservation_id}')
async def update_reservations(reservation_id: str, Authorize: AuthJWT = Depends()):
    # Delete completed reservation(s)
    # Accessable to users only
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    current_user = Authorize.get_jwt_subject()
    user = await User.get(email=current_user).first()
    reservation = await Reservation.get(reservation_id=reservation_id)

    if user.is_admin and reservation.is_complete:
        db_reservation = await Reservation.get(reservation_id=reservation_id).delete()
        if not db_reservation:
            raise HTTPException(
                status_code=404, detail="Reservation not found")
        return {"message": 'Reservation deleted successfully!'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Access denied or incomplete reservation!')
