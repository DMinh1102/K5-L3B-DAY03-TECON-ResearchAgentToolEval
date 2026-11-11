# Báo cáo cá nhân — PhamQuocHuy-2A202603897


## 1. Thông tin thành viên

- Họ tên: Phạm Quốc Huy
- MSSV: 2A202603897
- Email: huymix2k4@gmail.com

## 2. Phần việc phụ trách

- Nghiên cứu, thiết kế và lập trình các công cụ mới nhằm mở rộng năng lực phân tích cho Research Agent.
- Đăng ký các công cụ vào `TOOL_FUNCTIONS` trong `starter_v0/tools/__init__.py` và đồng bộ khai báo Schema trong `starter_v0/artifacts/tools.yaml`.
- Thiết kế bộ Unit Test offline trong `starter_v0/tests/test_tools_todo.py`, kiểm thử độc lập không phụ thuộc vào LLM hay API bên ngoài, đảm bảo hệ thống vượt qua mọi bài kiểm tra hợp đồng (`test_tool_contract.py`) và không bị lỗi runtime.
- Soạn thảo tài liệu bàn giao kỹ thuật cung cấp prompt rule cho Minh và các test case mẫu cho Khánh để cả nhóm làm việc song song không gián đoạn.

## 3. Đóng góp cụ thể

1. Phát triển 2 Tool mới hoàn chỉnh (Vượt yêu cầu tối thiểu 1 tool của Lab):
   - `summarize_text` (`starter_v0/tools/summarize_text/`):
     - Thuật toán trích xuất extractive scoring dựa trên tần suất từ và vị trí câu để chọn ra các câu đại diện tốt nhất cho đoạn văn bản dài.
     - Tự động tính toán tỷ lệ nén văn bản (`compression_ratio`) và số câu ban đầu/sau tóm tắt.
     - Thiết lập cơ chế an toàn: Bắt mọi ngoại lệ và kiểm tra dữ liệu đầu vào, trả về error dict an toàn nếu văn bản rỗng, không bao giờ raise exception làm sập agent.
     - Viết đầy đủ `TOOL.md` (frontmatter chuẩn) và `tool.py`.
   - `analyze_sentiment` (`starter_v0/tools/analyze_sentiment/`):
     - Phân tích sắc thái cảm xúc (tích cực, tiêu cực, trung tính) cho văn bản hoặc bài đăng mạng xã hội (tweet) bằng hệ thống từ khóa lưỡng ngữ Anh - Việt.
     - Trả về điểm số cảm xúc chuẩn hóa từ `-1.0` đến `+1.0` và trích xuất danh sách các từ thể hiện cảm xúc (`key_indicators`).
     - Viết đầy đủ `TOOL.md` và `tool.py`.

2. Đăng ký công cụ & Khai báo Schema:
   - Import và khai báo `summarize_text` và `analyze_sentiment` trong `starter_v0/tools/__init__.py`.
   - Khai báo Schema JSON chi tiết trong `starter_v0/artifacts/tools.yaml` (nêu rõ mục đích, khi nào nên dùng và khi nào KHÔNG được dùng).

3. Viết 6 Unit Tests offline trong `starter_v0/tests/test_tools_todo.py`:
   - `test_summarize_text_happy_path`: Kiểm tra tóm tắt văn bản chuẩn và tính đúng tỷ lệ nén.
   - `test_summarize_text_bad_input_from_model`: Kiểm tra trường hợp chuỗi rỗng và tham số `max_sentences <= 0`.
   - `test_summarize_text_failure_returns_error_dict`: Kiểm tra khi model truyền sai kiểu dữ liệu (`text=None`, số nguyên) tool trả về dict báo lỗi thay vì crash.
   - `test_analyze_sentiment_happy_path`: Kiểm tra phân loại chính xác văn bản mang sắc thái tích cực và tiêu cực.
   - `test_analyze_sentiment_bad_input_from_model`: Kiểm tra văn bản rỗng trả về trạng thái lỗi an toàn.
   - `test_analyze_sentiment_failure_returns_error_dict`: Kiểm tra xử lý ngoại lệ an toàn khi dữ liệu đầu vào không hợp lệ.

4. Đóng góp vào báo cáo chung:
   - Hoàn thiện mục B5a trong `report/team/group_report.md`.
   - Tạo file `HANDOVER_TV1_TV3.md` chứa sẵn 3 test case JSON chuẩn schema để TV3 dán vào `data/eval_group.json`.

## 4. Bằng chứng

- Danh sách File mã nguồn đã tạo và chỉnh sửa:
  - `starter_v0/tools/summarize_text/TOOL.md` & `tool.py`
  - `starter_v0/tools/analyze_sentiment/TOOL.md` & `tool.py`
  - `starter_v0/tools/__init__.py`
  - `starter_v0/artifacts/tools.yaml`
  - `starter_v0/tests/test_tools_todo.py`
  - `HANDOVER_TV1_TV3.md`
  - `report/team/group_report.md` (Mục B5a)
  - `report/team/2A202603897_PhamQuocHuy.md`
- Kết quả kiểm thử tự động (`pytest`):
  - Chạy `python -m pytest tests/test_tool_contract.py`: **65/65 PASSED** (toàn bộ tool mới khớp hoàn hảo với hợp đồng của hệ thống).
  - Chạy `python -m pytest tests/test_tools_todo.py`: **6 PASSED** cho các tool mới (0 failed).
  - Chạy toàn bộ test suite: **78 PASSED**, 0 FAILED.
- Sử dụng AI & Phương pháp kiểm chứng:
  - Sử dụng trợ lý AI để hỗ trợ thiết kế cấu trúc hàm `tool.py`, gợi ý từ khóa cảm xúc và đề xuất các ca kiểm thử biên (edge cases).
  - Tự kiểm chứng: Tự tay chạy kiểm thử thông qua terminal bằng lệnh `python -m pytest`, trực tiếp kiểm tra giá trị trả về của từng trường hợp ngoại lệ để đảm bảo tính ổn định tuyệt đối khi tích hợp vào Agent.

## 5. Tự đánh giá

- Hoàn thành xây dựng 2 tool mới, viết đầy đủ 6 unit tests offline pass 100%, bảo đảm contract test luôn xanh và chủ động hỗ trợ đồng đội với tài liệu bàn giao hoàn chỉnh.
