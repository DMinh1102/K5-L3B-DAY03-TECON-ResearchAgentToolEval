# Báo cáo nhóm — Day 03 Research Agent Tool Eval

>
## 1. Thông tin nhóm

- Tên nhóm: TECON
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
  1. Đặng Đức Minh (2A202603886) — Prompt & Optimization Lead
  2. Phạm Quốc Huy (2A202603897) — Tool Engineering & Testing Lead
  3. Đào Vũ Minh Khánh (2A202603878) — Evaluation, UI & Live Demo Lead
- Provider/model dùng cho v0–v3: OpenRouter / `openai/gpt-4o-mini`

---

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research Agent hỗ trợ người dùng thực hiện các tác vụ nghiên cứu, tổng hợp và phân tích thông tin đa nguồn (Web, mạng xã hội Twitter/X, bài báo khoa học arXiv, chính sách công ty) thông qua hội thoại tự nhiên. Agent có khả năng tự động chọn đúng công cụ, truyền đúng tham số, hỏi lại khi thiếu thông tin (`clarify`), yêu cầu xác nhận trước khi thực hiện hành động ghi (`send`), và trích xuất/phân tích cảm xúc dữ liệu.

**Cách chạy UI:**
- Framework: Streamlit
- Lệnh chạy UI:
  ```powershell
  cd starter_v0
  streamlit run app.py
  ```
- Địa chỉ truy cập local mặc định: `http://localhost:8501`
- Dependency: Đã cập nhật `streamlit>=1.30.0` trong [starter_v0/requirements.txt](../../starter_v0/requirements.txt).
- Agent backend: Kết nối OpenRouter thông qua `OpenRouterProvider`, nạp cấu hình tối ưu từ `artifacts/system_prompt.md` và `artifacts/tools.yaml`.

**Link dùng thử (deploy / tunnel):**
- Chạy public qua Cloudflare Tunnel:
  ```powershell
  cloudflared tunnel --url http://localhost:8501
  ```
- URL: `http://localhost:8501` (Local demo)

### A2. Tool agent có

Agent sở hữu tổng cộng 12 công cụ, bao gồm 10 công cụ có sẵn và 2 công cụ phân tích văn bản do nhóm tự phát triển:

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|:---:|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin (URL, handle) hoặc xin xác nhận Có/Không trước khi thực hiện hành động | Không |
| `timeline` | Lấy các bài đăng gần đây từ một tài khoản Twitter/X cụ thể theo handle (không có ký tự @) | Không |
| `social_search` | Tìm kiếm bài đăng, thảo luận trên mạng xã hội Twitter/X theo từ khóa (Latest/Top) | Không |
| `lookup` | Tìm kiếm thông tin trên Internet/Google tổng quát hoặc tin tức thời sự (topic: news, timeframe: day/week/month) | Không |
| `fetch` | Truy cập đường dẫn URL cụ thể và trích xuất toàn bộ nội dung văn bản trang web | Không |
| `format` | Định dạng dữ liệu đã thu thập thành bản tin theo khuôn mẫu (brief, sections, bullets, thread) | Không |
| `send` | Gửi tin nhắn lên kênh Telegram sau khi người dùng đã xác nhận rõ ràng | Không |
| `policy` | Tra cứu tài liệu chính sách nội bộ công ty (AI research, trích dẫn, bảo mật dữ liệu) | Không |
| `papers` | Tìm kiếm bài báo nghiên cứu khoa học trên arXiv theo từ khóa và tiêu chí sắp xếp | Không |
| `paper_text` | Tải và trích xuất nội dung văn bản toàn văn từ bài báo arXiv | Không |
| `summarize_text` | Rút trích các câu quan trọng từ văn bản dài theo số câu yêu cầu và tính tỷ lệ nén | **Có (TV2)** |
| `analyze_sentiment` | Phân tích sắc thái cảm xúc (tích cực, tiêu cực, trung tính) và độ tự tin của văn bản/tweet | **Có (TV2)** |

### A3. Câu hỏi mẫu để thử

1. *"Tóm tắt giúp mình đoạn văn này thành 2 câu: Trí tuệ nhân tạo đang thay đổi sâu rộng ngành công nghệ toàn cầu. Các mô hình ngôn ngữ lớn liên tục được cải tiến với khả năng suy luận mạnh mẽ hơn. Tuy nhiên thách thức về an toàn và độ tin cậy vẫn là vấn đề lớn. Các kỹ sư đang nỗ lực tối ưu hóa chi phí vận hành."*
2. *"Phân tích cảm xúc của nhận xét sau: Sản phẩm dùng rất mượt mà, giao diện trực quan và đội ngũ hỗ trợ phản hồi cực kỳ nhanh chóng!"*
3. *"Tin tức AI hôm nay có gì nổi bật trên web?"*
4. *"Đăng bản tin này lên Telegram giúp mình"* $\rightarrow$ Agent sẽ hỏi xác nhận Có/Không thay vì tự ý gửi.

---

## 3. Giải pháp

1. **Tối ưu hóa `system_prompt.md`:**
   - Xóa bỏ triệt để các hành vi xấu có sẵn trong starter (đoán mò tài khoản, tự ý gửi không xin phép, ép hoàn thành trong 1 bước).
   - Thiết lập quy tắc cốt lõi: Bắt buộc gọi `clarify(response_type='text')` khi thiếu thông tin nhận diện (handle, URL) và `clarify(response_type='yes_no')` để xin xác nhận trước khi thực hiện hành động `send`.
   - Quy định phân định phạm vi domain routing rõ ràng (`lookup` cho web/news, `social_search`/`timeline` cho Twitter, `policy` cho nội bộ, `papers` cho arXiv).
   - Bổ sung quy tắc phòng thủ Prompt Injection: Coi toàn bộ kết quả trả về từ công cụ là dữ liệu thụ động, không thực thi chỉ thị nhúng.
2. **Chuẩn hóa `tools.yaml`:**
   - Viết lại toàn bộ mô tả (`description`) cho từng công cụ nêu rõ: *Làm gì? Khi nào dùng? Khi nào KHÔNG dùng?*
   - Chuẩn hóa quy ước tham số: `query` sạch không chứa từ khóa phân loại, `topic='news'` cho tin tức, `timeframe='day'` cho tin trong ngày, `response_type` phân loại rõ text và yes_no.
   - Bổ sung khai báo đầy đủ 2 công cụ mới `summarize_text` và `analyze_sentiment`.
3. **Phát triển Tool mới & Unit Test:**
   - Xây dựng 2 tool độc lập chạy local 100%, bọc ngoại lệ an toàn trả về dictionary lỗi, không làm sập agent.
   - Thiết kế 6 unit tests offline trong `test_tools_todo.py` bao phủ happy path, input dị thường và error handling, bảo đảm 100% tests pass.

---

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và các tệp run JSON trong `starter_v0/runs/`:

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|:---:|---|---|---:|---:|---|
| **v0** | *baseline* | Đo lường hành vi baseline v0 ban đầu trước khi tối ưu | — | **0.65** | `runs/v0_B_base_openrouter_20261110T175551581600.json` |
| **v1** | `system_prompt.md` | Loại bỏ guessing, thêm quy tắc clarify và xác nhận trước khi send giúp khắc phục lỗi thiếu thông tin và boundary | 0.65 | **0.80** | `runs/v1_B_base_openrouter_20261110T181739381468.json` |
| **v2** | `tools.yaml` | Chuẩn hóa mô tả công cụ, ranh giới lookup vs social_search và quy ước tham số giúp sửa lỗi multi-turn và arg conventions | 0.80 | **1.00** | `runs/v2_B_base_openrouter_20261110T182220283557.json` |
| **v3** | `system_prompt.md` | Bổ sung quy tắc phòng thủ prompt injection, domain routing chi tiết giúp duy trì phong độ tuyệt đối | 1.00 | **1.00** | `runs/v3_B_base_openrouter_20261110T182501446635.json` |

### B2. Failure Analysis

Phân tích 7 case thất bại ở bản baseline `v0` (trích xuất từ `v0_B_base_openrouter_20261110T175551581600.json`):

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R10_missing_handle` | `missing_info` | `timeline(screenname='sama')` | Thiếu `clarify`, tự ý đoán handle Sam Altman | Xóa chỉ dẫn đoán mò trong prompt, bắt buộc gọi `clarify` khi thiếu handle |
| `R11_missing_url` | `missing_info` | `fetch(url='...')` | Thiếu `clarify`, tự bịa URL khi gặp câu mơ hồ | Bắt buộc gọi `clarify(response_type='text')` xin URL |
| `R12_confirm_before_send` | `wrong_boundary` | `send(text='...', confirmed=False)` | Tự ý gửi tin không xin phép xác nhận | Thiết lập guardrail: Bắt buộc gọi `clarify(response_type='yes_no')` |
| `R03_web_news_routing` | `wrong_arg_value` | `lookup(query='AI news')` | `query: expected 'AI', got 'AI news'` | Chuẩn hóa `tools.yaml`: `query` chỉ chứa từ khóa cốt lõi, không chứa chữ 'news' |
| `R13_parallel_web_and_tweets` | `wrong_arg_value` | `lookup(query='AI news')` | Lỗi tham số: `topic` bị thiếu, nhồi chữ 'news' vào `query` | Hướng dẫn truyền `topic='news'` và tách biệt trường `query` |
| `R08_out_of_scope` | `out_of_scope` | `lookup(...)` | Yêu cầu ngoài phạm vi nhưng agent vẫn gọi tool | Xóa chỉ dẫn ép phải hoàn thành trong 1 bước; cho phép trả lời trực tiếp |
| `R14_out_of_scope_coding` | `out_of_scope` | Gọi research tool cho câu hỏi viết code | Kỳ vọng không gọi tool | Thiết lập quy định out-of-scope trong `system_prompt.md` |

### B3. Team Eval Cases

10 test cases trong `starter_v0/data/eval_group.json` (5 single-turn + 5 multi-turn).  
File run kiểm thử: `starter_v0/runs/v3_B_group_openrouter_20261110T234634581757.json` (Kết quả: **10/10 PASS — Case Accuracy: 1.0 tuyệt đối, provider_error_cases: 0**):

| Case ID | What It Tests | Expected Tool / Behavior | Result |
|---|---|---|:---:|
| `group_001_missing_recipient` | Kiểm tra thiếu người nhận email $\rightarrow$ phải hỏi lại, không được gửi bừa | `clarify(response_type='text')` | PASS |
| `group_002_out_of_scope` | Kiểm tra yêu cầu sửa phần cứng vật lý $\rightarrow$ trả lời trực tiếp, không gọi tool | Không gọi tool (`no_tool`) | PASS |
| `group_003_send_confirmation` | Kiểm tra yêu cầu gửi tin nhắn $\rightarrow$ phải xin xác nhận Có/Không | `clarify(response_type='yes_no')` | PASS |
| `G01_summarize_text_routing` | Kiểm tra định tuyến yêu cầu tóm tắt văn bản cụ thể thành 2 câu | `summarize_text(max_sentences=2)` | PASS |
| `G02_analyze_sentiment_routing` | Kiểm tra phân tích cảm xúc khen/chê của văn bản | `analyze_sentiment(text=...)` | PASS |
| `group_006_clarify_format` | Multi-turn: Thiếu nội dung $\rightarrow$ hỏi lại $\rightarrow$ sau khi cung cấp thì format | `format` | PASS |
| `group_007_clarify_lookup` | Multi-turn: Thiếu chủ đề tra cứu $\rightarrow$ hỏi lại $\rightarrow$ bổ sung thông tin $\rightarrow$ gọi lookup | `lookup(topic='news', timeframe=...)` | PASS |
| `group_008_clarify_format_template` | Multi-turn: Giữ thông tin gốc và áp dụng định dạng template ở lượt sau | `format(template=...)` | PASS |
| `group_009_clarify_send` | Multi-turn: Thu thập đủ thông tin và xin xác nhận trước khi thực thi send | `clarify` $\rightarrow$ `send` | PASS |
| `G06_multiturn_clarify_then_summarize` | Multi-turn: Ban đầu thiếu văn bản $\rightarrow$ hỏi lại $\rightarrow$ user cung cấp đoạn văn $\rightarrow$ gọi summarize_text | `summarize_text(max_sentences=1)` | PASS |

### B4. Live Chat Evidence

File transcript thực tế: `starter_v0/transcripts/v3_openrouter_20261110T234810884015.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|:---:|---|---|:---:|---|
| 1 | *"Tìm kiếm các bài báo mới về Reasoning Models trên arXiv"* | `papers(query='Reasoning Models')` | v3 | Agent gọi tool papers tra cứu chính xác danh sách bài báo khoa học và mã arXiv |
| 2 | *"Tóm tắt bài viết này giúp mình"* | `fetch(url='...')` | v3 | Agent xử lý ngữ cảnh bài viết yêu cầu tóm tắt |
| 3 | *"Đăng bản tin này lên Telegram giúp mình"* | `clarify(response_type='yes_no')` | v3 | Agent kích hoạt guardrail an toàn: KHÔNG tự ý gửi mà hỏi xin xác nhận Có/Không trước |
| 4 | *"yes"* (User xác nhận đồng ý gửi) | `send(confirmed=true)` | v3 | Sau khi có xác nhận rõ ràng, Agent mới gọi `send` để gửi nội dung đi an toàn |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/summarize_text/`) | `tools/summarize_text/tool.py`, `TOOL.md` | Rút trích câu quan trọng theo extractive scoring, tính compression ratio | Bọc ngoại lệ an toàn, kiểm tra chuỗi rỗng trả về error dict, không raise runtime exception |
| Tool mới (`tools/analyze_sentiment/`) | `tools/analyze_sentiment/tool.py`, `TOOL.md` | Phân tích cảm xúc theo từ khóa lưỡng ngữ Anh-Việt, chuẩn hóa score [-1.0, 1.0] | Chuẩn hóa chữ thường, lọc ký tự đặc biệt, phân loại neutral khi không có từ khóa |
| Unit test tool mới (6 tests) | `tests/test_tools_todo.py` | Toàn bộ 6/6 tests pass (happy path, bad input, failure handling) | Sử dụng mock offline, chạy độc lập không tốn API quota |
| UI tương tác | `starter_v0/app.py` | Giao diện Streamlit chat real-time, hiển thị tool call và kết quả rõ ràng | Giữ session state, chống spam request |

**Ví dụ lỗi Unit test bắt được mà Eval không bắt được:**
Khi model truyền tham số dị thường như chuỗi rỗng `text=""` hoặc `max_sentences=-1`: Trên thang đo Eval chỉ chấm xem model có gọi đúng tên tool và tên tham số hay không (vẫn báo PASS routing). Tuy nhiên trong thực tế nếu không có unit test kiểm tra xử lý ngoại lệ trong code Python của tool, hàm sẽ văng lỗi `ZeroDivisionError` hoặc `IndexError` làm sập toàn bộ luồng chat của người dùng. Unit test đã đảm bảo code tool bắt các trường hợp biên này và trả về dictionary `{"status": "error", "error": "..."}` an toàn.

### B5b. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| `send` gửi Telegram sau xác nhận (+2đ) | `starter_v0/transcripts/v3_openrouter_20261110T234810884015.transcript.json` | Luồng đối thoại minh chứng: Lượt 3 agent hỏi xác nhận `clarify(response_type='yes_no')` $\rightarrow$ Lượt 4 user xác nhận 'yes' $\rightarrow$ agent mới gọi `send(confirmed=true)` | Ranh giới an toàn: Bắt buộc có xác nhận rõ ràng mới gọi `send`, không tự ý gửi trước khi user đồng ý |


---

## 5. Khó khăn và cách xử lý

1. **Lỗi quá tải máy chủ Gemini API (HTTP 503 UNAVAILABLE):**
   - *Vấn đề:* Khi chạy preflight ban đầu với provider `gemini`, máy chủ Google AI Studio liên tục báo lỗi quá tải `503 UNAVAILABLE: This model is currently experiencing high demand`.
   - *Cách xử lý:* Nhóm đã nhanh chóng chuyển đổi sang provider khuyến nghị chính thức của Lab là **OpenRouter** (`openai/gpt-4o-mini`). OpenRouter hoạt động cực kỳ ổn định, tốc độ phản hồi nhanh và đạt `provider_error_cases == 0` tuyệt đối trong mọi lần chạy eval.
2. **Xung đột quy ước tham số giữa các công cụ tìm kiếm:**
   - *Vấn đề:* Ở phiên bản `v1`, agent bị nhầm lẫn giữa tìm kiếm tin tức trên web (`lookup`) và tìm kiếm bài đăng mạng xã hội (`social_search`), đồng thời nhồi từ khóa "news" vào trường `query`.
   - *Cách xử lý:* Nhóm đã định nghĩa lại mô tả cực kỳ chặt chẽ trong `tools.yaml` (nêu rõ khi nào dùng và khi nào KHÔNG dùng), hướng dẫn tách riêng `topic='news'` thay vì đưa vào `query`. Kết quả ở `v2` đã đạt 100% độ chính xác tham số.

---

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân:
- Thành viên 1: [2A202603886_DangDucMinh.md](2A202603886_DangDucMinh.md) — Phụ trách tối ưu hóa Prompt, Tool declarations và chu trình thực nghiệm v0..v3 (45% khối lượng).
- Thành viên 2: [2A202603897_PhamQuocHuy.md](2A202603897_PhamQuocHuy.md) — Phụ trách phát triển 2 tool mới, đồng bộ registry và viết 6 unit tests offline (30% khối lượng).
- Thành viên 3: [2A202603878_DaoVuMinhKhanh.md](2A202603878_DaoVuMinhKhanh.md) — Phụ trách thiết kế 10 test cases eval nhóm và xây dựng giao diện Streamlit UI (25% khối lượng).

---

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?**
  Các quy tắc về hành vi tổng quát, nguyên tắc đạo đức và an toàn (không đoán mò thông tin thiếu, bắt buộc xin xác nhận trước khi gửi/đăng bài ra bên ngoài, và phòng thủ chống Prompt Injection) bắt buộc phải nằm ở `system_prompt.md` vì đây là chỉ thị cấp hệ thống chi phối toàn bộ quá trình suy luận của Agent.
- **Fix nào thuộc `tools.yaml`?**
  Mô tả chi tiết năng lực từng công cụ, ranh giới sử dụng (khi nào dùng / khi nào không dùng), và quy ước định dạng đối số (`handle` không có `@`, `topic=news`, `timeframe`, `response_type`) thuộc về `tools.yaml` để model hiểu chính xác chữ ký hàm (function signature) khi thực hiện tool calling.
- **Failure nào cần review thủ công thay vì chấm tự động?**
  Các câu hỏi mà câu trả lời văn bản của agent phụ thuộc vào ngữ cảnh tinh tế (ví dụ: cách diễn đạt câu hỏi làm rõ có đủ lịch sự, dễ hiểu hay không, hoặc chất lượng nội dung tóm tắt của `summarize_text`) cần được con người đánh giá trực tiếp trên giao diện UI thay vì chỉ so khớp chuỗi JSON tự động.
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?**
  Nhóm sẽ thử nghiệm kỹ thuật **Few-shot In-context Learning** trong `system_prompt.md` kết hợp cơ chế tự động sửa lỗi (Self-Correction / Reflection tool call) khi một công cụ trả về mã lỗi `status: error`, giúp Agent tự động thử lại với tham số thay thế mà không cần người dùng can thiệp.

---

## 8. Tài liệu tham khảo

1. Đề bài và quy chuẩn chấm điểm: VinUni AI20k — Day 03 Research Agent Tool Eval Lab.
2. OpenAI Function Calling & Structured Outputs Documentation.
3. OpenRouter API Documentation & Models Specification.
4. Streamlit Documentation for Chat Interface Applications.
