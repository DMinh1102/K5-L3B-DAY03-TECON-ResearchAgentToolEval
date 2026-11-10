# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 |        |      |       |        | Prompt & Optimization Lead (TV1) |
|   2 | Phạm Quốc Huy | 2A202603897 | huymix2k4@gmail.com | pqhuy454 | Tool Engineering & Testing Lead (TV2) |
|   3 |        |      |       |        | Evaluation, UI & Live Demo Lead (TV3) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## PhamQuocHuy-2A202603897

### Phần việc phụ trách

- Thành viên 2: Tool Engineering & Testing Lead.
- Nghiên cứu, thiết kế và triển khai mã nguồn 2 công cụ mới (`summarize_text`, `analyze_sentiment`).
- Đăng ký công cụ vào hệ sinh thái của Agent (`starter_v0/tools/__init__.py`) và khai báo Schema trong `starter_v0/artifacts/tools.yaml`.
- Thiết kế bộ Unit Test offline trong `starter_v0/tests/test_tools_todo.py`, đảm bảo toàn bộ hệ thống test contract và test suite đạt 0 failed.
- Soạn thảo tài liệu bàn giao kỹ thuật `HANDOVER_TV1_TV3.md`.

### Đóng góp cụ thể

- Hoàn thành 2 tool mới với đầy đủ `TOOL.md` và `tool.py`, bọc ngoại lệ an toàn, trả về error dict, không raise runtime exception.
- Viết 6 Unit Tests offline bao phủ happy path, bad input (văn bản rỗng, max_sentences âm), và failure path (sai kiểu dữ liệu).
- Đồng bộ Schema vào `tools.yaml` giúp Contract Test đạt **65/65 passed**.
- Soạn thảo 3 test case JSON chuẩn schema cung cấp cho TV3 dán vào `data/eval_group.json`.

### Bằng chứng

- Thư mục mã nguồn tool: `starter_v0/tools/summarize_text/`, `starter_v0/tools/analyze_sentiment/`
- Unit tests: `starter_v0/tests/test_tools_todo.py` (6 passed), `starter_v0/tests/test_tool_contract.py` (65 passed)
- Báo cáo cá nhân: `report/team/2A202603897_PhamQuocHuy.md`
- Tài liệu bàn giao: `HANDOVER_TV1_TV3.md`
