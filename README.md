# Hệ Thống AI Analytics Agent (Autonomous BI Agent) - Đồ Án Cuối Môn

Dự án triển khai một **Hệ thống AI Agent phân tích dữ liệu doanh nghiệp tự động (Autonomous Enterprise BI Agent)** chuẩn 6 giai đoạn, giải quyết bài toán chống ảo giác số học (hallucination), bảo vệ an toàn dữ liệu (security guardrails), lọc sạch dữ liệu bẩn (data profiling & quarantine), và sinh báo cáo ra quyết định (actionable insights).

---

## 🏗️ Kiến Trúc Hệ Thống 6 Giai Đoạn

```
[Người dùng / Web App / Lark / Slack]
                 │
                 ▼
 ┌───────────────────────────────────────────────┐
 │ Giai đoạn 1: Tiếp nhận & Hiểu ý định          │
 │ (Entity Extraction + Semantic Layer / Catalog)│
 └───────────────────────┬───────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────┐
 │ Giai đoạn 2: Lập kế hoạch & Truy vấn an toàn  │
 │ (Task Planner + AST Parser + RBAC + PII Mask) │
 └───────────────────────┬───────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────┐
 │ Giai đoạn 3: Làm sạch & Kiểm định dữ liệu     │
 │ (Python Profiling Sandbox + Data Quarantine)  │
 └───────────────────────┬───────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────┐
 │ Giai đoạn 4: Phân tích chuyên sâu & Root-Cause│
 │ (Drill-down + Hourly Trends + POS Discrepancy)│
 └───────────────────────┬───────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────┐
 │ Giai đoạn 5: Trực quan hóa & Sinh Insight     │
 │ (Auto Plotly/SVG Charts + Executive Summary)  │
 └───────────────────────┬───────────────────────┘
                         │
                         ▼
 ┌───────────────────────────────────────────────┐
 │ Giai đoạn 6: Phản hồi đa kênh & Cảnh báo      │
 │ (Proactive Alert + Approval Card + Feedback)  │
 └───────────────────────────────────────────────┘
```

---

## 📂 Cấu Trúc Mã Nguồn

```text
AI Agent_Cuối môn/
│
├── core/                           # Các module cốt lõi của Agent
│   ├── __init__.py
│   ├── semantic_layer.py           # Giai đoạn 1: Từ điển dữ liệu & định nghĩa KPI chuẩn
│   ├── planner.py                  # Giai đoạn 2a: Chia nhỏ truy vấn (Decomposition)
│   ├── guardrails.py               # Giai đoạn 2b: AST Parser, RBAC, PII Masking, Auto-retry
│   ├── data_profiler.py            # Giai đoạn 3: Phát hiện dữ liệu bẩn & cách ly (Quarantine)
│   ├── deep_analytics.py           # Giai đoạn 4: Thống kê chuyên sâu, bóc tách giờ cao điểm & RCA
│   ├── narrative_viz.py            # Giai đoạn 5: Sinh cấu trúc biểu đồ & tóm tắt điều hành
│   ├── delivery_hitl.py            # Giai đoạn 6: Cảnh báo vượt ngưỡng, Approval Card & Feedback
│   └── agent.py                    # Orchestrator kết nối toàn bộ 6 bước thành luồng khép kín
│
├── db/
│   ├── setup_demo_db.py            # Script khởi tạo cơ sở dữ liệu bán lẻ giả lập thực tế
│   └── enterprise_dw.sqlite        # SQLite Data Warehouse
│
├── templates/
│   └── index.html                  # Giao diện Web Dashboard trực quan
│
├── app.py                          # FastAPI Web Server phục vụ API & giao diện
├── main.py                         # CLI Runner chạy trực tiếp kịch bản Demo trên Terminal
├── test_system.py                  # Bộ kiểm thử tự động (Unit tests & Pipeline validation)
└── README.md                       # Tài liệu hướng dẫn đồ án
```

---

## 🚀 Hướng Dẫn Chạy Chương Trình

### 1. Chạy Demo trên Terminal (CLI Mode)
Xem từng bước của Agent được thực thi chi tiết trên console:
```bash
python main.py
```

### 2. Khởi động Giao diện Web Dashboard (Web App)
Khởi chạy máy chủ FastAPI:
```bash
python app.py
```
Mở trình duyệt truy cập: **`http://127.0.0.1:8000`**

Các tính năng trên giao diện:
- **Tùy chọn RBAC Role**: Thử nghiệm với vai trò `Manager_Region_North` (chỉ xem được Miền Bắc) hoặc `Admin_Global` (toàn quyền).
- **Thử nghiệm Prompt**: Có sẵn các nút test nhanh (Prompt mẫu, thử nghiệm tiêm SQL độc hại `DROP TABLE` để thấy AST Guardrail chặn).
- **Xem chi tiết 6 tab**: Tab Insight điều hành, Tab kiểm tra AST/RBAC/PII, Tab Data Quarantine, Tab Deep Analytics.
- **Thẻ phê duyệt tương tác (Approval Card)**: Quản lý ấn phê duyệt khóa SKU và ép đồng bộ POS ngay trên web.
- **Vòng lặp phản hồi (Feedback Loop)**: Đánh giá Like/Dislike được lưu trực tiếp vào database bộ nhớ của Agent.

### 3. Chạy Kiểm Thử Tự Động (Unit Tests)
```bash
python test_system.py
```

---

## 🌟 Điểm Nhấn Kỹ Thuật Đạt Điểm Cao Trong Đồ Án

1. **Khắc phục triệt để ảo giác số học (Deterministic Analytics):** LLM chỉ phụ trách lập kế hoạch và sinh mã truy vấn, toàn bộ phép tính toán số học được giao cho Python Engine & SQL Engine xử lý chuẩn xác 100%.
2. **Lớp bảo vệ dữ liệu đa tầng (Multi-tier Guardrails):**
   - **AST Parser:** Chặn đứng hoàn toàn SQL Injection, lệnh `DROP`, `DELETE`, `UPDATE`.
   - **RBAC Policy:** Tự động tiêm điều kiện phân quyền chi nhánh/vùng miền theo Role của người hỏi.
   - **PII Masking:** Tự động che giấu thông tin cá nhân khách hàng (`T*** A`, `098****07`) trước khi dữ liệu được hiển thị.
3. **Cơ chế Data Quarantine:** Tự động phát hiện và bóc tách các đơn hàng test nội bộ (`is_test = 1`), giá trị âm hoặc trùng lặp ra một bảng cách ly riêng biệt, bảo vệ độ tin cậy của chỉ số kinh doanh.
4. **Phân tích nguyên nhân gốc rễ (Root-Cause Analysis):** Không chỉ trả lời *chuyện gì xảy ra*, Agent tự động đối chiếu chéo giữa đơn hủy và cảnh báo tồn kho để giải thích *tại sao xảy ra* (lệch tồn thực tế vs POS trong khung 17h–19h).
5. **Human-in-the-Loop & Phản hồi chủ động:** Tự động kích hoạt Approval Card khi tỷ lệ hủy > 15%, cho phép người quản lý can thiệp kịp thời.
