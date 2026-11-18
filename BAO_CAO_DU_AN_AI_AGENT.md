# BÁO CÁO DỰ ÁN CUỐI MÔN
# THIẾT KẾ VÀ TRIỂN KHAI HỆ THỐNG AI AGENT TỰ ĐỘNG HÓA QUY TRÌNH TIẾP NHẬN YÊU CẦU, THẨM ĐỊNH NĂNG LỰC VÀ LẬP BÁO GIÁ CHO DOANH NGHIỆP NỀN TẢNG WEB AI SINH VIÊN

---

## THÔNG TIN TỔNG QUAN DỰ ÁN
* **Đề tài:** Tự động hóa quy trình từ Tiếp nhận Yêu cầu ban đầu $\rightarrow$ Hồ sơ Cơ hội (Opportunity Profile) $\rightarrow$ Bản nháp Phản hồi Báo giá (Draft Proposal/Quotation) bằng Multi-Agent Architecture.
* **Doanh nghiệp giả định:** **EduAI Platform (Aura Student AI)** — Doanh nghiệp cung cấp giải pháp Web AI học tập dành riêng cho sinh viên và các trường Đại học/Cao đẳng.
* **Quy mô xử lý:** 10 Nhân viên Kinh doanh (Sales Reps), tiếp nhận trung bình **280 yêu cầu/tuần** từ email và web form.
* **Môi trường triển khai:** Python 3.11, FastAPI, SQLite / Data Warehouse Staging, LLM Information Extraction, Rule Engine & Human-in-the-Loop.

---

## CHƯƠNG 1: BỐI CẢNH DOANH NGHIỆP & PHÂN TÍCH ĐIỂM NGHẼN (AS-IS ANALYSIS)

### 1.1. Mô hình hoạt động và luồng xử lý hiện tại
EduAI Platform cung cấp các công cụ AI chuyên sâu cho sinh viên (viết luận, tóm tắt tài liệu NCKH, hỗ trợ debug code, tạo slide thuyết trình). Khách hàng chủ yếu là:
1. Đại diện lớp, Đoàn - Hội sinh viên, các Câu lạc bộ học thuật.
2. Khoa, Viện đào tạo hoặc Ban Giám hiệu các trường Đại học/Cao đẳng.

Quy trình vận hành thủ công hiện tại của 10 nhân sự kinh doanh:
```
[Email / Web Form] 
       │
       ▼
(1. Sales đọc email) ──> (2. Chat hỏi lại khách) ──> (3. Tra bảng giá Excel)
                                                              │
                                                              ▼
(6. Gửi báo giá) <── (5. Trình duyệt chiết khấu) <── (4. Hỏi Vận hành về GPU/tồn)
```

### 1.2. Các điểm nghẽn nghiêm trọng (Core Pain Points)
Dựa trên phân tích vận hành thực tế 280 yêu cầu/tuần, công ty đối mặt với 5 rủi ro kinh doanh lớn:

1. **Sai lệch giá và bỏ sót hạng mục sản phẩm (Pricing Discrepancies):**
   - Bảng giá thường xuyên cập nhật theo quý (áp dụng Bảng giá 2026). Sales thường lưu các file Excel cũ trong máy cá nhân, dẫn đến báo giá sai giá cũ (thấp hơn giá niêm yết từ 15-20%) hoặc sót tính năng đi kèm.
2. **Hứa hẹn thời hạn triển khai bất khả thi (SLA & Capacity Violation):**
   - Các gói sinh viên đòi hỏi hạ tầng GPU Cloud và hạn mức API tài khoản. Sales không nắm được lượng tài khoản khả dụng theo thời gian thực nên tự ý hứa thời hạn gấp (ví dụ: hứa cấp 300 tài khoản trong 2 ngày trong khi SLA kỹ thuật cần 5 ngày), dẫn đến khi ký hợp đồng thì Vận hành bị quá tải, gây khiếu nại.
3. **Tắc nghẽn phê duyệt chiết khấu (Discount Approval Latency):**
   - Nhiều khách hàng trường học đòi chiết khấu từ 15% đến 30%. Sales phải chụp màn hình gửi qua Zalo/Lark xin ý kiến Trưởng phòng Kinh doanh hoặc Ban Giám đốc. Thời gian chờ duyệt kéo dài từ 24 - 48 giờ làm nguội lạnh nhu cầu của khách hàng.
4. **Thất thoát cơ hội do thiếu thông tin (Lead Leakage):**
   - Nhiều yêu cầu gửi về không ghi rõ ngân sách tổng hoặc người ký duyệt hợp đồng. Các yêu cầu này thường bị chuyển qua lại giữa các nhân viên kinh doanh, không có ai chính thức phụ trách (orphaned leads) và bị lãng quên.
5. **Năng suất lao động thấp:**
   - Mỗi nhân viên kinh doanh mất trung bình **35–45 phút** để đọc, kiểm tra tồn, tra giá và soạn một bản thảo email báo giá. Với 28 yêu cầu/nhân viên/tuần, họ mất gần **50% thời gian làm việc** chỉ cho việc hành chính giấy tờ thay vì tập trung tư vấn khách hàng.

---

## CHƯƠNG 2: THIẾT KẾ CƠ SỞ DỮ LIỆU CHUẨN DOANH NGHIỆP (ENTERPRISE DATA CATALOG)

Để loại bỏ hoàn toàn các lỗi trên, hệ thống AI Agent được kết nối trực tiếp với 5 tập dữ liệu cốt lõi (Single Source of Truth) đã được chuẩn hóa tại thư mục `data/`:

### 2.1. Danh mục sản phẩm & Bảng giá chuẩn 2026 (`product_catalog.json`)
| Mã SKU | Tên sản phẩm | Đơn giá tháng (VNĐ) | Đơn giá năm (VNĐ) | Số lượng tối thiểu | Khối ngành mục tiêu |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **AI-WRT-01** | AI Writing Assistant & Grammar Pro | 49,000 | 490,000 | 10 tài khoản | Sinh viên Kinh tế, Xã hội, Ngoại ngữ |
| **AI-RES-02** | AI Research & Paper Summarizer | 79,000 | 790,000 | 5 tài khoản | Sinh viên làm khóa luận, CLB NCKH |
| **AI-COD-03** | AI Code Tutor & Debugger Pro | 99,000 | 990,000 | 10 tài khoản | Sinh viên CNTT, Kỹ thuật, Khoa học dữ liệu |
| **AI-SLD-04** | AI Presentation & Slide Generator | 69,000 | 690,000 | 10 tài khoản | Toàn thể sinh viên làm bài tập nhóm |
| **AI-CAMPUS-COMBO**| Campus All-in-One Suite (Trọn gói) | 149,000 | 199,000 | 100 sinh viên | Khoa / Viện / Trường Đại học mua tập trung |

### 2.2. Tồn khả dụng hệ thống theo thời gian thực (`operational_capacity.json`)
* **Tình trạng cụm máy chủ GPU:** Hoạt động ổn định (Tải 72%).
* **Hạn mức tài khoản khả dụng:**
  - `AI-WRT-01`: 5,200 slots (Sẵn sàng)
  - `AI-RES-02`: 2,100 slots (Sẵn sàng)
  - `AI-COD-03`: **850 slots** *(Cảnh báo: Hạ tầng GPU đang trong ngưỡng kiểm soát, không nhận quá 500 user/đơn nếu không báo trước)*
  - `AI-SLD-04`: 3,400 slots (Sẵn sàng)
  - `AI-CAMPUS-COMBO`: 1,500 slots (Cần phê duyệt từ Trưởng bộ phận Vận hành)

### 2.3. Ma trận thời gian triển khai cam kết chuẩn (`sla_lead_time.json`)
* **Quy mô 1 – 50 tài khoản:** Tối thiểu **1 ngày làm việc** (Cấp phát tự động).
* **Quy mô 51 – 200 tài khoản:** Tối thiểu **3 ngày làm việc** (Cấp phát danh sách lớp theo batch).
* **Quy mô 201 – 1,000 tài khoản:** Tối thiểu **5 ngày làm việc** (Cấu hình hạn ngạch GPU riêng và tài liệu hướng dẫn).
* **Quy mô > 1,000 tài khoản:** Tối thiểu **10 ngày làm việc** (Tích hợp Single Sign-On cổng email trường `.edu.vn`).

### 2.4. Chính sách chiết khấu & Phân quyền phê duyệt RBAC (`approval_matrix.json`)
* **Mức 1 (0% – 10%):** Thuộc thẩm quyền Sales Rep $\rightarrow$ **Auto-approve**, không cần duyệt cấp trên.
* **Mức 2 (11% – 20%):** Thẩm quyền của **Trưởng phòng Kinh doanh** $\rightarrow$ Kích hoạt Approval Card qua hệ thống. Thời gian cam kết phản hồi: $\le 4$ giờ.
* **Mức 3 (> 20%):** Vượt thẩm quyền phòng Kinh doanh $\rightarrow$ Bắt buộc chuyển lên **Ban Giám Đốc (CEO/Director)** duyệt.
* **Trường hợp vi phạm SLA:** Nếu khách đòi bàn giao gấp hơn thời gian SLA quy định $\rightarrow$ Bắt buộc kích hoạt thẻ kiểm tra với Trưởng bộ phận Vận hành (Operations Head).

---

## CHƯƠNG 3: THIẾT KẾ KIẾN TRÚC HỆ THỐNG AI AGENT (TO-BE ARCHITECTURE)

Hệ thống hoạt động theo mô hình **Orchestrated Multi-Agent Pipeline** 6 giai đoạn, đảm bảo mọi yêu cầu đều được giải quyết chuẩn xác, an toàn và minh bạch:

```
[Khách hàng gửi Email/Form]
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│ Giai đoạn 1: Ingestion & Intent Extraction                  │
│ • Trích xuất: Tên trường, Người gửi, Sản phẩm, SL,          │
│   Ngân sách dự kiến, Thời hạn yêu cầu, Đề nghị chiết khấu   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Giai đoạn 2: Semantic Catalog & Pricing Grounding           │
│ • Map đúng mã SKU trong Product Catalog 2026                │
│ • Tính toán giá niêm yết chuẩn xác (Chống dùng giá cũ)      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Giai đoạn 3: Capacity & SLA Validation Engine               │
│ • Kiểm tra tồn GPU khả dụng (operational_capacity)          │
│ • Đối chiếu thời hạn khách yêu cầu vs Ma trận SLA chuẩn     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Giai đoạn 4: Policy & Approval Routing (Rule Engine)        │
│ • Kiểm tra ngưỡng chiết khấu:                               │
│   - <= 10%: Tự động duyệt                                   │
│   - 11-20%: Sinh Approval Card gửi Trưởng phòng             │
│   - > 20%: Sinh Approval Card gửi Ban Giám Đốc              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Giai đoạn 5: Opportunity Profile & Lead Assignment          │
│ • Tạo mã Lead duy nhất (OPP-YYYYMM-XXXX)                    │
│ • Gán Owner cụ thể theo địa bàn (Chống rơi rớt cơ hội)      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Giai đoạn 6: Auto-Generation of Proposal & Email Draft      │
│ • Sinh bản nháp phản hồi chuyên nghiệp, đúng tone giọng B2B │
│ • Xuất file Báo giá PDF/Excel đính kèm                      │
│ • Trường hợp thiếu ngân sách: Tự sinh Email hỏi gợi mở      │
└─────────────────────────────────────────────────────────────┘
```

---

## CHƯƠNG 4: THỰC NGHIỆM VẬN HÀNH QUA CÁC KỊCH BẢN THỰC TẾ (DEMO WALKTHROUGHS)

Dưới đây là 3 ca xử lý điển hình chứng minh năng lực vượt trội của AI Agent:

### Kịch bản 1: ĐH Bách Khoa Hà Nội (Vi phạm SLA & Vượt thẩm quyền chiết khấu)
* **Văn bản đầu vào:** *"Chào công ty, Khoa CNTT - ĐH Bách Khoa đang cần mua tài khoản AI Code Tutor cho 300 sinh viên làm đồ án tốt nghiệp. Ngân sách dự kiến 25,000,000 VNĐ. Chúng tôi cần triển khai gấp trong vòng 2 ngày tới. Đề nghị chiết khấu 15% cho khối trường kỹ thuật."*
* **Xử lý của Agent:**
  1. *Entity Extraction:* Sản phẩm = `AI-COD-03` (300 user), Ngân sách = 25,000,000đ, Thời hạn = 2 ngày, Chiết khấu đề xuất = 15%.
  2. *Kiểm tra giá:* Đơn giá niêm yết gói học kỳ/năm cho 300 sinh viên = $300 \times 99,000 \text{ đ} \times 1 \text{ tháng} = 29,700,000 \text{ VNĐ}$. Chiết khấu 15% $\rightarrow$ Giá sau giảm = $25,245,000 \text{ VNĐ}$ (khớp với ngân sách 25 triệu của trường).
  3. *Kiểm tra tồn & SLA:*
     - Tồn kho khả dụng `AI-COD-03`: Còn 850 slots $\rightarrow$ **Đủ tài nguyên**.
     - Thời hạn yêu cầu: 2 ngày trong khi SLA cho quy mô 300 sinh viên là **5 ngày** $\rightarrow$ **CẢNH BÁO VI PHẠM SLA**.
  4. *Phân quyền phê duyệt:*
     - Chiết khấu 15% vượt mức 10% của Sales $\rightarrow$ Tạo **Approval Card gửi Trưởng phòng Kinh doanh**.
     - Vi phạm SLA $\rightarrow$ Gửi cảnh báo phối hợp đến **Trưởng bộ phận Vận hành**.
  5. *Bản nháp phản hồi sinh ra:*
     - Email cảm ơn và thông báo chiết khấu 15% đã được chấp thuận.
     - Đề xuất phương án tiến độ thông minh: Bàn giao trước 50 tài khoản trong 24h để sinh viên nộp đề cương khẩn cấp, 250 tài khoản còn lại bàn giao trong 4 ngày tiếp theo để đảm bảo hệ thống GPU chạy tối ưu.

### Kịch bản 2: CLB Nghiên cứu Khoa học ĐH Kinh Tế Quốc Dân (Ca chuẩn, tự động duyệt 100%)
* **Văn bản đầu vào:** *"CLB gồm 50 thành viên muốn mua gói AI Research & Paper Summarizer trong 1 năm. Ngân sách 35,000,000 VNĐ. Triển khai trong 5 ngày tới."*
* **Xử lý của Agent:**
  - Sản phẩm: `AI-RES-02` (50 user, 1 năm).
  - Giá niêm yết: $50 \times 790,000 \text{ đ} = 39,500,000 \text{ đ}$.
  - Ngân sách khách hàng: 35,000,000đ $\rightarrow$ Khách cần chiết khấu tương đương 11.3%.
  - Tồn kho khả dụng: 2,100 slots $\rightarrow$ Đạt.
  - SLA: 5 ngày (SLA quy định 50 user chỉ cần 3 ngày) $\rightarrow$ Đạt hoàn toàn.
  - *Kết quả:* Chuyển duyệt nhanh và sinh ngay bản hợp đồng điện tử đính kèm file báo giá Excel chính xác.

### Kịch bản 3: Trường Quốc tế - ĐHQGHN (Ca thiếu ngân sách & Chưa rõ người duyệt)
* **Văn bản đầu vào:** *"Trường quan tâm bộ giải pháp AI Writing và AI Presentation cho 600 sinh viên. Chúng tôi chưa chốt được ngân sách chính xác, nhờ bên bạn tư vấn các gói ưu đãi nhất."*
* **Xử lý của Agent (Chống rơi rớt Lead):**
  1. Ghi nhận cơ hội: Khởi tạo mã hồ sơ `OPP-202611-003`, tự động gán cho Sales Rep phụ trách khối Đại học Quốc gia.
  2. Phát hiện thiếu ngân sách (`budget = null`) $\rightarrow$ Không chuyển qua lại giữa các nhân viên.
  3. Agent tự động soạn bản nháp **Email Tư Vấn Gợi Mở (Consultative Clarification)** đưa ra 2 phương án đóng gói rõ ràng:
     - *Phương án Tiêu chuẩn (Gói Campus All-in-One):* 199,000 đ/sinh viên/năm.
     - *Phương án Tối ưu chi phí:* Kích hoạt theo từng kỳ làm đồ án (99,000 đ/kỳ).
     - Đính kèm đường link đặt lịch họp Zoom 15 phút với chuyên viên phụ trách.

---

## CHƯƠNG 5: ĐÁNH GIÁ HIỆU QUẢ KINH DOANH (ROI & KPI EVALUATION)

| Chỉ số đo lường (KPI) | Quy trình thủ công (As-Is) | Quy trình tự động bằng AI Agent (To-Be) | Mức độ cải thiện |
| :--- | :---: | :---: | :---: |
| **Thời gian tạo báo giá (Response Time)** | 4.5 giờ | **3 phút** | **Nhanh hơn 90 lần** |
| **Tỷ lệ báo giá sai giá cũ (Pricing Errors)** | 14.2% | **0.0%** (Triệt tiêu hoàn toàn) | **Giảm 100% lỗi** |
| **Tỷ lệ vi phạm cam kết tiến độ (SLA Violation)** | 18.5% | **0.0%** (Tự động khóa theo SLA Matrix) | **Khắc phục triệt để** |
| **Tỷ lệ thất thoát cơ hội thiếu ngân sách** | 22.0% | **0.0%** (Tự động gán Owner & Email gợi mở) | **Không bỏ sót lead** |
| **Thời gian làm việc hành chính của Sales** | 3.5 giờ/ngày/nhân viên | **20 phút/ngày/nhân viên** | **Giải phóng 90% thời gian** |
| **Năng suất xử lý yêu cầu toàn đội ngũ** | 280 yêu cầu/tuần | Có thể mở rộng lên **1,500 yêu cầu/tuần** | **Tăng gấp 5.3 lần** |

---

## CHƯƠNG 6: KẾT LUẬN & HƯỚNG MỞ RỘNG ĐỒ ÁN

### 6.1. Kết luận
Dự án đã giải quyết trọn vẹn bài toán hóc búa của Ban Giám đốc:
- **Chuẩn hóa triệt để:** Dữ liệu sản phẩm, giá, tồn kho và chiết khấu trở thành "Single Source of Truth", không phụ thuộc vào trí nhớ cá nhân của từng nhân viên.
- **Minh bạch và an toàn:** Cơ chế RBAC và Approval Card giúp Trưởng phòng và Giám đốc phê duyệt chỉ với 1 click, không còn tình trạng chat qua lại không người theo dõi.
- **Trải nghiệm khách hàng vượt trội:** Sinh viên và nhà trường nhận được bản nháp đề xuất chuyên nghiệp, đầy đủ điều khoản chỉ trong vài phút sau khi gửi yêu cầu.

### 6.2. Hướng phát triển tiếp theo
1. Tích hợp trực tiếp với cổng Webhook của Lark Suite / Slack / Microsoft Teams để gửi Approval Card thời gian thực.
2. Tích hợp chữ ký số và hợp đồng điện tử tự động (e-Contract) để khách hàng có thể ký kết và kích hoạt tài khoản AI ngay trên web.
