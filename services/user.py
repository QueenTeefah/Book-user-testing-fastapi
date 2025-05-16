from uuid import uuid4
from database import users
from schemas.user import User, UserCreate, UserUpdate


class UserService:

    @staticmethod
    def get_user_by_id(user_id):
        user = users.get(str(user_id))
        if not user:
            return None
        return user

    @staticmethod
    def create_user(user_in: UserCreate):
        user = User(
            id=str(uuid4()),
            **user_in.model_dump()
        )
        users[user.id] = user
        return user

    @staticmethod
    def update_user(user_id, user_in: UserUpdate):
        user = users.get(str(user_id))
        if not user:
            return None

        if user_in.username is not None:
            user.username = user_in.username
        if user_in.email is not None:
            user.email = user_in.email
        if user_in.full_name is not None:
            user.full_name = user_in.full_name

        return user

    @staticmethod
    def delete_user(user_id):
        user = users.get(str(user_id))
        if not user:
            return None

        del users[user.id]
        return True


user_service = UserService()
