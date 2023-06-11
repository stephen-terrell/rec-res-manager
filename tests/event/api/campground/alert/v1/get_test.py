import os
import pytest
from unittest.mock import patch

from src.event.api.campground.alert.v1.get import GetAlert


@patch.dict(os.environ, {"USER_CONFIG_BUCKET_NAME": "us-west-2"})
class TestGetAlert:
    def test_enact_raises(self):
        under_test = GetAlert({})

        with pytest.raises(NotImplementedError):
            under_test.enact()
