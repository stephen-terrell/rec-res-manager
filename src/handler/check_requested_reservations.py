import requests
import datetime

from src.event.check_reservations_event import CheckReservationsEvent

sensitivity_levels = {
    'ALL_DAYS_AVAILABLE_NO_RV',
    'ANY_DAY_AVAILABLE_NO_RV',
    'ALL_DAYS_AVAILABLE',
    'ANY_DAY_AVAILABLE',
}

campsite_types = {
    'WALK TO': 'seems to be for backpackers',
    'STANDARD NONELECTRIC': 'standard site, but no trailers or long camper vans. see: https://www.recreation.gov/camping/campsites/514',
    'RV ELECTRIC': 'RV site, but don\'t see why you couldn\'t book it. see: https://www.recreation.gov/camping/campsites/464',
    'TENT ONLY NONELECTRIC': 'that good shit',
    'STANDARD ELECTRIC': 'no large rvs, seems you could book it for a tent. see: https://www.recreation.gov/camping/campsites/354',
    'GROUP TENT ONLY AREA NONELECTRIC': 'group site. minimum of 20 people',
    'MANAGEMENT': 'for our good friends the park rangers; not reservable',
}

campsite_type_allow_list = {
    'STANDARD NONELECTRIC',
    'TENT ONLY NONELECTRIC',
    'RV ELECTRIC',
    'STANDARD ELECTRIC',
}

rv_like_campsite_types = {
    'RV ELECTRIC',
    'STANDARD ELECTRIC',  # TODO: are we sure about this?
}

def handle(event, context):
    # campground_id = '232445'
    # output_date = datetime.datetime.now().strftime("2022-%m-01T00:00:00.000Z")
    #
    # print(output_date)
    # params = {
    #     'start_date': output_date
    # }
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    #     "Accept": "application/json",
    #     "Accept-Encoding": "gzip, deflate",
    #     "pragma": "no-cache"
    # }
    #
    # url_pattern = 'https://www.recreation.gov/api/camps/availability/campground/{campground_id}/month'
    #
    # get = requests.get(url_pattern.format(campground_id=campground_id), params=params, headers=headers)
    # # get = requests.get('https://www.recreation.gov/api/camps/availability/campground/232445/month?start_date=2022-04-01T00%3A00%3A00.000Z', headers=headers)
    #
    # # print(get.json())
    #
    # campsites = get.json()['campsites']
    #
    # camp_types = {}
    # for key, value in campsites.items():
    #     if value['type_of_use'] not in camp_types:
    #         camp_types[value['type_of_use']] = 1
    #     else:
    #         camp_types[value['type_of_use']] += 1
    #
    #
    # print(camp_types)
    #

    event_handler = CheckReservationsEvent(event, context)

    event_handler.handle()

    return {'hello': 'world'}


if __name__ == '__main__':
    handle(1, 2)
