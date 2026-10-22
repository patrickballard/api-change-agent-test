"""Plain HTTP helpers.

Uses httpx directly but never declares it: openai 1.x/2.x happened to
install it, so this worked until openai 3.0.
"""
import httpx


def status_of(url: str, client: httpx.Client | None = None) -> int:
    with client or httpx.Client(timeout=5) as c:
        return c.get(url).status_code
