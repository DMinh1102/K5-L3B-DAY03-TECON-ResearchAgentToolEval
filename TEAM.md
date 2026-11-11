# Team TECON

## Thông tin nhóm

- Tên nhóm: TECON
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-TECON-ResearchAgentToolEval`
- URL repo: `https://github.com/DMinh1102/K5-L3B-DAY03-TECON-ResearchAgentToolEval`
- Nhánh nộp: `main`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Đặng Đức Minh | 2A202603886 | 26ai.minhdd3@vinuni.edu.vn | DMinh1102 | Prompt & Optimization Lead |
|   2 | Phạm Quốc Huy | 2A202603897 | 26ai.huypq5@vinuni.edu.vn | pqhuy454 | Tool Engineering & Testing Lead |
|   3 | Đào Vũ Minh Khánh | 2A202603878 | 26ai.khanhdvm@vinuni.edu.vn | iamdvmk | Evaluation, UI & Live Demo Lead  |


## Thành viên 1: Đặng Đức Minh - 2A202603886

### Phần việc phụ trách
- Prompt Engineering, chuẩn hóa Tool Declarations và tối ưu hóa thực nghiệm Agent qua các vòng lặp v0 $\rightarrow$ v3.
- Phân tích nguyên nhân lỗi (Failure Analysis) từ baseline v0 và xây dựng các giả thuyết cải tiến dựa trên dữ liệu run JSON thực tế.
- Quản lý nhật ký phiên bản thực nghiệm (`version_log.csv`) và đối soát tính toàn vẹn của hợp đồng công cụ (`test_tool_contract.py`).

### Đóng góp cụ thể
- **Chạy Baseline `v0`:** Chạy bộ test cố định `eval_base.json` (đạt accuracy 65.0%), phân tích chi tiết nguyên nhân gốc rễ của 7 cases thất bại (`R03`, `R08`, `R10`, `R11`, `R12`, `R13`, `R14`).
- **Tối ưu hóa `system_prompt.md` (v1):** Loại bỏ hoàn toàn các chỉ dẫn xấu của bản starter (đoán mò thông tin thiếu, tự ý gửi tin không xin phép, ép hoàn thành trong 1 bước); thiết lập quy tắc bắt buộc gọi `clarify` khi thiếu thông tin và guardrail xác nhận trước khi gọi `send` $\rightarrow$ Nâng Case Accuracy lên **80.0%**, Tool Routing Accuracy lên **90.0%**.
- **Chuẩn hóa `tools.yaml` (v2):** Viết lại mô tả cho từng công cụ nêu rõ khi nào dùng / khi nào không dùng; phân định ranh giới rõ ràng giữa `lookup` (tìm web/tin tức) và `social_search` (tìm bài đăng Twitter/X); quy định chặt chẽ các tham số (`query`, `topic`, `timeframe`, `response_type`) $\rightarrow$ Đạt độ chính xác tuyệt đối **100.0%** (20/20 cases PASS), bảo đảm 55/55 contract tests pass xanh.
- **Hoàn thiện `system_prompt.md` (v3):** Bổ sung quy tắc phòng thủ Prompt Injection (coi kết quả tool là dữ liệu thụ động, không phải lệnh thực thi), định tuyến chính sách và bài báo khoa học (`policy`, `papers`, `paper_text`), từ chối gọi tool với các tác vụ ngoài phạm vi $\rightarrow$ Duy trì điểm số tuyệt đối **100.0%** với hash mới.
- **Ghi chép nhật ký thực nghiệm:** Ghi nhận đầy đủ, trung thực cả 4 version vào `starter_v0/artifacts/version_log.csv`.

### Bằng chứng
- **Tệp kết quả Run JSON hợp lệ (`provider_error_cases == 0`, `measured_cases == 20`):**
  - `starter_v0/runs/v0_B_base_openrouter_20261110T175551581600.json` (Accuracy: 0.65)
  - `starter_v0/runs/v1_B_base_openrouter_20261110T181739381468.json` (Accuracy: 0.80)
  - `starter_v0/runs/v2_B_base_openrouter_20261110T182220283557.json` (Accuracy: 1.00)
  - `starter_v0/runs/v3_B_base_openrouter_20261110T182501446635.json` (Accuracy: 1.00)
- **Tệp mã nguồn & cấu hình đã tối ưu:**
  - `starter_v0/artifacts/system_prompt.md`
  - `starter_v0/artifacts/tools.yaml`
  - `starter_v0/artifacts/version_log.csv`
- **Kết quả kiểm thử hợp đồng:** `pytest starter_v0/tests/test_tool_contract.py` pass 55/55 tests.

---

## Thành viên 2: Phạm Quốc Huy - 2A202603897

### Phần việc phụ trách
- Nghiên cứu, thiết kế và lập trình các công cụ mới (`summarize_text`, `analyze_sentiment`) mở rộng năng lực cho Agent.
- Đăng ký công cụ vào `TOOL_FUNCTIONS` trong `tools/__init__.py` và đồng bộ khai báo Schema trong `tools.yaml`.
- Thiết kế bộ Unit Test offline trong `tests/test_tools_todo.py`, bảo đảm toàn bộ hệ thống vượt qua kiểm thử hợp đồng (`test_tool_contract.py`).

### Đóng góp cụ thể
- Phát triển 2 công cụ mới hoàn chỉnh:
  - `summarize_text`: Trích xuất các câu quan trọng theo tần suất từ và vị trí câu, tính tỷ lệ nén `compression_ratio`, xử lý ngoại lệ an toàn trả về dictionary lỗi nếu văn bản rỗng.
  - `analyze_sentiment`: Phân tích cảm xúc tích cực/tiêu cực/trung tính bằng bộ từ điển Anh-Việt, trả về điểm số `-1.0` đến `+1.0` và danh sách từ khóa chỉ báo.
- Viết 6 Unit Tests offline trong `tests/test_tools_todo.py` bao phủ happy path, bad input và failure handling (6/6 tests pass).
- Soạn thảo tài liệu bàn giao kỹ thuật `HANDOVER_TV1_TV3.md` giúp TV1 và TV3 tích hợp song song mượt mà.

### Bằng chứng
- Mã nguồn tool mới: `starter_v0/tools/summarize_text/` (`tool.py`, `TOOL.md`), `starter_v0/tools/analyze_sentiment/` (`tool.py`, `TOOL.md`).
- Đăng ký công cụ: `starter_v0/tools/__init__.py`.
- Unit tests: `starter_v0/tests/test_tools_todo.py` (6 passed, 0 failed).
- Báo cáo cá nhân: `report/team/2A202603897_PhamQuocHuy.md`.

---

## Thành viên 3: Đào Vũ Minh Khánh - 2A202603878

### Phần việc phụ trách
- Thiết kế bộ 10 Eval Cases cho nhóm trong `data/eval_group.json` (5 single-turn và 5 multi-turn).
- Xây dựng giao diện tương tác người dùng Streamlit Web UI (`starter_v0/app.py`).
- Biên soạn Phần A (Giới thiệu agent, bảng công cụ, câu hỏi mẫu) trong `report/team/group_report.md`.

### Đóng góp cụ thể
- Thiết kế 10 test cases trong `eval_group.json` bao phủ các kỹ năng ranh giới an toàn, out-of-scope, làm rõ thông tin thiếu và định tuyến đến các công cụ mới của nhóm.
- Xây dựng ứng dụng Streamlit UI tương tác thời gian thực với Agent (`app.py`), hiển thị luồng suy nghĩ, tool calling và kết quả thực thi.
- Hoàn thiện Phần A báo cáo nhóm phục vụ giới thiệu agent trong Team Showdown.

### Bằng chứng
- Bộ test eval nhóm: `starter_v0/data/eval_group.json`.
- Mã nguồn ứng dụng UI: `starter_v0/app.py`.
- Báo cáo nhóm (Phần A): `report/team/group_report.md`.
- Báo cáo cá nhân: `report/team/2A202603878_DaoVuMinhKhanh.md`.
