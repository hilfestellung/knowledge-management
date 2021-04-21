import datetime
from hashlib import sha256
from uuid import uuid4

import jwt
from flask import Blueprint, jsonify
from flask_restful import reqparse, fields, marshal, abort

from km.utls import datetime_to_unixtimestamp, protect_resource

_is_testing = False
_test_now = None
_test_refresh_token = str(uuid4())


def now_():
    if _is_testing:
        return _test_now
    return datetime.datetime.utcnow()


def create_refresh_token():
    if _is_testing:
        return _test_refresh_token
    return str(uuid4())


expiration_timespan = datetime.timedelta(minutes=120)
token_expiration_timespan = datetime.timedelta(days=2)

bp = Blueprint('authentication', __name__, url_prefix='/authentication')

create_register_request_args = reqparse.RequestParser()
create_register_request_args.add_argument('email', type=str, required=True)
create_register_request_args.add_argument('password', type=str, required=True)
create_register_request_args.add_argument('firstName', type=str, required=True)
create_register_request_args.add_argument('lastName', type=str, required=True)

create_login_request_args = reqparse.RequestParser()
create_login_request_args.add_argument('email', type=str, nullable=True)
create_login_request_args.add_argument('password', type=str, nullable=True)

create_refresh_request_args = reqparse.RequestParser()
create_refresh_request_args.add_argument('token', type=str, nullable=True)

user_fields = {
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
}


def generate_token(user) -> tuple:
    from flask import request, current_app
    from km.database import get_db
    from km.model import Authentication

    now = now_()
    expires = now + expiration_timespan
    refresh_token = create_refresh_token()
    auth = Authentication(email=user.email, ip_address=request.remote_addr, refresh_token=refresh_token,
                          success=True, expires=expires)
    print(f"\nNew {now}+{expiration_timespan} = {expires}", flush=True)
    db = get_db()
    db.session.add(auth)
    db.session.commit()

    return (jwt.encode(
        {'sub': user.email, 'exp': expires, 'aud': current_app.config['JWT_AUDIENCE'], 'iat': now,
         'permissions': user.permissions},
        current_app.config['PRIVATE_KEY'],
        algorithm='RS256'), refresh_token, expires)


def can_pass(condition, email, failure_message, failure_code=400):
    if condition():
        from flask import request
        from km.database import get_db
        from km.model import Authentication
        db = get_db()
        authentication = Authentication(email=email, ip_address=request.remote_addr, message=failure_message)
        db.session.add(authentication)
        db.session.commit()
        abort(failure_code, message=failure_message)


@bp.route('/register', methods=['PUT'])
def register():
    from km.database import get_db
    from km.model import User
    from km.model.user import fetch_user_group

    args = create_register_request_args.parse_args()
    hash_ = sha256()
    hash_.update(args['password'].encode('utf-8'))
    user = User(email=args['email'], password=hash_.hexdigest(), first_name=args['firstName'],
                last_name=args['lastName'])
    user.groups.append(fetch_user_group('User'))
    db = get_db()
    db.session.add(user)
    db.session.commit()

    return marshal(user, user_fields), 201


@bp.route('/login', methods=['PUT'])
def login():
    from km.model import User
    from km.database import get_db
    db = get_db()
    args = create_login_request_args.parse_args()
    if not args['email']:
        abort(401, message='Missing email.')
    can_pass(lambda: not args['password'], args['email'], 'Missing password', 401)

    password = sha256()
    password.update(args['password'].encode('utf-8'))

    user = User.query.filter_by(email=args['email'], password=password.hexdigest()).first()
    can_pass(lambda: not user, args['email'], 'E-Mail or password is wrong.', 401)

    token, refresh_token, expires = generate_token(user)

    return jsonify(
        {"access_token": token, 'refresh_token': refresh_token, "expires_at": datetime_to_unixtimestamp(expires)}), 200


@bp.route('/refresh', methods=['PUT'])
@protect_resource()
def refresh():
    from flask import request
    from km.model import Authentication, User

    if not hasattr(request, 'user') or not request.user:
        abort(401, message='Missing user')
    user = User.query.filter_by(email=request.user.get('sub')).first()
    args = create_refresh_request_args.parse_args()
    can_pass(lambda: not args['token'], user.email, 'Missing token', 401)

    authentication = Authentication.query.filter_by(email=user.email, refresh_token=args['token'],
                                                    success=True).order_by(
        Authentication.created_at.desc()).first()
    can_pass(lambda: not authentication, user.email, 'Invalid token', 401)

    can_pass(lambda: authentication.expires + token_expiration_timespan < now_(), user.email, 'Token expired', 401)

    token, refresh_token, expires = generate_token(user)

    return jsonify(
        {"access_token": token, 'refresh_token': refresh_token, "expires_at": datetime_to_unixtimestamp(expires)}), 200
