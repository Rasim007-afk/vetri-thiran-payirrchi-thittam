from services.sanitizer import sanitize_text


def test_sanitize_text():

    result = sanitize_text(
        "Hello\u2019s  \nTest"
    )

    assert result == (
        "Hello's\nTest"
    )