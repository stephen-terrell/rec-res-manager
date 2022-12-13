import os
from unittest.mock import patch

from src.proxy.sns_proxy import SnsProxy


def test_simple_assert():
    asdf = 'asdf'
    assert asdf == 'asdf'


@patch.dict(os.environ, {'AWS_REGION': 'us-west-2', 'AWS_DEFAULT_REGION': 'us-west-2', 'AWS_ACCOUNT_ID': '1234'})
@patch("src.proxy.sns_proxy.boto3")
def test_me_is_test(boto3_mock, os_environ_patch):
    under_test_2 = SnsProxy()

    asdf = 'asdf'
    fdsa = 'fdsa'

    assert asdf + fdsa == under_test_2.me_is_test(asdf, fdsa)
