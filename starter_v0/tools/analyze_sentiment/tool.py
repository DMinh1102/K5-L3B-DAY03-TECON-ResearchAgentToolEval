from __future__ import annotations

import re
from typing import Any

POSITIVE_WORDS = {
    "good", "great", "excellent", "positive", "amazing", "love", "best",
    "impressive", "breakthrough", "success", "promising", "fantastic",
    "awesome", "helpful", "tốt", "tuyệt", "xuất sắc", "thành công",
    "tiềm năng", "ủng hộ", "phát triển", "hay", "đỉnh", "thích", "tiến bộ",
}

NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "negative", "poor", "hate", "worst",
    "failure", "disappointing", "disaster", "bug", "risk", "crisis",
    "flaw", "flawed", "tệ", "xấu", "thất bại", "thất vọng", "lỗi",
    "rủi ro", "khủng hoảng", "ghét", "kém", "dở", "nguy hiểm", "suy thoái",
}


def run(text: str) -> dict[str, Any]:
    """Rule-based sentiment analysis tool for research texts and tweets.

    Safely handles edge cases without raising exceptions.
    """
    try:
        if text is None or not isinstance(text, str):
            return {
                "status": "error",
                "error": "Văn bản đầu vào không hợp lệ hoặc thiếu (phải là chuỗi ký tự).",
                "sentiment": "neutral",
                "score": 0.0,
                "key_indicators": [],
                "word_count": 0,
            }

        cleaned_text = text.strip()
        if not cleaned_text:
            return {
                "status": "error",
                "error": "Văn bản đầu vào rỗng.",
                "sentiment": "neutral",
                "score": 0.0,
                "key_indicators": [],
                "word_count": 0,
            }

        tokens = re.findall(r"\b\w+\b", cleaned_text.lower())
        word_count = len(tokens)

        pos_found = [w for w in tokens if w in POSITIVE_WORDS]
        neg_found = [w for w in tokens if w in NEGATIVE_WORDS]

        pos_count = len(pos_found)
        neg_count = len(neg_found)
        total_sentiment_words = pos_count + neg_count

        if total_sentiment_words == 0:
            score = 0.0
            sentiment = "neutral"
        else:
            raw_score = (pos_count - neg_count) / total_sentiment_words
            score = round(raw_score, 2)
            if score > 0.15:
                sentiment = "positive"
            elif score < -0.15:
                sentiment = "negative"
            else:
                sentiment = "neutral"

        indicators = list(set(pos_found + neg_found))

        return {
            "status": "success",
            "sentiment": sentiment,
            "score": score,
            "key_indicators": indicators,
            "word_count": word_count,
        }

    except Exception as e:
        return {
            "status": "error",
            "error": f"Lỗi phân tích cảm xúc: {str(e)}",
            "sentiment": "neutral",
            "score": 0.0,
            "key_indicators": [],
            "word_count": 0,
        }
