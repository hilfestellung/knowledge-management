from hashlib import sha256

from flask import Blueprint
from flask_restful import reqparse, fields, marshal

bp = Blueprint('authentication', __name__, url_prefix='/authentication')

create_register_request_args = reqparse.RequestParser()
create_register_request_args.add_argument('email', type=str, required=True)
create_register_request_args.add_argument('password', type=str, required=True)
create_register_request_args.add_argument('firstName', type=str, required=True)
create_register_request_args.add_argument('lastName', type=str, required=True)

user_fields = {
    'email': fields.String,
}


@bp.route('/register', methods=['PUT'])
def register():
    from km.database import get_db
    from km.model import User

    args = create_register_request_args.parse_args()
    hash_ = sha256()
    hash_.update(args['password'].encode('utf-8'))
    user = User(email=args['email'], password=hash_.hexdigest(), first_name=args['firstName'],
                last_name=args['lastName'])
    db = get_db()
    db.session.add(user)
    db.session.commit()

    return marshal(user, user_fields), 201
