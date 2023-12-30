from datetime import datetime


def format_date_MM_YYYY(date: str) -> str:
    """
    Creates Datetime obj, returns a Str of MM YYYY
    :param date:
    :return: MONTH YEAR
    """
    tmp = datetime.fromisoformat(date)
    formatted_date = tmp.strftime('%b %Y')
    return formatted_date
