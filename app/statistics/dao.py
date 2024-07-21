from app.statistics.models import Statistics
from app.dao.base import BaseDAO


class StatisticsDAO(BaseDAO):
    model = Statistics
