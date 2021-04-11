from sqlalchemy import ForeignKey

from km.database import Model, Column, String, Integer, Table, get_db, Relationship, Backref

user_usergroup_table = Table('user_usergroup', Model.metadata,
                             Column('user_id', Integer, ForeignKey('user.id')),
                             Column('group_id', Integer, ForeignKey('usergroup.id'))
                             )

usergroup_permission_table = Table('usergroup_permission', Model.metadata,
                                   Column('group_id', Integer, ForeignKey('usergroup.id')),
                                   Column('permission_id', Integer, ForeignKey('permission.id'))
                                   )


class Permission(Model):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True)

    def __repr__(self):
        return f"Permission(id={self.id}, name='{self.name}')"


class UserGroup(Model):
    __tablename__ = 'usergroup'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True)
    permissions = Relationship('Permission', secondary=usergroup_permission_table,
                               backref=Backref('groups', lazy='dynamic'))

    def __repr__(self):
        permissions = ""
        for permission in map(lambda p: repr(p), self.permissions):
            if len(permissions) > 0:
                permissions += ', '
            permissions += permission
        return f"UserGroup(id={self.id}, name='{self.name}', permissions=[{permissions}])"


class User(Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(200), unique=True)
    password = Column(String(64), index=True)
    last_name = Column(String(200))
    first_name = Column(String(200))
    groups = Relationship('UserGroup', secondary=user_usergroup_table, backref=Backref('users', lazy='dynamic'))

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def permissions(self):
        permissions = []
        for group in self.groups:
            for permission in group.permissions:
                permissions.append(permission.name)
        return permissions

    def __repr__(self):
        groups = ""
        for group in map(lambda g: repr(g), self.groups):
            if len(groups) > 0:
                groups += ', '
            groups += group
        return f"User(email='{self.email}', password='{self.password}', first_name='{self.first_name}', last_name='{self.last_name}', groups=[{groups}])"


def fetch_permission(name: str):
    permission = Permission.query.filter_by(name=name).first()
    if not permission:
        db = get_db()
        permission = Permission(name=name)
        db.session.add(permission)
    return permission


def fetch_user_group(name: str):
    user_group = UserGroup.query.filter_by(name=name).first()
    if not user_group:
        db = get_db()
        user_group = UserGroup(name=name)
        db.session.add(user_group)
    return user_group


def ensure_group_administrator():
    db = get_db()
    administrator = fetch_user_group('Administrator')
    permissions = administrator.permissions
    permissions.append(fetch_permission('concept:read'))
    permissions.append(fetch_permission('concept:write'))
    db.session.commit()


def ensure_group_user():
    db = get_db()
    user = fetch_user_group('User')
    permissions = user.permissions
    permissions.append(fetch_permission('concept:read'))
    db.session.commit()


def setup():
    ensure_group_administrator()
    ensure_group_user()
    pass
