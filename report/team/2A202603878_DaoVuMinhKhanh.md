# Báo cáo cá nhân — Đào Vũ Minh Khánh - 2A202603878

## 1. Thông tin thành viên

- Họ tên: Đào Vũ Minh Khánh
- MSSV: 2A202603878
- Email: daovuminhkhanh@gmail.com
- Vai trò: Evaluation, UI & Live Demo Lead 

## 2. Phần việc phụ trách

- Thiết kế và chuẩn hóa bộ 10 test case đánh giá của nhóm trong `starter_v0/data/eval_group.json` (5 single-turn và 5 multi-turn).
- Xây dựng và hoàn thiện ứng dụng tương tác Web UI bằng Streamlit (`starter_v0/app.py`).
- Biên soạn Phần A (Mục tiêu, năng lực agent, bảng công cụ, câu hỏi mẫu) trong `report/team/group_report.md` phục vụ Team Showdown.
- Cấu hình phụ thuộc UI trong `starter_v0/requirements.txt` và hỗ trợ thử nghiệm chat live thực tế.

## 3. Đóng góp cụ thể

- **Thiết kế bộ 10 Eval Cases (`eval_group.json`):**
  - Xây dựng 5 case single-turn và 5 case multi-turn bao phủ các kỹ năng: ranh giới an toàn xác nhận (`group_003_send_confirmation`), xử lý ngoài phạm vi (`group_002_out_of_scope`), hỏi lại thông tin thiếu (`group_001_missing_recipient`), định dạng dữ liệu (`group_006`, `group_008`), tra cứu web (`group_007`), và định tuyến chính xác tới 2 công cụ mới của nhóm (`G01_summarize_text_routing`, `G02_analyze_sentiment_routing`, `G06_multiturn_clarify_then_summarize`).
  - Chuẩn hóa cấu trúc lượt thoại (`content` trong mọi turn) và trường kiểm tra `expect`, giúp bộ test chạy hoàn hảo đạt **10/10 PASS (100% Case Accuracy, 0 provider errors)**.
- **Phát triển giao diện Web UI (`app.py`):**
  - Lập trình ứng dụng Streamlit hoàn chỉnh (474 dòng code), kết nối trực tiếp với logic backend của Agent.
  - Thiết kế giao diện trò chuyện trực quan: hiển thị tin nhắn người dùng, luồng suy nghĩ của mô hình, chi tiết từng tool call kèm tham số đối số, và kết quả trả về từ công cụ.
  - Quản lý trạng thái phiên làm việc (`session_state`) mượt mà, hỗ trợ reset hội thoại và cấu hình linh hoạt.
- **Biên soạn Phần A Báo cáo nhóm (`group_report.md`):**
  - Tóm tắt năng lực cốt lõi của Agent (A1), tổng hợp bảng 12 công cụ kèm 2 tool mới (A2), và soạn 4 câu hỏi mẫu minh họa các tình huống tương tác thực tế (A3).

## 4. Bằng chứng

- **File / Run log / Test:**
  - `starter_v0/data/eval_group.json` (Bộ 10 test cases nhóm đạt chuẩn)
  - `starter_v0/app.py` (Mã nguồn ứng dụng Streamlit UI)
  - `starter_v0/requirements.txt` (Đã bổ sung dependency `streamlit>=1.30.0`)
  - `report/team/group_report.md` (Phần A: A1, A2, A3)
  - `starter_v0/runs/v3_B_group_openrouter_20261110T234634581757.json` (File run eval nhóm đạt 10/10 PASS — Accuracy: 1.0)
  - Lịch sử Git commit trên nhánh `DaoVuMinhKhanh` (commit `ad5964c`, `e2378f0`).
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - Công cụ AI: Sử dụng AI Assistant để hỗ trợ dựng khung ứng dụng Streamlit và gợi ý schema kịch bản multi-turn.
  - Cách tự kiểm tra: Chạy `streamlit run app.py` kiểm tra giao diện cục bộ trên cổng 8501; chạy lệnh `python run_eval.py --provider openrouter --version v3 --suite group --eval-cases data/eval_group.json` xác thực 10/10 test cases đều PASS định lượng và 0 lỗi provider.

## 5. Tự đánh giá

- Hoàn thành nhiệm vụ được phân công.
- Xây dựng bộ test eval nhóm chất lượng cao (đạt điểm tuyệt đối 10/10) và ứng dụng UI tương tác hoạt động ổn định, trực quan.
- Tuân thủ liêm chính học thuật, dữ liệu thực nghiệm trung thực.
