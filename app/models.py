
from app import db
from werkzeug.security import generate_password_hash, \
    check_password_hash


class UserModel(db.Model):
    """
    User Database Modal
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, email, password, name=None):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)

    @staticmethod
    def check_password(pw_hash, password):
        """ 
        Validates password        
        :param pw_hash: 
        :param password: 
        """
        return check_password_hash(pw_hash, password)

    def save(self):
        """
        Save User to DB        
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all Users"""
        return UserModal.query.all()

    def delete(self):
        """Delete User"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<User: {}>".format(self.name)


class ShoppinglistsModel(db.Model):
    """
    Shopping Lists database Model
    """
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, desc, user_id):
        self.name = name
        self.desc = desc
        self.user_id = user_id

    def save(self):
        """
        Save List to DB
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        """Updates List"""
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all Lists"""
        ShoppinglistsModal.query.all()

    def delete(self):
        """Delete List"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Shoplist: {}>".format(self.name)


class ItemsModal(db.Model):
    """
    Item Database Modal
    """
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(5), default=False)
    price = db.Column(db.String(100))
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    def __init__(self, name, bucket_id):
        self.name = name
        self.list_id = list_id

    def save(self):
        """
        Save Item to DB
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all Items"""
        ItemsModal.query.all()

    def delete(self):
        """Delete Item"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        """Updates Items"""
        db.session.commit()

    def __repr__(self) -> str:
        return "<Item: {}>".format(self.name)
