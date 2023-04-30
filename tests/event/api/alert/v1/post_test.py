import pytest
from unittest.mock import patch

from src.event.api.alert.v1.post import PostAlert


class TestPost:
    @pytest.fixture
    def campground_id_1(self):
        return "campground111111"

    @pytest.fixture
    def user_id_1(self):
        return "user1111111"

    @pytest.fixture
    def alert_id_1(self):
        return "alert1111111"

    @pytest.fixture
    def check_in_date_1(self):
        return "today"

    @pytest.fixture
    def check_out_date_1(self):
        return "tomorrow"

    @pytest.fixture
    def notification_preferences(self):
        return {"notificationSensitivityLevel": "ANY_DAYS_AVAILABLE", "notificationsEnabled": True}

    @pytest.fixture
    def make_event(self):
        def _make_event(alert_id, user_id, campground_id, check_in_date, check_out_date, notification_preferences):
            return {
                "headers": {"x-rec-res-user-id": user_id},
                "pathParameters": {"alertId": alert_id},
                "body": {
                    "campgroundId": campground_id,
                    "type": "recreation.gov",
                    "checkInDate": check_in_date,
                    "checkOutDate": check_out_date,
                    "notificationPreferences": notification_preferences,
                },
            }

        return _make_event

    @pytest.fixture
    def send_api_command_mock(self):
        with patch("src.event.api.alert.v1.post.SqsProxy") as sqs_proxy:
            yield sqs_proxy.return_value.send_api_command

    def test_enact(
        self,
        alert_id_1,
        user_id_1,
        campground_id_1,
        check_in_date_1,
        check_out_date_1,
        notification_preferences,
        make_event,
        send_api_command_mock,
    ):
        under_test = PostAlert(
            make_event(
                alert_id_1, user_id_1, campground_id_1, check_in_date_1, check_out_date_1, notification_preferences
            )
        )

        result = under_test.enact()

        data = {
            "userId": user_id_1,
            "alertId": alert_id_1,
            "type": "recreation.gov",
            "checkInDate": check_in_date_1,
            "checkOutDate": check_out_date_1,
            "notificationPreferences": notification_preferences,
        }

        assert result == data

        send_api_command_mock.assert_called_once_with({"commandName": "UPDATE_ALERT", "data": data})
