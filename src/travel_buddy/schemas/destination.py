from pydantic import BaseModel, ConfigDict
from typing import List

class Destination(BaseModel):
    """
    Destination model
    """
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    country: str
    region : str
    description : str
    days_recommended: int
    best_months: List[int]
    entry_requirements : str
    safety_level : str
    crowds : str

class Attraction(BaseModel):
    """
    Attraction model for a destination
    """
    model_config = ConfigDict(from_attributes=True)
    id : str
    name : str
    destination : str
    category : str
    description : str
    cultural_notes : str
    best_time : str
    crowd_level : str
    entrance_fee: str
    hours: str


class Event(BaseModel):
    """
    Event/festival model for a destination
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    destination : List[str]
    season : str
    months : List[str]
    duration : str
    description : str
    cultural_notes: str
    crowdedness : str
    what_to_know: str


class DestinationGuide(BaseModel):
    """
    Complete guide response
    """
    destination : Destination
    attractions : List[Attraction]
    events: List[Event]