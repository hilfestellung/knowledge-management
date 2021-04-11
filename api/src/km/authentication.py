import datetime
from hashlib import sha256

import jwt
from flask import Blueprint, jsonify
from flask_restful import reqparse, fields, marshal, abort

from km.utls import datetime_to_unixtimestamp

_is_testing = False
_test_now = None


def now_():
    if _is_testing:
        return _test_now
    else:
        return datetime.datetime.utcnow()


expiration_timespan = datetime.timedelta(minutes=120)

bp = Blueprint('authentication', __name__, url_prefix='/authentication')

create_register_request_args = reqparse.RequestParser()
create_register_request_args.add_argument('email', type=str, required=True)
create_register_request_args.add_argument('password', type=str, required=True)
create_register_request_args.add_argument('firstName', type=str, required=True)
create_register_request_args.add_argument('lastName', type=str, required=True)

create_login_request_args = reqparse.RequestParser()
create_login_request_args.add_argument('email', type=str, nullable=True)
create_login_request_args.add_argument('password', type=str, nullable=True)

user_fields = {
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
}


@bp.route('/register', methods=['PUT'])
def register():
    from km.database import get_db
    from km.model import User
    from km.model.user import fetch_user_group, ensure_group_user

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
    from flask import current_app
    from km.model import User
    args = create_login_request_args.parse_args()
    if not args['email'] or not args['password']:
        abort(401, message='Invalid authentication credentials.')
    hash_ = sha256()
    hash_.update(args['password'].encode('utf-8'))
    user = User.query.filter_by(email=args['email'], password=hash_.hexdigest()).first()
    now = now_()
    expires = now + expiration_timespan
    token = jwt.encode(
        {'sub': user.email, 'exp': expires, 'aud': current_app.config['JWT_AUDIENCE'], 'iat': now,
         'permissions': user.permissions},
        current_app.config['PRIVATE_KEY'],
        algorithm='RS256')
    return jsonify({"access_token": token, "expires_at": datetime_to_unixtimestamp(expires)}), 200
