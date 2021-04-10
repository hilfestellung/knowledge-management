from km.database import Model, Column, String


class User(Model):
    __tablename__ = 'user'

    email = Column(String(200), primary_key=True)
    password = Column(String(64), index=True)
    last_name = Column(String(200))
    first_name = Column(String(200))

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"User(email='{self.email}', password='{self.password}', first_name='{self.first_name}', last_name='{self.last_name}')"
