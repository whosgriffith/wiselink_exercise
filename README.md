# Ejercicio Practico - Wiselink 

### Built with

![](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)


### Requirements
- Postgres or MySQL
- Python 3+
### How to run locally
1- Create a Postgres or MySQL db database.

2- Update the `settings.py` located in the `./wiselink_exercise/` folder (line 109)

(Use the engine `django.db.backends.mysql` for MySQL)

3- While located on the root folder run:

`python manage.py makemigrations`

`python manage.py migrate`

5- Create superuser

`python manage.py createsuperuser`

5- Run server

`python manage.py runserver`

## Users

#### Create users
```http
POST /users/signup/
```

| Form Keys                                             |
|-------------------------------------------------------|
| username                                              |
| email                                                 |
| password                                              |
| password_confirmation                                 |
| first_name                                            |
| last_name                                             |
| organization_name (Default to first_name + last_name) |


#### Login user
```http
POST /users/login/
```
The response will contain the user information and the token for authentication, as following:

```
{
    "user": {
        "username": "Nicolas",
        "organization_name": "Nicolas Repetto",
        "email": "nicolas@email.com",
        "first_name": "Nicolas",
        "last_name": "Repetto",
        "is_staff": false,
        "is_superuser": true,
        "is_active": true
    },
    "token": "afb77af711d75bf188e500a826f7f5a1f6ca9708"
}
```

| Form Keys |
| ------------ |
| username |
| password |


#### Retrieve user
```http
GET /users/<username>/
```
This will retrieve the user information, as following:

```
{
    "user": {
        "username": "root",
        "organization_name": Wiselink,
        "email": "root@root.com",
        "first_name": "Nicolas",
        "last_name": "Repetto",
        "is_staff": true,
        "is_superuser": true,
        "is_active": true
    }
}
```

Only the account owner will have authorization to retrieve the user information.

| Headers       | Value           |
|---------------|-----------------|
| Authorization | token < token > |

#### List users
```http
GET /users/
```
This will get a list of all the users, this endpoint is only accessible for admins.

```
[
    {
        "username": "root",
        "organization_name": Wiselink,
        "email": "root@root.com",
        "first_name": "Nicolas",
        "last_name": "Repetto",
        "is_staff": true,
        "is_superuser": true,
        "is_active": true
    }
	...
]
```

#### Delete user
```http
DELETE /users/<username>/
```

This will deactivate the user, it will not be deleted from the database.

| Headers | Value           |
| ------------ |-----------------|
| Authorization | token < token > |

## Events
#### Create event
```http
POST /events/
```
This request will create an event, and return it.
Only admins can create events.
Events can't be created with a time window smaller than 2 hours before beginning.

| Headers       | Value           |
|---------------|-----------------|
| Authorization | token < token > |

| Form Keys         |
|-------------------|
| title             |
| short_description |
| long_description  |
| date_time         |
| location          |
| status            |

#### Retrieve event
```http
GET /events/<id>/
```
This will retrieve the event information, as following:
```
{
    "event": {
        "organizer": "root",
        "title": "Super Event",
        "short_description": "This is a super short description",
        "long_description": "This description is a super longer description",
        "date_time": null,
        "location": "TBD",
        "status": "draft"
    }
}
```
Only admins can retrieve an Event.

| Headers       | Value           |
|---------------|-----------------|
| Authorization | token < token > |

#### List events
```http
GET /events/
```
This will get a list of all the events, filters can be applied as query strings.

```
[
    {
        "organizer": "root",
        "title": "Super Event",
        "short_description": "This is a short description",
        "long_description": "This is a long description",
        "date_time": "2024-09-29T23:48:00",
        "location": "TBD",
        "status": "active"
    },
	...
]
```

For filtering the following parameters can be applied

| Filter by      | Value                      |
|----------------|----------------------------|
| title          | < title >                  |
| event_datetime | <yy-mm-ddTh:m>             |
| status         | draft / active / cancelled |
| ordering       | (-) < field >              |
| only_active    | *Not necessary*            |

#### Update event
```http
PATCH /events/<id>/
```
Only admins can update events, no matter which admin created the event.

| Headers       | Value           |
|---------------|-----------------|
| Authorization | token < token > |

| Form Keys         |
|-------------------|
| title             |
| short_description |
| long_description  |
| date_time         |
| location          |
| status            |

#### Delete event
```http
DELETE /events/<id>/
```

Only admins can delete events.

| Headers       | Value           |
|---------------|-----------------|
| Authorization | token < token > |


#### Registration for an event
```http
GET /events/<id>/register/
```

Only active events, with date_time in the future are open to inscriptions (inscriptions are closed 1 hour before the event starts).

| Headers       | Value           |
|---------------|-----------------|
| Authorization | token < token > |

#### Retrieve event participants
```http
GET /events/<id>/participants/
```

Only admins can access to the list of participants of the events.

| Headers       | Value           |
|---------------|-----------------|
| Authorization | token < token > |