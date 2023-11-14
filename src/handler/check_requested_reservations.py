from src.event.check_reservations_event import CheckReservationsEvent

sensitivity_levels = {
    "ALL_DAYS_AVAILABLE_NO_RV",
    "ANY_DAY_AVAILABLE_NO_RV",
    "ALL_DAYS_AVAILABLE",
    "ANY_DAY_AVAILABLE",
}

campsite_types = {
    "WALK TO": "seems to be for backpackers",
    "STANDARD NONELECTRIC": """standard site, but no trailers or long camper vans. see:
                                https://www.recreation.gov/camping/campsites/514""",
    "RV ELECTRIC": """RV site, but don't see why you couldn't book it. see:
                    https://www.recreation.gov/camping/campsites/464""",
    "TENT ONLY NONELECTRIC": "that good shit",
    "STANDARD ELECTRIC": """no large rvs, seems you could book it for a tent. see:
                            https://www.recreation.gov/camping/campsites/354""",
    "GROUP TENT ONLY AREA NONELECTRIC": "group site. minimum of 20 people",
    "MANAGEMENT": "for our good friends the park rangers; not reservable",
}

campsite_type_allow_list = {
    "STANDARD NONELECTRIC",
    "TENT ONLY NONELECTRIC",
    "RV ELECTRIC",
    "STANDARD ELECTRIC",
}

rv_like_campsite_types = {
    "RV ELECTRIC",
    "STANDARD ELECTRIC",  # TODO: are we sure about this?
}


# TODO: remove this file and the entire code path
def handler(event, context):
    event_handler = CheckReservationsEvent(event, context)

    event_handler.handle()

    return {"hello": "world"}


if __name__ == "__main__":
    handler(1, 2)
