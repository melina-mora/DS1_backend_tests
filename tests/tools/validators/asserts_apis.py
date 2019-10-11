from colorama import Fore
from pytest import fail


def assert_response(response):
    try:
        assert response.status_code in [200, 201]
    except AssertionError as error:
        api_failed = response.url

        fail(msg=Fore.RED + "(%s) API: %s \n RESPONSE: %s" % (response.status_code, api_failed, response.json),
             pytrace=False)
