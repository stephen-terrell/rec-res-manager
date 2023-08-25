from src.event.check_user_alerts_event import CheckUserAlertsEvent


def handler(_, __):
    event_handler = CheckUserAlertsEvent()

    event_handler.handle()
