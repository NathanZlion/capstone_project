from enum import Enum


class RideStatus(Enum):
    created = "created"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"
