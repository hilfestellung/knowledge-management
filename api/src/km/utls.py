import traceback
from datetime import date, datetime
from typing import Optional

import jwt
from flask_restful import abort


def date_to_datetime(date_: date, hour: Optional[int] = 0, minute: Optional[int] = 0,
                     second: Optional[int] = 0) -> datetime:
    return datetime(date_.year, date_.month, date_.day, hour, minute, second)


epoch = datetime.utcfromtimestamp(0)


def date_to_unixtimestamp(date_: date):
    return int((date_to_datetime(date_) - epoch).total_seconds() * 1000.0)


def datetime_to_unixtimestamp(datetime_: datetime):
    return int((datetime_ - epoch).total_seconds() * 1000.0)


AUTHORIZATION_PREFIX = 'Bearer '
AUTHORIZATION_PREFIX_LENGTH = len(AUTHORIZATION_PREFIX)


def has_permissions(user: dict, permissions: set):
    user_permissions = set(user.get('permissions', []))
    print(user_permissions, permissions, flush=True)
    return permissions <= user_permissions


def protect_resource(permissions: list = None):
    if isinstance(permissions, list):
        permission_set = set(permissions)
    else:
        permission_set = None

    def wrap(f):
        def decorated(*args, **kwargs):
            from flask import current_app, request
            from flask_restful import abort

            authorization = request.headers.get('authorization')
            if not authorization or not authorization.startswith(AUTHORIZATION_PREFIX):
                return abort(401, error='Unauthorized', message='You are not authorized.')
            token = authorization[AUTHORIZATION_PREFIX_LENGTH:]
            try:
                user = jwt.decode(token, current_app.config['PUBLIC_KEY'], verify=True,
                                  audience=current_app.config['JWT_AUDIENCE'], algorithms=['RS256'])
            except Exception:
                traceback.print_exc()
                return abort(401, error='InvalidToken', message='The provided token is invalid.')
            if permission_set and not has_permissions(user, permission_set):
                return abort(403, error='Forbidden', message='You are not authorized to this resource.')
            setattr(request, 'user', user)

            return f(*args, **kwargs)

        return decorated

    return wrap
