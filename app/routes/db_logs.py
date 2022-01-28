from app.core.session import get_session
from app.service.db_log_service import db_log_payment_service, db_log_login_service

from typing import Tuple, List, Optional


def get_payment_logs(
    tablename: str,
    state: str,
    less_than: bool = True,
    date: Optional[str] = None,
    limit: Optional[str] = None,
) -> Tuple[List, int]:
    get_session()

    response = db_log_payment_service(tablename, state, less_than, date, limit)

    return response, 200


def get_login_logs(
    less_than: bool = True, date: Optional[str] = None, limit: Optional[str] = None
) -> Tuple[List, int]:

    response = db_log_login_service(less_than, date, limit)

    return response, 200
