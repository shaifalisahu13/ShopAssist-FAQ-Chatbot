"""Simple, explainable NLP text preprocessing."""
import re
import nltk
from nltk.tokenize import word_tokenize


def _ensure_tokenizer():
    """Download the small tokenizer resource if it is not already installed."""
    for resource in ("tokenizers/punkt", "tokenizers/punkt_tab"):
        try:
            nltk.data.find(resource)
        except LookupError:
            # If offline, NLTK may be unable to download; the regex fallback below
            # keeps the app usable.
            try:
                nltk.download(resource.split("/")[-1], quiet=True)
            except Exception:
                pass


def preprocess_text(text):
    """
    Lowercase text, tokenize it, and keep words/numbers only.
    Returns a list of tokens. A regex fallback handles missing NLTK data.
    """
    text = (text or "").lower().strip()
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text)

    if not text:
        return []

    try:
        _ensure_tokenizer()
        tokens = word_tokenize(text)
    except Exception:
        tokens = re.findall(r"[a-z0-9']+", text)

    return [token for token in tokens if token.strip()]
