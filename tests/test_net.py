import httpx

from app.net import status_of


def test_status_of():
    transport = httpx.MockTransport(lambda request: httpx.Response(204))
    assert status_of("https://example.invalid/health", httpx.Client(transport=transport)) == 204
