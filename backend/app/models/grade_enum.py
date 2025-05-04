import enum

class GradeEnum(str, enum.Enum):
    sehr_gut = "Sehr gut"
    gut = "Gut"
    befriedigend = "Befriedigend"
    genuegend = "Genügend"
    nicht_genuegend = "Nicht Genügend"
