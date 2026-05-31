
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import create_model, init_tables
from sqlalchemy import Enum, Column, Integer, String, DateTime, ForeignKey
from utils.logger_config import logger
from utils.config import Config

# User Schema
Users = create_model(
    "users",
    user_id=Column(String, primary_key=True, unique=True, nullable=False),
    username=Column(String, unique=True, nullable=False),
    email=Column(String, unique=True, nullable=False),
    password=Column(String, nullable=False),
    created_at=Column(DateTime, nullable=False)
)

# Status = pending, ongoing, completed, cancelled

Bookings = create_model(
    "bookings",
    booking_id=Column(String, primary_key=True, unique=True, nullable=False),
    title=Column(String, nullable=False),
    description=Column(String, nullable=True),
    creator_id=Column(String, ForeignKey("users.user_id"), nullable=False),
    start_datetime=Column(DateTime, nullable=False),
    end_datetime=Column(DateTime, nullable=False),
    status=Column(String, nullable=False, default="pending"),
    created_at=Column(DateTime, nullable=False)
)

# Response Status = pending, accepted, declined

Booking_participants = create_model(
    "booking_participants",
    id=Column(Integer, primary_key=True, autoincrement=True),
    booking_id=Column(String, ForeignKey("bookings.booking_id"), nullable=False),
    user_id=Column(String, ForeignKey("users.user_id"), nullable=False),
    response_status=Column(String, nullable=False, default="pending"),
    created_at=Column(DateTime, nullable=False)
)