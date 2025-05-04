import enum

class Role(str, enum.Enum):
    SUPERUSER = "Superuser"
    EDITOR = "Editor"
    VIEWER = "Viewer"