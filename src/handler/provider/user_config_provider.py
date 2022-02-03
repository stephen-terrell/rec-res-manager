

class UserConfigProvider:

    def get_user_config(self):
        return camp_config


camp_config = {
    'carly-stephen': {
        'version': 1,
        'subscribers': [
            'stephen.terrell14+rec-res@gmail.com'
        ],
        'autoBookCredentials': {
            'enc': ''
        },
        'campgrounds': [
            {
                'campgroundId': 232445,
                'checkInDate': '04/01/2022',
                'checkoutOutDate': '04/05/2022',
                'notificationPreferences': {
                    'notificationsEnabled': True,
                    'notificationSensitivityLevel': 'ANY_DAY_AVAILABLE',
                },
                'autoBookPreferences': {
                    'attemptAutoBook': True,
                    'autoBookSensitivityLevel': 'ALL_DAYS_AVAILABLE_NO_RV'
                },

            }
        ],
        'permits': [
            {
                'coming': 'soon'
            }
        ]
    }
}
