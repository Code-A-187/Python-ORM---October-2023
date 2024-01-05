from models import User
from main import Session

with Session() as session:
    users = session.query(User).all()
    for user in users:
        print(user.username, user.email)