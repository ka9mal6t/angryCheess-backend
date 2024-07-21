from app.dao.base import BaseDAO
from app.recovery.models import Recovery
from app.users.models import Users


class RecoveryDAO(BaseDAO):
    model = Recovery



