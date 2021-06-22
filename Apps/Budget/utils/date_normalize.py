import datetime
from django.utils import timezone


def date_normalize(naive_date):
    cur_time_zone = timezone.get_current_timezone()
    dt_obj = datetime.datetime.strptime(naive_date, "%Y-%m-%d %H:%M:%S.%f")
    return cur_time_zone.localize(dt_obj)
