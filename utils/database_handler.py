# Database handler Module

import sqlite3
import logging


from typing import List
from custom.types.user import User
from custom.types.ride import Ride
from custom.types.rating import Rating
from custom.enums.ride_status import RideStatus
from custom.enums.user_roles import UserRole


class DB_Handler:
    def __init__(self):
        self._users = "users"
        self._rides = "rides"
        self._ratings = "ratings"
        self._database_file_name = "database.db"
        self.db_logger = logging.getLogger("database")

        self.db_logger.info("connecting to database ... ")

        # connecting to the database
        try:
            self._sqlite = sqlite3.connect(self._database_file_name)

        except Exception as e:
            self.db_logger.error(
                f"Error connecting to database, {self._database_file_name}: {e}"
            )
            raise e  # pass the error up to the caller
        self.db_logger.info("Connected to database successfully!")

        self._cursor = self._sqlite.cursor()

        self._create_user_table_sql_query = f""" CREATE TABLE IF NOT EXISTS {self._users} ( user_id TEXT PRIMARY KEY, full_name TEXT, phone_number TEXT, role TEXT CHECK(role IN ('Driver', 'Passenger')), created_at TEXT DEFAULT CURRENT_TIMESTAMP) """
        self._create_rides_table_sql_query = f""" CREATE TABLE IF NOT EXISTS {self._rides} ( ride_id INTEGER PRIMARY KEY AUTOINCREMENT, passenger_id INTEGER, driver_id INTEGER, ride_from TEXT, ride_to TEXT, eta INTEGER, fare_estimate INTEGER, status TEXT CHECK(status IN ('created', 'ongoing', 'completed', 'cancelled')), FOREIGN KEY (passenger_id) REFERENCES users(user_id), FOREIGN KEY (driver_id) REFERENCES users(user_id)) """
        self._create_ratings_table_sql_query = f""" CREATE TABLE IF NOT EXISTS {self._ratings} ( rating_id INTEGER PRIMARY KEY AUTOINCREMENT, driver_id INTEGER, passenger_id INTEGER, rating_value INTEGER CHECK (rating_value BETWEEN 1 AND 5), feedback TEXT, FOREIGN KEY (driver_id) REFERENCES users(user_id), FOREIGN KEY (passenger_id) REFERENCES users(user_id)) """

        try:
            self._create_tables()
        except Exception as e:
            self.db_logger.error(f"Error Creating tables: {e}")

        try:
            self.db_logger.info(f"Creating dummy user!")
            self._create_dummy_user()
        except Exception as e:
            self.db_logger.info(f"Dummy user already exist!")

        self.db_logger.info("Created tables successfully!")

    ### user related database methods ###
    def get_user_by_user_id(self, user_id: int) -> User | None:
        self._cursor.execute(
            f"""
            SELECT * FROM {self._users} WHERE user_id = :id
            """,
            {"id": user_id},
        )

        user_res = self._cursor.fetchone()
        if not user_res:
            return None

        return User.from_tuple(user_res)

    def create_user(
        self, user_id: int, full_name: str, phone_number: str, role: UserRole
    ) -> None:
        try:
            self._cursor.execute(
                f"""
                INSERT INTO {self._users} 
                (
                    user_id,
                    full_name,
                    phone_number,
                    role
                ) VALUES (
                    :user_id,
                    :full_name,
                    :phone_number,
                    :role
                )
                """,
                {
                    "user_id": user_id,
                    "full_name": full_name,
                    "phone_number": phone_number,
                    "role": role,
                },
            )
            self._sqlite.commit()
        except Exception as e:
            raise e

    def delete_user(self, user_id: int) -> None:
        try:
            self._cursor.execute(
                f"""
                    DELETE FROM {self._users} WHERE user_id = :id
                """,
                {"id": user_id},
            )

            self._sqlite.commit()
        except Exception as e:
            raise e

    def edit_user(
        self,
        user_id: int,
        full_name: str | None = None,
        phone_number: str | None = None,
    ) -> None:
        try:
            user = self.get_user_by_user_id(user_id)
            if not user:
                raise Exception("No User by that name!")

            full_name = full_name or user.full_name
            phone_number = phone_number or user.phone_number
            self._cursor.execute(
                f"""
                UPDATE {self._users} SET
                full_name= :_full_name,
                phone_number= :_phone_number,
                """,
                {"_full_name": full_name, "_phone_number": phone_number},
            )

            self._sqlite.commit()

        except Exception as e:
            raise e

    ### ride related database methods ###
    def create_ride(
        self,
        passenger_id: int,
        ride_from: str,
        ride_to: str,
        eta: int,
        fare_estimate: int,
        driver_id: int | None = -1,
    ) -> None:
        try:
            self._cursor.execute(
                f"""
                INSERT INTO {self._rides}
                (
                    passenger_id, 
                    driver_id,
                    rides_from,
                    rides_to,
                    eta,
                    fare_estimate,
                    status
                )
       
                VALUES (
                    :passenger_id,
                    :driver_id,
                    :ride_from,
                    :ride_to,
                    :eta,
                    :fare_estimate,
                    :status
                )
                """,
                {
                    "passenger_id": passenger_id,
                    "driver_id": driver_id,
                    "ride_from": ride_from,
                    "ride_to": ride_to,
                    "eta": eta,
                    "fare_estimate": fare_estimate,
                    "status": RideStatus.created,
                },
            )
        except Exception as e:
            raise e

    def update_ride_status(self, ride_id: int, ride_status: RideStatus) -> None:
        """
        This method allows to change the status of a ride.
        """
        try:
            self._cursor.execute(
                f"""UPDATE {self._rides} SET status = :status WHERE ride_id = :ride_id""",
                {"status": ride_status, "ride_id": ride_id},
            )

            self._sqlite.commit()
        except Exception as e:
            raise e

    def assign_driver_to_ride(self, ride_id: int, driver_id: int) -> None:
        try:
            self._cursor.execute(
                f"""UPDATE {self._rides} SET driver_id = :driver_id WHERE ride_id = :ride_id""",
                {"driver_id": driver_id, "ride_id": ride_id},
            )

            self._sqlite.commit()
        except Exception as e:
            raise e

    def get_ride_history(self, user_id: int) -> List[Ride] | None:
        self._cursor.execute(
            f"""
                SELECT * FROM {self._rides}
                WHERE user_id = :id AND
                status IN ({RideStatus.completed}, {RideStatus.cancelled})
            """,
            {"id": user_id},
        )

        rides_res = self._cursor.fetchall()
        if not rides_res:
            return None

        return [Ride.from_tuple(ride_tuple) for ride_tuple in rides_res]

    def create_rating(
        self,
        driver_id: int,
        passenger_id: int,
        rating_value: int,
        feedback: str,
    ) -> None:
        try:
            self._cursor.execute(
                f"""
                INSERT INTO {self._ratings}
                (
                    driver_id,
                    passenger_id,
                    rating_value, 
                    feedback
                )
                VALUES (
                    :driver_id,
                    :passenger_id,
                    :rating_value,
                    :feedback
                )
                """,
                {
                    "driver_id": driver_id,
                    "passenger_id": passenger_id,
                    "rating_value": rating_value,
                    "feedback": feedback,
                },
            )

            self._sqlite.commit()
        except Exception as e:
            raise e

    def get_driver_ratings(self, driver_id: int) -> List[Rating] | None:
        try:
            self._cursor.execute(
                f"""
                SELECT * FROM {self._ratings} WHERE driver_id = :driver_id
                """,
                {"driver_id": driver_id},
            )

            rating_res = self._cursor.fetchall()

            return [
                Rating.from_tuple(rating_tuple) for rating_tuple in rating_res
            ] or None

        except Exception as e:
            raise e

    def _create_tables(self) -> None:
        self.db_logger.info("Creating tables ... ")
        # create the users table if it doesn't exist
        self._cursor.execute(self._create_user_table_sql_query)
        self._sqlite.commit()

        # create rides table if not exist
        self._cursor.execute(self._create_rides_table_sql_query)
        self._sqlite.commit()

        # create the ratings table
        self._cursor.execute(self._create_ratings_table_sql_query)
        self._sqlite.commit()

    def _create_dummy_user(self):
        """
        This method creates a dummy driver user where we can reference to when creating a ride.
        When the ride request get's accepted by a driver then it gets assigned to the actual driver.
        """

        self.create_user(-1, "foo", "+2519123456", UserRole.Driver)
