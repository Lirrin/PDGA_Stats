from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class CourseLayout:
    "Represents a Course Layout"
    course_id: int
    layout_id: int
    layout_name: str
    holes: int
    length: int
    units: str
    
    def __str__(self):
        return f"{self.course_name} {self.layout_name}"