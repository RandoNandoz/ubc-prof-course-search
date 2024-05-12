from enum import Enum
from typing import Optional

"""
Class for a Course at UBC
"""


class Campus(Enum):
    Okanagan = "UBCO"
    Vancouver = "UBCV"


class Session(Enum):
    Summer = "S"
    Winter = "W"


class Course:
    def __init__(self, campus: Campus, year: int, session: Session, subject: str, code: str, detail: Optional[str],
                 section: str, desc: str, avg: float):
        self.campus = campus
        self.year = year
        self.session = session
        self.subject = subject
        self.code = code
        self.detail = detail
        self.section = section
        self.desc = desc
        self.avg = avg

    def __str__(self):
        return f"{self.campus.value}-{self.year}{self.session.value}-{self.subject}-{self.code}{self.detail if self.detail is not None else ''}-{self.section}"

    def get_desc(self):
        return self.desc

    def __eq__(self, other):
        if not isinstance(other, Course): return False
        if self is other: return True

        campus_eq = self.campus == other.campus
        year_eq = self.year == other.year
        session_eq = self.session == other.session
        subject_eq = self.subject == other.subject
        code_eq = self.code == other.code
        details_eq = self.detail == other.detail
        section_eq = self.section == other.section
        desc_eq = self.desc == other.desc
        average_eq = self.avg == self.avg

        return campus_eq and year_eq and session_eq and subject_eq and code_eq and details_eq and section_eq and desc_eq and average_eq

    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.year == other.year and self.session == Session.Summer and other.session == Session.Winter:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.year > other:
            return True
        elif self.year == other.year and self.session == Session.Winter and other.session == Session.Summer:
            return True
        else:
            return False

    def __dict__(self):
        return {'campus': self.campus.value, 'year': self.year, 'session': self.session.value, 'subject': self.subject,
                'code': self.code, 'detail': self.detail, 'section': self.section, 'desc': self.desc,
                'ubcgrades': str(self), 'avg': self.avg}
