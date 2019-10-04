from dataclasses import dataclass
from datetime import datetime


@dataclass
class CalendarEvent:
    start: datetime
    end: datetime
    subject: str
    subject_code: str
    event_type: str
    location: str
    description: str

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.start.strftime("%a%H") + self.subject))
