from app.match_history.models import MatchHistory
from app.dao.base import BaseDAO


class MatchHistoryDAO(BaseDAO):
    model = MatchHistory
