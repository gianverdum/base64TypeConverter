# src/schemas/participant.py
import re
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ParticipantCreate(BaseModel):
    """
    Schema for creating a participant with necessary details.

    Attributes:
        full_name (str): Full name of the participant.
        company_name (str): Company the participant is representing.
        whatsapp (str): Participant's WhatsApp number.
        email (str): Participant's email address.
        custom_data (dict, optional): Additional dynamic fields for the event.
        event_id (int): ID of the event the participant is attending.
    """

    full_name: str
    company_name: str
    whatsapp: str
    email: EmailStr
    custom_data: Optional[Dict[str, Any]] = Field(default=None)
    event_id: int

    model_config = ConfigDict(from_attributes=True)

    @field_validator("custom_data", mode="before")  # Ensure the validator is static or class-based
    @classmethod
    def validate_custom_data(cls, value: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Ensures custom_data is stored as a dictionary. If custom_data is a string,
        it will try to parse it as JSON. If the value is None, it is allowed.
        """
        if value is None:
            return None
        if isinstance(value, str):
            try:
                # Try parsing string as JSON if it's passed as a string
                import json

                return json.loads(value)
            except json.JSONDecodeError:
                raise ValueError("custom_data must be a valid JSON string or dictionary.")
        elif isinstance(value, dict):
            return value
        else:
            raise ValueError("custom_data must be a dictionary or a valid JSON string.")

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        """
        Ensures full_name contains at least a first name and a last name.
        """
        if len(value.split()) < 2:
            raise ValueError("full_name must contain at least a first name and a last name.")
        return value

    @field_validator("whatsapp")
    @classmethod
    def validate_whatsapp(cls, value: str) -> str:
        """
        Ensures whatsapp has at least 11 numeric digits.
        """
        if not re.match(r"^\+?\d{11,15}$", value):
            raise ValueError("whatsapp must be a valid phone number with at least 11 digits.")
        return value


class ParticipantRead(ParticipantCreate):
    """
    Schema for reading a participant, which includes the participant ID.

    Attributes:
        id (int): Unique identifier for the participant.
        full_name (str): Name of the participant.
        whatsapp (str): Whatsapp of the participant.
        email (str): E-mail of the participant.
        custom_data (Dict): Additional dynamic fields specific to the event (optional).
    """

    id: int

    model_config = ConfigDict(from_attributes=True)