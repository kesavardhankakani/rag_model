import re


def clean_text(raw_text: str) -> str:
    """Normalize document text while preserving useful structure."""
    if raw_text is None:
        return ""

    text = str(raw_text).replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = "".join(ch for ch in text if ch.isprintable() or ch in "\n\t")

    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", text)
    text = re.sub(r"(?<=[A-Za-z0-9])\n(?=[A-Za-z0-9])", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\n\s+\n", "\n\n", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()
