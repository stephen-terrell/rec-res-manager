from typing import List

from src.model.campground_availability import CampgroundAvailability


class EmailFormatter:
    __campsite_url_format = 'https://www.recreation.gov/camping/campsites/{campsite_id}'
    __campground_url_format = 'https://www.recreation.gov/camping/campgrounds/{campground_id}'

    def get_formatted_message(self, campground_availabilities: List[CampgroundAvailability]):
        message_parts = [
            'Hello!\n\n',
            'Availability found for your requested campground(s). Good luck!\n\n\n'
        ]

        for campground_availability in campground_availabilities:
            message_parts.append(
                'Availabilities for campground: {name} ({alternate})\n'.format(
                    name=campground_availability.get_campground_name().get('facility_name'),
                    alternate=campground_availability.get_campground_name().get('alternate_names')
                )
            )
            message_parts.append(self.__campground_url_format.format(campground_id=campground_availability.campground_id))
            message_parts.append('\n\n')
            for campsite in campground_availability.get_campsites():
                message_parts.append(
                    'Site: {site} | Type: {type}\n'.format(site=campsite.site, type=campsite.campsite_type.value)
                )
                for key, value in campsite.availabilities.items():
                    message_parts.append('  • {date} - {status}\n'.format(date=key, status=value))
                message_parts.append('Book it here: ')
                message_parts.append(self.__campsite_url_format.format(campsite_id=campsite.campsite_id))
                message_parts.append('\n\n')

        message_parts.append('\n\n')
        message_parts.append('Beep boop, I\'m a computer. Automation provided by Stephen 🍻')

        return ''.join(message_parts)
