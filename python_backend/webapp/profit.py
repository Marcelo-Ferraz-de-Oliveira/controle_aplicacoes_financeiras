from webapp.position import Position
from datetime import datetime

class Profit:
    def __init__(self) -> None:
        self.__profit = {}
        self.__month_profit = {}
        self.__profit_daytrade = {}
        self.__month_profit_daytrade = {}
    
    @property
    def profit(self) -> dict:
        return self.__profit
    @profit.setter
    def profit(self, profit: dict) -> None:
        self.__profit = profit
    
    @property
    def month_profit(self) -> dict:
        return self.__month_profit
    @month_profit.setter
    def month_profit(self, month_profit: dict) -> None:
        self.__month_profit = month_profit

    @property
    def profit_daytrade(self) -> dict:
        return self.__profit_daytrade
    @profit_daytrade.setter
    def profit_daytrade(self, profit_daytrade: dict) -> None:
        self.__profit_daytrade = profit_daytrade
    
    @property
    def month_profit_daytrade(self) -> dict:
        return self.__month_profit_daytrade
    @month_profit_daytrade.setter
    def month_profit_daytrade(self, month_profit_daytrade: dict) -> None:
        self.__month_profit_daytrade = month_profit_daytrade

    def get_months_with_profit(self) -> None:
        months = self._date_str_to_sorted_unique_months_str(list(self.profit.keys()))
        self.month_profit = {month: self._get_month_profit(self.profit, datetime.strptime(month, "%m/%Y")) for month in months}

    def get_months_with_profit_daytrade(self) -> None:
        months = self._date_str_to_sorted_unique_months_str(list(self.profit_daytrade.keys()))
        self.month_profit_daytrade = {month: self._get_month_profit(self.profit_daytrade, datetime.strptime(month, "%m/%Y")) for month in months}
    
    def _date_str_to_sorted_unique_months_str(self, days: list) -> list:
        months = [datetime.strptime(day, "%d/%m/%Y").replace(day=1) for day in days]
        return [datetime.strftime(date, "%m/%Y") for date in sorted(set(months))]
    
    def update_profit(self, positions: Position) -> None:
        """Get all profits from previous positions and calculate total profit

        Args:
            positions (dict): Position dict

        Returns:
            dict: Profit dict with each date and total profit
        """    
        self.profit = {}
        self.profit_daytrade = {}
        for position in positions.position.values():
            for k, v in position['lucro_normal'].items():
                self.profit[k] = self.profit[k] + v if k in self.profit else v
            for k, v in position['lucro_daytrade'].items():
                self.profit_daytrade[k] = self.profit_daytrade[k] + v if k in self.profit_daytrade else v
        self.get_months_with_profit()
        self.get_months_with_profit_daytrade()

    
    def _get_month_profit(self, profit, date: datetime) -> float:            
        month_profit = 0
        for k, v in profit.items():
            if self._firstday_datetime(date) == self._str_date_to_datetime(k):
                month_profit += v
        return month_profit

    def _str_date_to_datetime(self, date: str) -> datetime:
        return self._firstday_datetime(datetime.strptime(date, "%d/%m/%Y"))
    
    def _firstday_datetime(self, date: datetime) -> datetime:
        return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)