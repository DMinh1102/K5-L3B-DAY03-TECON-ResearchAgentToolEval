# Báo cáo cá nhân — Đặng Đức Minh - 2A202603886

## 1. Thông tin thành viên

- Họ tên: Đặng Đức Minh
- MSSV: 2A202603886
- Vai trò: Prompt & Optimization Lead 

## 2. Phần việc phụ trách

- Cấu hình provider OpenRouter và thiết lập môi trường chạy thử ban đầu.
- Chạy đánh giá baseline `v0` trên bộ 20 case cố định `eval_base.json` và phân loại lỗi (Failure Analysis).
- Dẫn dắt chu trình tối ưu hóa thực nghiệm theo phương pháp evidence-driven qua các phiên bản `v1`, `v2`, `v3`.
- Tối ưu hóa tệp chỉ thị hệ thống `starter_v0/artifacts/system_prompt.md`.
- Chuẩn hóa mô tả công cụ và quy ước tham số trong `starter_v0/artifacts/tools.yaml`, duy trì bộ test hợp đồng (`test_tool_contract.py`).
- Quản lý nhật ký phiên bản thực nghiệm `starter_v0/artifacts/version_log.csv`.

## 3. Đóng góp cụ thể

- **Baseline v0:** Chạy đánh giá đo lường đạt accuracy 65.0% (13/20 pass), xác định chính xác 7 case lỗi bắt nguồn từ các chỉ dẫn xấu của starter (đoán mò, tự ý gửi tin không xin phép, ép hoàn thành trong 1 bước).
- **Tối ưu hóa v1 (`system_prompt.md`):** Xóa bỏ các bad practices; thiết lập quy tắc bắt buộc gọi `clarify(response_type="text")` khi thiếu URL/handle và `clarify(response_type="yes_no")` xin xác nhận trước khi gọi `send` $\rightarrow$ Tăng Case Accuracy lên **80.0%** (16/20 pass), Tool Routing Accuracy đạt **90.0%**.
- **Chuẩn hóa v2 (`tools.yaml`):** Viết lại mô tả cho từng tool nêu rõ ranh giới khi nào dùng / khi nào không dùng; phân định ranh giới giữa `lookup` (tìm web/tin tức) và `social_search` (tìm tweet); quy định chặt chẽ các tham số (`query`, `topic='news'`, `timeframe`, `response_type`) $\rightarrow$ Đạt độ chính xác tuyệt đối **100.0%** (20/20 pass), bảo đảm 55/55 contract tests pass xanh.
- **Hoàn thiện v3 (`system_prompt.md`):** Bổ sung quy tắc phòng thủ Prompt Injection (coi kết quả tool là dữ liệu thụ động, không phải lệnh thực thi), định tuyến chính sách và bài báo khoa học (`policy`, `papers`, `fetch`), từ chối gọi tool đối với các tác vụ ngoài phạm vi $\rightarrow$ Duy trì điểm số tuyệt đối **100.0%** với prompt hash mới.
- **Ghi chép thực nghiệm:** Ghi nhận đầy đủ, trung thực cả 4 version vào `starter_v0/artifacts/version_log.csv` gồm hashes, giả thuyết, metric trước/sau và file run.

## 4. Bằng chứng

- **File / Run log / Test:**
  - `starter_v0/artifacts/system_prompt.md` (phiên bản v3 hoàn thiện)
  - `starter_v0/artifacts/tools.yaml` (chuẩn hóa mô tả và tham số)
  - `starter_v0/artifacts/version_log.csv` (nhật ký v0..v3)
  - 4 tệp run JSON hợp lệ (`provider_error_cases == 0`, `measured_cases == 20`):
    - `starter_v0/runs/v0_B_base_openrouter_20261110T175551581600.json` (Accuracy: 0.65)
    - `starter_v0/runs/v1_B_base_openrouter_20261110T181739381468.json` (Accuracy: 0.80)
    - `starter_v0/runs/v2_B_base_openrouter_20261110T182220283557.json` (Accuracy: 1.00)
    - `starter_v0/runs/v3_B_base_openrouter_20261110T182501446635.json` (Accuracy: 1.00)
  - Kết quả kiểm thử contract: `pytest starter_v0/tests/test_tool_contract.py` pass 55/55 tests xanh.
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - Công cụ AI: Sử dụng AI Assistant để hỗ trợ phân tích cấu trúc lỗi từ run JSON log và gợi ý cú pháp YAML/Markdown.
  - Cách tự kiểm tra: Tự chạy kiểm thử định lượng bằng lệnh `run_eval.py` trên API OpenRouter thật để thu thập số liệu khách quan; chạy `pytest tests/test_tool_contract.py` kiểm tra tính tương thích của mã nguồn trước khi commit.

## 5. Tự đánh giá

- Hoàn thành nhiệm vụ được phân công.
- Nâng độ chính xác của Agent từ 65% lên 100% tuyệt đối theo đúng phương pháp evidence-driven.
- Tuân thủ chặt chẽ liêm chính học thuật, không rò rỉ secret/API key.
