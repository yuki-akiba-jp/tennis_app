from werkzeug.security import generate_password_hash

from backend.models import User


def init_db(db):
    pass
    # db.create_all()
    # with db.session.begin(subtransactions=True):
    # hashed_password = generate_password_hash('psw')
    # new_user = User(username='test', hashed_password=hashed_password)
    # db.session.add(new_user)
    # db.session.commit()
