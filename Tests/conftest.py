import pytest


@pytest.fixture(scope="function")
def fixture(request):
    print("Started TestCase " + request.function.__name__ + ".")
    yield
    print("Completed TestCase " + request.function.__name__ + ".")