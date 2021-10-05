# Resturant Reservation App

### Endpoints Functionality of the application.

| METHODS | ROUTES                               | FUNCTIONALITY             | ACCESS                |
| ------- | ------------------------------------ | ------------------------- | --------------------- |
| POST    | /auth/register                       | Register new user         | All users             |
| POST    | /auth/login                          | Login user                | All users             |
| GET     | /auth/users                          | List all users            | Admin Users           |
| POST    | /reservations/make_reservation       | Make Reservation          | All users             |
| GET     | /reservations                        | List all Reservation      | Staff and Admin Users |
| GET     | /reservations/user_reservations      | List user Reservations    | Logged in user        |
| GET     | /reservations/reservation_details/id | Reservation details       | Staff and Admin Users |
| PUT     | /reservations/update_reservation/id  | Update Reservation        | All users             |
| PUT     | /reservations/update_reservation/id  | Update Reservation status | Admin Users           |
| DELETE  | /reservations/update_reservation/id  | Delete Reservation        | Admin Users           |
