# Ride Hailing Bot 

## Database Schema

1. **Users Table:**
   - Columns:
     - `telegram_id` (Telegram ID for authentication) (Primary Key)
     - `full_name`
     - `phone_number`
     - `role` (driver/passenger) We could use an enum thing for this.

2. **Rides Table:**
   - Columns:
     - `ride_id` (Primary key) Autoincrement
     - `passanger_id` (Foreign key referencing Users table): passenger's telegram id
     - `driver_id` (Foreign key referencing Users table): driver's telegram id 
     - `current_location`:
     - `destination_location`: could be a string coordinate
     - `estimated_arrival_time`: eta based on the locations of destination and current location
     - `fare_estimate`: the money they paid. Could be based on the distance and eta.
     - `status` (created, ongoing, completed, canceled, etc.)

3. **Ratings Table:**
   - Columns:
     - `rating_id` (Primary key) AutoIncrement
     - `from_user_id` (Foreign key referencing Users table, the one giving the rating)
     - `to_user_id` (Foreign key referencing Users table, the one receiving the rating)
     - `rating_value`: an integer value from 1 to 5
     - `feedback`: a string review given by a passenger

