---
name: summarize_text
track: core
kind: local_formatter
inputs: [text, max_sentences]
outputs: [status, summary, original_sentences_count, summary_sentences_count, compression_ratio]
side_effect: false
requires_confirmation: false
---

# summarize_text

Rút trích tóm tắt các câu quan trọng từ một đoạn văn bản dài để tạo bản tóm tắt súc tích.

## Khi nào nên dùng
- Khi người dùng yêu cầu tóm tắt, rút gọn, hoặc tìm các ý chính từ một đoạn văn bản được cung cấp.
- Khi cần rút ngắn nội dung của bài viết vừa đọc được từ web trước khi đưa vào báo cáo tổng hợp.

## Khi nào KHÔNG dùng
- Khi người dùng muốn tìm kiếm tin tức trên web (dùng `lookup`).
- Khi cần đọc nội dung từ một liên kết URL (dùng `fetch`).
