from enum import Enum


class UserRole(str, Enum):
    INVESTOR = "INVESTOR"
    OFFICER = "OFFICER"
    ADMIN = "ADMIN"


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    LOCKED = "LOCKED"
    PENDING = "PENDING"
