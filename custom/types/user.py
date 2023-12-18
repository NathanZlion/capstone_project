import datetime
from custom.enums.user_roles import UserRole
from typing import Optional, Tuple


class User:
    def __init__(
        self, user_id: int, full_name: str, phone_number: str, role: UserRole, created_at: Optional[str] = str( datetime.datetime.now())
    ) -> None:
        self.user_id = user_id
        self.phone_number = phone_number
        self.full_name = full_name
        self.role = role
        self.created_at = created_at

    @staticmethod
    def from_tuple(user_tuple: Tuple) -> "User":
        """
        The properties in the tuple should be in order, user_id, phone_number, full_name, role
        """
        user_id, full_name, phone_number, role, created_at = user_tuple

        return User(user_id, full_name, phone_number, role, created_at)
