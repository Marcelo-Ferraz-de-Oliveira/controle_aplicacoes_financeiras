from webapp.position import Position
from datetime import datetime

class Profit:
    def __init__(self) -> None:
        self.__profit = {}
    
    @property
    def profit(self) -> dict:
        return self.__profit
    @profit.setter
    def profit(self, profit: dict) -> None:
        self.__profit = profit
    
    def to_dict(self) -> dict:
        return {}
    
    def update_profit(self, positions: Position) -> None:
        """Get all profits from previous positions and calculate total profit

        Args:
            positions (dict): Position dict

        Returns:
            dict: Profit dict with each date and total profit
        """    
        self.profit = {}
        for position in positions.position.values():
            for k, v in position['lucro'].items():
                self.profit[k] = self.profit[k] + v if k in self.profit else v
        self.profit['total'] = sum(self.profit.values())
    
    def get_month_profit(self, date: datetime) -> float:            
        month_profit = 0
        for k, v in self.profit.items():
            if k != 'total':
                if self._firstday_datetime(date) == self._str_date_to_datetime(k):
                    month_profit += v
        return month_profit

    def _str_date_to_datetime(self, date: str) -> datetime:
        return self._firstday_datetime(datetime.strptime(date, "%d/%m/%Y"))
    
    def _firstday_datetime(self, date: datetime) -> datetime:
        return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)