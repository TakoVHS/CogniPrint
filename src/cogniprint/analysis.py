"""Deterministic text profile analysis for local CogniPrint runs."""

from __future__ import annotations

import hashlib
import math
import re
import statistics
from dataclasses import dataclass
from typing import Any

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+(?:[-'][A-Za-zА-Яа-яЁё0-9]+)?", re.UNICODE)
SENTENCE_RE = re.compile(r"[.!?]+")

FINGERPRINT_KEYS = [
    "log_char_count",
    "log_word_count",
    "type_token_ratio",
    "hapax_ratio",
    "avg_word_length",
    "word_length_stddev",
    "avg_sentence_length_words",
    "punctuation_ratio",
    "digit_ratio",
    "uppercase_ratio",
]


@dataclass(frozen=True)
class TextProfile:
    """A compact statistical profile for one text sample."""

    metrics: dict[str, float | int]
    fingerprint: dict[str, float]
    fingerprint_vector: list[float]
    content_hash: str


def analyze_text(text: str) -> TextProfile:
    """Compute deterministic local metrics and a fixed-order profile vector."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    words = WORD_RE.findall(normalized)
    lower_words = [word.lower() for word in words]
    word_lengths = [len(word) for word in words]
    unique_words = set(lower_words)
    frequencies = {word: lower_words.count(word) for word in unique_words}

    char_count = len(normalized)
    non_space_count = sum(1 for char in normalized if not char.isspace())
    letter_count = sum(1 for char in normalized if char.isalpha())
    digit_count = sum(1 for char in normalized if char.isdigit())
    uppercase_count = sum(1 for char in normalized if char.isupper())
    punctuation_count = sum(1 for char in normalized if char in ".,;:!?()[]{}\"'-")
    word_count = len(words)
    sentence_count = max(1, len([part for part in SENTENCE_RE.split(normalized) if part.strip()]))
    unique_word_count = len(unique_words)
    hapax_count = sum(1 for count in frequencies.values() if count == 1)

    avg_word_length = _safe_mean(word_lengths)
    word_length_stddev = statistics.pstdev(word_lengths) if len(word_lengths) > 1 else 0.0
    avg_sentence_length_words = word_count / sentence_count if sentence_count else 0.0
    type_token_ratio = unique_word_count / word_count if word_count else 0.0
    hapax_ratio = hapax_count / word_count if word_count else 0.0

    metrics: dict[str, float | int] = {
        "char_count": char_count,
        "non_space_count": non_space_count,
        "letter_count": letter_count,
        "digit_count": digit_count,
        "punctuation_count": punctuation_count,
        "word_count": word_count,
        "unique_word_count": unique_word_count,
        "sentence_count": sentence_count if normalized.strip() else 0,
        "avg_word_length": round(avg_word_length, 6),
        "word_length_stddev": round(word_length_stddev, 6),
        "avg_sentence_length_words": round(avg_sentence_length_words, 6),
        "type_token_ratio": round(type_token_ratio, 6),
        "hapax_ratio": round(hapax_ratio, 6),
        "punctuation_ratio": round(punctuation_count / non_space_count, 6) if non_space_count else 0.0,
        "digit_ratio": round(digit_count / non_space_count, 6) if non_space_count else 0.0,
        "uppercase_ratio": round(uppercase_count / max(letter_count, 1), 6) if letter_count else 0.0,
    }

    fingerprint = {
        "log_char_count": round(math.log1p(char_count), 6),
        "log_word_count": round(math.log1p(word_count), 6),
        "type_token_ratio": float(metrics["type_token_ratio"]),
        "hapax_ratio": float(metrics["hapax_ratio"]),
        "avg_word_length": float(metrics["avg_word_length"]),
        "word_length_stddev": float(metrics["word_length_stddev"]),
        "avg_sentence_length_words": float(metrics["avg_sentence_length_words"]),
        "punctuation_ratio": float(metrics["punctuation_ratio"]),
        "digit_ratio": float(metrics["digit_ratio"]),
        "uppercase_ratio": float(metrics["uppercase_ratio"]),
    }
    vector = [fingerprint[key] for key in FINGERPRINT_KEYS]
    content_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return TextProfile(metrics=metrics, fingerprint=fingerprint, fingerprint_vector=vector, content_hash=content_hash)


def compare_profiles(left: TextProfile, right: TextProfile) -> dict[str, Any]:
    """Compare two profiles and return conservative distance/similarity signals."""

    left_vector = left.fingerprint_vector
    right_vector = right.fingerprint_vector
    deltas = {
        key: round(right.fingerprint[key] - left.fingerprint[key], 6)
        for key in FINGERPRINT_KEYS
    }
    return {
        "cosine_similarity": round(_cosine(left_vector, right_vector), 6),
        "euclidean_distance": round(_euclidean(left_vector, right_vector), 6),
        "manhattan_distance": round(sum(abs(a - b) for a, b in zip(left_vector, right_vector)), 6),
        "delta_fingerprint": deltas,
        "observed_change": _summarize_delta(deltas),
    }


def _safe_mean(values: list[int]) -> float:
    return statistics.fmean(values) if values else 0.0


def _cosine(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def _euclidean(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def _summarize_delta(deltas: dict[str, float]) -> list[dict[str, float | str]]:
    ranked = sorted(deltas.items(), key=lambda item: abs(item[1]), reverse=True)
    return [
        {"metric": metric, "delta": delta}
        for metric, delta in ranked[:5]
        if delta != 0
    ]
