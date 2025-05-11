from datetime import datetime


# Helper function to validate the date range
def validate_dates(start_date: str, end_date: str):
    today = datetime.today()

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Dates must be in 'YYYY-MM-DD' format.")

    if start >= today:
        raise ValueError("Start date must be before today's date.")
    if end > today:
        raise ValueError("End date cannot be in the future.")

    if start >= end:
        raise ValueError("Start date must be before end date.")

    return start, end
