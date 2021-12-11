from dataclasses import dataclass


@dataclass
class MonthYear:
    """A class that ties together the month and year of a certain time period

    Instance Attributes:
        - month: the month of the time period
        - year: the year of the time period

    Representation Invariants:
        - self.month in [Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec']
        - self.year in ['2020', '2021']
    """
    month: str
    year: str


def generate_month_year_list() -> list[MonthYear]:
    """Generates a list of month-year combinations for file"""
    return [MonthYear('Jan', '2020'),
            MonthYear('Feb', '2020'),
            MonthYear('Mar', '2020'),
            MonthYear('Apr', '2020'),
            MonthYear('May', '2020'),
            MonthYear('Jun', '2020'),
            MonthYear('Jul', '2020'),
            MonthYear('Aug', '2020'),
            MonthYear('Sep', '2020'),
            MonthYear('Oct', '2020'),
            MonthYear('Nov', '2020'),
            MonthYear('Dec', '2020'),
            MonthYear('Jan', '2021'),
            MonthYear('Feb', '2021'),
            MonthYear('Mar', '2021'),
            MonthYear('Apr', '2021'),
            MonthYear('May', '2021'),
            MonthYear('Jun', '2021'),
            MonthYear('Jul', '2021'),
            MonthYear('Aug', '2021'),
            MonthYear('Sep', '2021')]
