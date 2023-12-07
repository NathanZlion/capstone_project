from typing import Tuple


class Rating:
    def __init__(
        self,
        rating_id: int,
        driver_id: int,
        passenger_id: int,
        rating_value: int,
        feedback: str = "",
    ) -> None:
        self.rating_id = rating_id
        self.passenger_id = passenger_id
        self.driver_id = driver_id
        self.rating_value = rating_value
        self.feedback = feedback

    @staticmethod
    def from_tuple(rating_tuple: Tuple) -> "Rating":
        """
        The properties in the tuple should be in order, rating_id, phone_number, full_name, role
        """
        # destructure the tuple input

        rating_id, driver_id, passenger_id, rating_value, feedback = rating_tuple

        return Rating(rating_id, driver_id, passenger_id, rating_value, feedback)
