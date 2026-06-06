from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class CourseLayout:
    "Represents a Course Layout"
    course_id: int
    layout_id: int
    layout_name: str
    hole_count: int
    course_par: int
    total_length: int
    length_unit: str
    
    def __str__(self):
        return f"{self.course_name} {self.layout_name}"