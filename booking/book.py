# TODO create function for scheduling 
# Set Title
# Add Description
# Choose date and time
# Add participants 

# TODO create function for inviting participants to booking and accepting/declining invitations
# TODO create function for editing and rescheduling bookings

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import insert_data, init_tables, Bookings, Booking_participants, session
from fastapi import HTTPException
from utils.logger_config import logger
from utils.config import Config
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

db = session()

init_tables(Bookings)

# Initialize the Bookings table if it doesn't exist

# Define a Pydantic model for validation
class Schedule(BaseModel):
    user_id: str
    title: str
    description: str
    start_date: datetime
    end_date: datetime

# ==============================================================================================================================================
# ==============================================================================================================================================

# Check for overlapping schedules for a user
def check_overlapping_schedules(user_id: str, start_date: datetime, end_date: datetime) -> bool:
    # Query the database for bookings that overlap with the given time range
    overlapping_bookings = db.query(Bookings).filter(
        Bookings.user_id == user_id,
        Bookings.start_date < end_date,
        Bookings.end_date > start_date
    ).all()
    
    return len(overlapping_bookings) > 0

# ===============================
# CRUD operations for bookings ||
# ===============================


# CREATE 
def add_schedule(schedule: Schedule):
    # Add the booking to the database
    booking_data = {
        "user_id": schedule.user_id,
        "booking_title": schedule.title,
        "booking_description": schedule.description,
        "start_date": schedule.start_date,
        "end_date": schedule.end_date,
        "created_at": datetime.now()
    }
    
    overlapping_schedule = check_overlapping_schedules(schedule.user_id, 
                                                       schedule.start_date, 
                                                       schedule.end_date)
    
    if overlapping_schedule:
        logger.warning(f"User {schedule.user_id} has overlapping schedules. Booking not added.")
        return {"message": "Booking overlaps with an existing schedule. Please choose a different time."}
    
    insert_data(Bookings, **booking_data)
    logger.info(f"Booking added successfully for user {schedule.user_id}.")
    return {"message": "Booking added successfully."}

# UPDATE
def edit_schedule(booking_id: str, updated_schedule: Schedule):
    # TODO implement edit schedule function
    pass
    
# DELETE    
def delete_schedule(booking_id: str):
    # TODO implement delete schedule function
    pass

if __name__ == "__main__":
    
    # Test
    
    test_schedule = Schedule(
        user_id="user123",
        title="Test Booking",
        description="This is a test booking.",
        start_date=datetime(2026, 10, 10, 10, 0),
        end_date=datetime(2026, 10, 10, 11, 0)
    )
    
    add_schedule(test_schedule)