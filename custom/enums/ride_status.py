from dataclasses import dataclass


@dataclass
class RideStatus:
    created: str = "created"
    ongoing: str = "ongoing"
    completed: str = "completed"
    calcelled: str = "cancelled"
