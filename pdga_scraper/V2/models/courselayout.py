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
    

def to_course_layout(layout:dict):

    return CourseLayout(
        course_id= layout["course_id"],
        layout_id= layout["layout_id"],
        layout_name = layout["layout_name"],
        hole_count = layout["holes"],
        course_par = layout["par"],
        total_length = layout["length"],
        length_unit = layout["units"]
    )
    
    
