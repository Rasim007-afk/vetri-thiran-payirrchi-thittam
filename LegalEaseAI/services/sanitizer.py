import re


def sanitize_text(text: str) -> str:

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2022": "-",
        "\ufeff": ""
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    # Remove trailing spaces from lines
    text = re.sub(
        r"[ \t]+$",
        "",
        text,
        flags=re.MULTILINE
    )

    return text.strip()