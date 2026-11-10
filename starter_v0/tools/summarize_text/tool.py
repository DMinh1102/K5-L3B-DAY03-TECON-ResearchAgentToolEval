from __future__ import annotations

import re
from typing import Any


def run(text: str, max_sentences: int = 3) -> dict[str, Any]:
    """Extractive summarization tool that extracts top informative sentences.

    Safely handles edge cases without raising exceptions.
    """
    try:
        # 1. Input validation & edge cases
        if text is None or not isinstance(text, str):
            return {
                "status": "error",
                "error": "Văn bản đầu vào không hợp lệ hoặc thiếu (phải là chuỗi ký tự).",
                "summary": "",
                "original_sentences_count": 0,
                "summary_sentences_count": 0,
                "compression_ratio": 0.0,
            }

        cleaned_text = text.strip()
        if not cleaned_text:
            return {
                "status": "error",
                "error": "Văn bản đầu vào rỗng.",
                "summary": "",
                "original_sentences_count": 0,
                "summary_sentences_count": 0,
                "compression_ratio": 0.0,
            }

        # Normalize max_sentences
        if not isinstance(max_sentences, int) or max_sentences <= 0:
            target_sentences = 3
        else:
            target_sentences = max_sentences

        # 2. Split sentences
        raw_sentences = re.split(r"(?<=[.!?\n])\s+", cleaned_text)
        sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 3]

        if not sentences:
            sentences = [cleaned_text]

        original_count = len(sentences)

        # 3. Frequency-based extractive scoring
        words = re.findall(r"\b\w+\b", cleaned_text.lower())
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "is", "was", "are", "were", "it", "this", "that", "là",
            "và", "của", "cho", "với", "trong", "đã", "đang", "sẽ", "những", "các",
            "có", "được", "tại", "về", "như", "một", "này", "thì", "khi",
        }
        word_freq: dict[str, int] = {}
        for w in words:
            if w not in stop_words and len(w) > 1:
                word_freq[w] = word_freq.get(w, 0) + 1

        # Score sentences
        def score_sentence(idx: int, sentence: str) -> float:
            s_words = re.findall(r"\b\w+\b", sentence.lower())
            score = sum(word_freq.get(w, 0) for w in s_words)
            # Bonus for position: early sentences are often topic sentences
            position_multiplier = 1.2 if idx == 0 else 1.0
            return (score / max(len(s_words), 1)) * position_multiplier

        scored_sentences = [(idx, score_sentence(idx, s), s) for idx, s in enumerate(sentences)]

        # Sort by score descending and take top N
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        chosen = scored_sentences[:target_sentences]

        # Re-sort chosen sentences by original appearance order
        chosen.sort(key=lambda x: x[0])
        summary_sentences = [item[2] for item in chosen]
        summary_text = " ".join(summary_sentences)

        orig_char_len = len(cleaned_text)
        sum_char_len = len(summary_text)
        compression_ratio = round(max(0.0, 1.0 - (sum_char_len / max(orig_char_len, 1))), 2)

        return {
            "status": "success",
            "summary": summary_text,
            "original_sentences_count": original_count,
            "summary_sentences_count": len(summary_sentences),
            "compression_ratio": compression_ratio,
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Lỗi xử lý tóm tắt: {str(e)}",
            "summary": "",
            "original_sentences_count": 0,
            "summary_sentences_count": 0,
            "compression_ratio": 0.0,
        }
