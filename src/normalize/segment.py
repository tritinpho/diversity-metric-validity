"""Vietnamese word segmentation for token counts.

Vietnamese words span multiple whitespace-separated syllables, so a naive
``text.split()`` overcounts. We use underthesea's word tokenizer; if it is
unavailable we fall back to whitespace counts and flag that downstream so the
metric's provenance is clear.
"""
from __future__ import annotations

import logging

_LOG = logging.getLogger("vnnews.segment")

_TOKENIZER = None
_UNAVAILABLE = False


def _tokenizer():
    global _TOKENIZER, _UNAVAILABLE
    if _TOKENIZER is None and not _UNAVAILABLE:
        try:
            from underthesea import word_tokenize
            _TOKENIZER = word_tokenize
            _LOG.info("underthesea word segmenter loaded")
        except Exception as exc:  # pragma: no cover - import/runtime guard
            _UNAVAILABLE = True
            _LOG.warning("underthesea unavailable (%s); using whitespace fallback", exc)
    return _TOKENIZER


def vi_word_count(text: str | None) -> tuple[int, str]:
    """Return (token_count, method) for ``text``.

    method is 'underthesea' for true Vietnamese segmentation, or 'whitespace'
    when the fallback was used. Empty text -> (0, 'empty').
    """
    if not text or not text.strip():
        return 0, "empty"
    tok = _tokenizer()
    if tok is not None:
        try:
            return len(tok(text)), "underthesea"
        except Exception as exc:  # pragma: no cover
            _LOG.warning("segmentation error (%s); whitespace fallback for one doc", exc)
    return len(text.split()), "whitespace"
