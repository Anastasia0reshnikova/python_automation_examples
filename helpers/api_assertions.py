from requests import Response


def verify_ok_response(response: Response):
    assert response.status_code < 400, f"We expected OK response, but got {response.status_code}"