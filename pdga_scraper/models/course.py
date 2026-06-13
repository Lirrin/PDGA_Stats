from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Course:
    "Represents a Course"
    course_id: int
    course_name: str
    
    def __str__(self):
        return f"{self.course_name}"
    
def to_course(layout: dict):
    return Course(
        course_id=layout["course_id"],
        course_name=layout["course_name"]
    )
