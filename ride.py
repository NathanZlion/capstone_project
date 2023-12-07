from typing import Tuple
from custom_enums.ride_status import RideStatus


class Ride:
    def __init__(
        self,
        ride_id: int,
        passenger_id: int,
        driver_id: int,
        ride_from: str,
        ride_to: str,
        eta: int,
        fare_estimate: int,
        status: RideStatus,
    ):
        self.ride_id = ride_id
        self.passenger_id = passenger_id
        self.driver_id = driver_id
        self.ride_from = ride_from
        self.ride_to = ride_to
        self.eta = eta
        self.fare_estimate = fare_estimate
        self.status = status

    @staticmethod
    def from_tuple(ride_tuple: Tuple) -> "Ride":
        """
        The properties in the tuple should be in ride_id, passenger_id,
        driver_id, ride_from, ride_to, eta, fare_estimate, status
        """
        # destructure the tuple input
        (
            ride_id,
            passenger_id,
            driver_id,
            ride_from,
            ride_to,
            eta,
            fare_estimate,
            status,
        ) = ride_tuple

        return Ride(
            ride_id,
            passenger_id,
            driver_id,
            ride_from,
            ride_to,
            eta,
            fare_estimate,
            status,
        )
