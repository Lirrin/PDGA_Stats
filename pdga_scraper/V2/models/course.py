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

'''
    course_layouts.append({
            "event_id": event_id,
            "layout_id": layoutID,
            "layout_name": c["Name"],
            "course_id": courseID,
            "course_name": c["CourseName"],
            "holes": c["Holes"],
            "par": c["Par"],
            "length": c["Length"],
            "units": units
        })
'''