import enum

class Role(str, enum.Enum):
    SUPERUSER = "Superuser"
    RACECONTROL = "RaceControl"
    RACINGTEAM = "RacingTeam"
    STARTLINEJUDGE = "StartLineJudge"