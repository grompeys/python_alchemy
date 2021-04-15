# pylint: disable=import-error
from werkzeug.security import safe_str_cmp
# pylint: enable=import-error
from models.user import UserModel

# users = [
#     UserModel(1, 'billy', 'broot')
# ]

# username_mapping = {u.username: u for u in users}

# userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)