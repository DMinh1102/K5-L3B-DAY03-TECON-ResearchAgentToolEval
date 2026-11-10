"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) (TV2) ----------------
# Tests for summarize_text and analyze_sentiment

def test_summarize_text_happy_path() -> None:
    text = (
        "Trí tuệ nhân tạo đang phát triển với tốc độ chóng mặt trong năm 2026. "
        "Nhiều mô hình ngôn ngữ lớn mới đã xuất hiện và cải thiện đáng kể hiệu suất. "
        "Các nhà nghiên cứu tập trung giải quyết bài toán giảm thiểu ảo giác và nâng cao độ tin cậy. "
        "Doanh nghiệp trên toàn cầu bắt đầu ứng dụng AI sâu rộng vào quy trình sản xuất thực tế."
    )
    result = TOOL_FUNCTIONS["summarize_text"](text=text, max_sentences=2)
    assert result["status"] == "success"
    assert result["summary_sentences_count"] == 2
    assert result["original_sentences_count"] >= 3
    assert result["compression_ratio"] > 0
    assert len(result["summary"]) > 0


def test_summarize_text_bad_input_from_model() -> None:
    # Empty string or only spaces -> returns error dict, does not crash
    empty_res = TOOL_FUNCTIONS["summarize_text"](text="   ", max_sentences=2)
    assert empty_res["status"] == "error"
    assert "error" in empty_res
    assert empty_res["summary"] == ""

    # Invalid max_sentences <= 0 -> fallback safely without crash
    valid_text = "Câu thứ nhất rất hay. Câu thứ hai cũng thế. Câu thứ ba kết luận."
    safe_res = TOOL_FUNCTIONS["summarize_text"](text=valid_text, max_sentences=-1)
    assert safe_res["status"] == "success"
    assert len(safe_res["summary"]) > 0


def test_summarize_text_failure_returns_error_dict() -> None:
    # Model sends wrong type (None or int) -> returns error dict, never raises
    none_res = TOOL_FUNCTIONS["summarize_text"](text=None, max_sentences=3)
    assert none_res["status"] == "error"
    assert "error" in none_res

    int_res = TOOL_FUNCTIONS["summarize_text"](text=12345, max_sentences=3)
    assert int_res["status"] == "error"
    assert "error" in int_res


def test_analyze_sentiment_happy_path() -> None:
    pos_text = "The new breakthrough research is amazing, excellent and very promising for AI future."
    pos_res = TOOL_FUNCTIONS["analyze_sentiment"](text=pos_text)
    assert pos_res["status"] == "success"
    assert pos_res["sentiment"] == "positive"
    assert pos_res["score"] > 0
    assert "amazing" in pos_res["key_indicators"] or "excellent" in pos_res["key_indicators"]

    neg_text = "The product update is terrible, full of critical bugs, failure and disappointing."
    neg_res = TOOL_FUNCTIONS["analyze_sentiment"](text=neg_text)
    assert neg_res["status"] == "success"
    assert neg_res["sentiment"] == "negative"
    assert neg_res["score"] < 0


def test_analyze_sentiment_bad_input_from_model() -> None:
    # Empty string -> returns error dict
    res = TOOL_FUNCTIONS["analyze_sentiment"](text="")
    assert res["status"] == "error"
    assert "error" in res
    assert res["sentiment"] == "neutral"


def test_analyze_sentiment_failure_returns_error_dict() -> None:
    # Non-string input -> returns error dict without raising
    res = TOOL_FUNCTIONS["analyze_sentiment"](text=None)
    assert res["status"] == "error"
    assert "error" in res
    assert res["sentiment"] == "neutral"

