---
name: analyze_sentiment
track: core
kind: local_formatter
inputs: [text]
outputs: [status, sentiment, score, key_indicators, word_count]
side_effect: false
requires_confirmation: false
---

# analyze_sentiment

Phân tích cảm xúc và sắc thái thái độ (tích cực, tiêu cực, trung tính) của bài viết, bình luận, hoặc tweet.

## Khi nào nên dùng
- Khi người dùng muốn biết phản ứng hoặc cảm xúc của cộng đồng/bài viết về một công nghệ, sản phẩm hoặc sự kiện.
- Khi cần đánh giá xu hướng dư luận từ các bài đăng mạng xã hội vừa tìm được.

## Khi nào KHÔNG dùng
- Khi người dùng chỉ hỏi sự thật khách quan hoặc tin tức thông thường không yêu cầu đánh giá thái độ.
- Khi cần trích xuất tóm tắt nội dung dài (dùng `summarize_text`).
