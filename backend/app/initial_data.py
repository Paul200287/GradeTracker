import logging
from sqlalchemy.orm import Session

from app.core.db import init_db
from app.database.session import engine
from app.models.role import Role as RoleEnum
from app.models.user import User
from app.core.security import get_password_hash
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("🔧 Creating initial data")
    init()
    logger.info("✅ Initial data created")


if __name__ == "__main__":
    main()
