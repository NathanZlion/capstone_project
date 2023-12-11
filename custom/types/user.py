from custom.enums.user_roles import UserRole
from typing import Tuple


class User:
    def __init__(
        self, user_id: int, full_name: str, phone_number: str, role: UserRole
    ) -> None:
        self.user_id = user_id
        self.phone_number = phone_number
        self.full_name = full_name
        self.role = role

    @staticmethod
    def from_tuple(user_tuple: Tuple) -> "User":
        """
        The properties in the tuple should be in order, user_id, phone_number, full_name, role
        """
        # destructure the tuple input
        user_id, full_name, phone_number, role = user_tuple

        return User(user_id, full_name, phone_number, role)
