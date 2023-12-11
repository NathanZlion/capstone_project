from dataclasses import dataclass


@dataclass
class UserRole:
    Driver: str = "driver"
    Passenger: str = "passenger"
