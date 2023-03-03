import pytz

from datetime import datetime

from scheduler.models import User


def check_send_to_user(user: User) -> bool:
    """Checks the allowed time in user settings."""    
    tz_user = pytz.timezone(user.timezone)
    checking_time = datetime.now(tz_user).time()
    if (user.from_time <= checking_time) and (user.befor_time > checking_time):
        return True
    return False


def sorting_users_for_timezones(name_groop: str | None = None) -> tuple:
    """Sorts users by allowed posting time.
    
    Returns a tuple of lists of user ids with permission
    and disallow sending.
    """
    sending = []
    not_sending = []
    if name_groop is None:
        users = User.objects.all()
    else:
        users = User.objects.filter(groups__name=name_groop)
    for user in users:
        user_id = str(user.id) 
        if check_send_to_user(user) is True:
            sending.append(user_id)
        else:
            not_sending.append(user_id)
    return sending, not_sending


def sorting_delayed_users_for_timezones(uses_ids: list) -> tuple:
    """re-sorts delayed users by allowed posting time.
    
    Returns a tuple of lists of user ids with permission
    and disallow sending.
    """
    sending = []
    not_sending = []
    users = User.objects.filter(pk__in=uses_ids)
    for user in users:
        user_id = str(user.id) 
        if check_send_to_user(user) is True:
            sending.append(user_id)
        else:
            not_sending.append(user_id)
    return sending, not_sending
