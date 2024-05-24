# create_user.py
from models.user import User

user = User()
user.email = "bobsession@hbtn.io"
user.password = "fake pwd"
user.save()
print("User created with email:", user.email)
