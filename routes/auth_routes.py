from typing import List
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi_jwt_auth.auth_jwt import AuthJWT
from werkzeug.security import generate_password_hash, check_password_hash
from schemas.user_schemas import EditUserSchema, LoginSchema, RegisterUserSchema, UserSchema
from models.models import User, User_Pydantic

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@auth_router.get('/')
async def root():
    return {"message": "Hello World, welcomw to our Restaurant"}


@auth_router.post('/register', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: RegisterUserSchema):
    """Create New user

    Args:
        user (RegisterUserSchema): Required pydantic fields to create a new user.
    Raises:
        HTTPException: User with that Username  already exists
        HTTPException: User with that Phone number already exists
        HTTPException: User with that Email already exists

    Returns:
        json: json object of user information
    """

    # Check Username
    username = await User.get_or_none(username=user.username)
    if username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with that Username  already exists')
    # Check User phone
    user_phone = await User.get_or_none(phone=user.phone)
    if user_phone is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with that Phone number already exists')
    # Check User Email
    user_email = await User.get_or_none(email=user.email)
    if user_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with that Email already exists')

    user = await User.create(
        title=user.title,
        username=user.username,
        full_name=user.full_name,
        phone=user.phone,
        email=user.email,
        password=generate_password_hash(user.password)
    )
    await user.save()
    return user


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginSchema, Authorize: AuthJWT = Depends()):
    """Login

    Args:
        user (LoginSchema): fields to login a user(username and password)
        Authorize (AuthJWT, optional): Login required. Defaults to Depends().

    Raises:
        HTTPException: Invalid Username or Password if either of them is incorrect.

    Returns:
        str: token, login successful
    """
    db_user = await User.get(username=user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.email)
        refresh_token = Authorize.create_refresh_token(db_user.email)
        reponse = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Login successful!"
        }
        return jsonable_encoder(reponse)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Invalid Username or Password')


@auth_router.get('/users', response_model=List[UserSchema])
async def list_users():
    """All users

    Returns:
        List: Return a list of registered users
    """
    users = await User_Pydantic.from_queryset(User.all().order_by('-created_at'))
    return users


@auth_router.get('/users/{user_id}', response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_user(user_id: str,):
    """Get single user by user id.

    Args:
        user_id (str): User id.

    Returns:
        json: json object of a single user details
    """
    user = await User_Pydantic.from_queryset_single(User.get(id=user_id))
    return user


@auth_router.put('/users/{user_id}', response_model=UserSchema, status_code=status.HTTP_200_OK)
async def edit_user(user_id: str, user: EditUserSchema):
    """Update User

    Args:
        user_id (str): Update the user with the given id
        user (EditUserSchema): The allowable fields to be updated by the user

    Returns:
        json: json object of the updated user details
    """
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@auth_router.delete('/users/{user_id}')
async def delete_user(user_id: str):
    """Delete a user

    Args:
        user_id (str): Delete a user with the given id

    Raises:
        HTTPException: [description]

    Returns:
        str: The user with the given not found
    """
    user = await User.filter(id=user_id).delete()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User {user_id} not found")
    return {"message": f'User with ID {user_id} deleted successfully!'}
