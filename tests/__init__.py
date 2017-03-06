from datetime import datetime


def make_date(d):
    "For convenience."
    return datetime.strptime(d, "%Y-%m-%d").date()

