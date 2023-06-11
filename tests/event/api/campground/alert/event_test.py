import pytest
from unittest.mock import patch

from src.event.api.campground.alert.event import AlertEvent


class TestAlertEvent:
    @pytest.fixture
    def handler_result(self):
        return {"asdf": "list alerts"}

    @pytest.fixture
    def list_alerts_mock(self, handler_result):
        with patch("src.event.api.campground.alert.event.ListAlerts") as list_alerts_mock:
            list_alerts_mock.return_value.enact.return_value = handler_result

            yield list_alerts_mock

    def test_list(self, handler_result, list_alerts_mock):
        event = {"routeKey": "GET /campground/alerts"}

        under_test = AlertEvent(event, {})

        result = under_test.handle()

        list_alerts_mock.assert_called_once_with(event)

        assert result == handler_result

    @pytest.fixture
    def get_alert_mock(self, handler_result):
        with patch("src.event.api.campground.alert.event.GetAlert") as get_alerts_mock:
            get_alerts_mock.return_value.enact.return_value = handler_result

            yield get_alerts_mock

    def test_get(self, handler_result, get_alert_mock):
        event = {"routeKey": "GET /campground/alerts/{alertId}"}

        under_test = AlertEvent(event, {})

        result = under_test.handle()

        get_alert_mock.assert_called_once_with(event)

        assert result == handler_result

    @pytest.fixture
    def put_alert_mock(self, handler_result):
        with patch("src.event.api.campground.alert.event.PutAlert") as put_alerts_mock:
            put_alerts_mock.return_value.enact.return_value = handler_result

            yield put_alerts_mock

    def test_put(self, handler_result, put_alert_mock):
        event = {"routeKey": "PUT /campground/alerts"}

        under_test = AlertEvent(event, {})

        result = under_test.handle()

        put_alert_mock.assert_called_once_with(event)

        assert result == handler_result

    @pytest.fixture
    def delete_alert_mock(self, handler_result):
        with patch("src.event.api.campground.alert.event.DeleteAlert") as delete_alert_mock:
            delete_alert_mock.return_value.enact.return_value = handler_result

            yield delete_alert_mock

    def test_delete(self, handler_result, delete_alert_mock):
        event = {"routeKey": "DELETE /campground/alerts/{alertId}"}

        under_test = AlertEvent(event, {})

        result = under_test.handle()

        delete_alert_mock.assert_called_once_with(event)

        assert result == handler_result

    @pytest.fixture
    def post_alert_mock(self, handler_result):
        with patch("src.event.api.campground.alert.event.PostAlert") as post_alert_mock:
            post_alert_mock.return_value.enact.return_value = handler_result

            yield post_alert_mock

    def test_post(self, handler_result, post_alert_mock):
        event = {"routeKey": "POST /campground/alerts/{alertId}"}

        under_test = AlertEvent(event, {})

        result = under_test.handle()

        post_alert_mock.assert_called_once_with(event)

        assert result == handler_result

    def test_invalid_route_key(self):
        event = {"routeKey": "invalid"}

        under_test = AlertEvent(event, {})

        with pytest.raises(ValueError):
            under_test.handle()

    def test_missing_route_key(self):
        event = {"some": "other key"}

        under_test = AlertEvent(event, {})

        with pytest.raises(ValueError):
            under_test.handle()
