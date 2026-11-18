"""
Script: generate_enterprise_context_data.py
Khởi tạo toàn bộ 5 tập dữ liệu chuẩn cho bài toán Doanh nghiệp Web AI Sinh viên
"""
import json
import os
import pandas as pd

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Danh mục sản phẩm & Bảng giá chuẩn (Product Catalog & Pricing 2026)
product_catalog = [
    {
        "sku": "AI-WRT-01",
        "product_name": "AI Writing Assistant & Grammar Pro",
        "description": "Công cụ AI hỗ trợ viết tiểu luận, chỉnh sửa ngữ pháp, gợi ý cấu trúc học thuật và kiểm tra trùng lặp",
        "target_audience": "Sinh viên khối ngành Xã hội, Kinh tế, Ngoại ngữ",
        "unit_price_monthly": 49000,
        "unit_price_yearly": 490000,
        "min_quantity": 10,
        "effective_date": "2026-01-01"
    },
    {
        "sku": "AI-RES-02",
        "product_name": "AI Research & Paper Summarizer",
        "description": "Trợ lý AI đọc và tóm tắt bài báo khoa học PDF (ArXiv, IEEE), trích xuất citation chuẩn APA/IEEE",
        "target_audience": "Sinh viên làm khóa luận, Nghiên cứu sinh, CLB NCKH",
        "unit_price_monthly": 79000,
        "unit_price_yearly": 790000,
        "min_quantity": 5,
        "effective_date": "2026-01-01"
    },
    {
        "sku": "AI-COD-03",
        "product_name": "AI Code Tutor & Debugger Pro",
        "description": "Gợi ý thuật toán, sửa lỗi code (Python, C++, Java, JS), giải thích lỗi đồ án chuyên ngành CNTT",
        "target_audience": "Sinh viên khối Kỹ thuật, Lập trình, Khoa học dữ liệu",
        "unit_price_monthly": 99000,
        "unit_price_yearly": 990000,
        "min_quantity": 10,
        "effective_date": "2026-01-01"
    },
    {
        "sku": "AI-SLD-04",
        "product_name": "AI Presentation & Slide Generator",
        "description": "Tự động tạo outline, bài thuyết trình PowerPoint/Canva từ nội dung tài liệu học tập trong 30 giây",
        "target_audience": "Toàn thể sinh viên làm bài tập nhóm",
        "unit_price_monthly": 69000,
        "unit_price_yearly": 690000,
        "min_quantity": 10,
        "effective_date": "2026-01-01"
    },
    {
        "sku": "AI-CAMPUS-COMBO",
        "product_name": "Campus All-in-One AI Suite (Trọn gói)",
        "description": "Bộ công cụ đầy đủ 4 trong 1 tích hợp SSO email trường (.edu.vn), có dashboard quản trị cho giảng viên",
        "target_audience": "Khoa / Viện / Trường Đại học mua tập trung",
        "unit_price_monthly": 149000,
        "unit_price_yearly": 199000, # Ưu đãi gói lớn
        "min_quantity": 100,
        "effective_date": "2026-01-01"
    }
]

with open(os.path.join(DATA_DIR, "product_catalog.json"), "w", encoding="utf-8") as f:
    json.dump(product_catalog, f, ensure_ascii=False, indent=2)

# 2. Tồn khả dụng hệ thống (Operational Capacity / Resource Quotas)
operational_capacity = {
    "report_timestamp": "2026-11-17T08:00:00+07:00",
    "gpu_cluster_status": "Healthy (Utilization: 72%)",
    "available_capacity": {
        "AI-WRT-01": {"available_slots": 5200, "status": "In Stock"},
        "AI-RES-02": {"available_slots": 2100, "status": "In Stock"},
        "AI-COD-03": {"available_slots": 850, "status": "Constrained"}, # Đang nghẽn GPU
        "AI-SLD-04": {"available_slots": 3400, "status": "In Stock"},
        "AI-CAMPUS-COMBO": {"available_slots": 1500, "status": "Requires Operations Pre-allocation"}
    },
    "weekly_onboarding_capacity_remaining": 6 # Chỉ onboarding tối đa 6 trường lớn/tuần
}

with open(os.path.join(DATA_DIR, "operational_capacity.json"), "w", encoding="utf-8") as f:
    json.dump(operational_capacity, f, ensure_ascii=False, indent=2)

# 3. Ma trận thời gian triển khai chuẩn (SLA Lead Time Matrix)
sla_lead_time = [
    {"user_range": "1 - 50 tài khoản", "min_lead_time_days": 1, "description": "Tự động cấp phát tài khoản qua email trong 24 giờ"},
    {"user_range": "51 - 200 tài khoản", "min_lead_time_days": 3, "description": "Cấp phát tài khoản hàng loạt theo danh sách Excel của lớp/khoa"},
    {"user_range": "201 - 1,000 tài khoản", "min_lead_time_days": 5, "description": "Cấu hình phân vùng GPU riêng, tài liệu hướng dẫn và demo kỹ thuật"},
    {"user_range": "Trên 1,000 tài khoản", "min_lead_time_days": 10, "description": "Tích hợp xác thực Single Sign-On (Google Workspace/Office 365 .edu.vn)"}
]

with open(os.path.join(DATA_DIR, "sla_lead_time.json"), "w", encoding="utf-8") as f:
    json.dump(sla_lead_time, f, ensure_ascii=False, indent=2)

# 4. Chính sách chiết khấu & Ma trận phân quyền duyệt (Discount & Approval Matrix)
approval_matrix = {
    "discount_tiers": [
        {"tier": "Tier 1", "min_discount": 0, "max_discount": 10, "approver_role": "Sales_Representative", "auto_approve": True, "sla_hours": 0},
        {"tier": "Tier 2", "min_discount": 11, "max_discount": 20, "approver_role": "Sales_Manager (Trưởng phòng KD)", "auto_approve": False, "sla_hours": 4},
        {"tier": "Tier 3", "min_discount": 21, "max_discount": 35, "approver_role": "Executive_Director (Ban Giám Đốc)", "auto_approve": False, "sla_hours": 12}
    ],
    "special_triggers": [
        {"trigger": "SLA_VIOLATION", "condition": "Requested lead time < Standard SLA", "approver": "Operations_Head", "action": "Xác nhận khả năng đáp ứng GPU khẩn cấp"},
        {"trigger": "MISSING_BUDGET", "condition": "Budget is null or below minimum price", "action": "Kích hoạt phản hồi hỏi lại khách hàng (Clarification Email)"},
        {"trigger": "OUTDATED_PRICE", "condition": "Inquiry references legacy price", "action": "Tự động điều chỉnh về Bảng giá 2026 kèm giải thích"}
    ]
}

with open(os.path.join(DATA_DIR, "approval_matrix.json"), "w", encoding="utf-8") as f:
    json.dump(approval_matrix, f, ensure_ascii=False, indent=2)

# 5. Mẫu yêu cầu khách hàng dạng văn bản (Raw Customer Inquiries)
raw_inquiries = [
    {
        "inquiry_id": "INQ-202611-001",
        "received_at": "2026-11-16 08:30:00",
        "channel": "Form Website",
        "sender_name": "TS. Nguyễn Hoàng Nam",
        "sender_email": "nam.nh@hust.edu.vn",
        "organization": "Khoa CNTT - ĐH Bách Khoa Hà Nội",
        "raw_text": "Chào công ty, Khoa chúng tôi đang cần mua tài khoản AI Code Tutor cho 300 sinh viên làm đồ án tốt nghiệp học kỳ 1. Ngân sách dự kiến của Khoa khoảng 25,000,000 VNĐ. Chúng tôi cần triển khai gấp trong vòng 2 ngày tới để kịp sinh viên nộp đề cương. Đề nghị chiết khấu 15% cho khối trường đại học kỹ thuật.",
        "expected_issue": "Yêu cầu gấp 2 ngày (vi phạm SLA chuẩn 5 ngày) + Chiết khấu 15% (vượt quyền Sales Rep, cần Trưởng phòng duyệt)."
    },
    {
        "inquiry_id": "INQ-202611-002",
        "received_at": "2026-11-16 09:15:00",
        "channel": "Email Khách hàng",
        "sender_name": "Bạn Trần Thảo Linh",
        "sender_email": "linhtt.club@neu.edu.vn",
        "organization": "CLB Sinh viên Nghiên cứu Khoa học ĐH Kinh Tế Quốc Dân",
        "raw_text": "Dạ em chào anh/chị, CLB em gồm 50 thành viên muốn mua gói AI Research & Paper Summarizer trong 1 năm để phục vụ đợt thi NCKH cấp Bộ sắp tới. Ngân sách tụi em gom được khoảng 35,000,000 VNĐ. Bên mình có thể xuất hóa đơn tài chính và triển khai trong 5 ngày tới được không ạ?",
        "expected_issue": "Ca chuẩn, đủ ngân sách, đúng SLA, chiết khấu 0% -> Tự động duyệt và sinh bản nháp báo giá ngay."
    },
    {
        "inquiry_id": "INQ-202611-003",
        "received_at": "2026-11-16 11:20:00",
        "channel": "Email Khách hàng",
        "sender_name": "ThS. Lê Minh Quân",
        "sender_email": "quanlm@vnu.edu.vn",
        "organization": "Trường Quốc tế - ĐHQGHN",
        "raw_text": "Trường chúng tôi quan tâm đến bộ giải pháp AI cho sinh viên gồm AI Writing và AI Presentation cho khoảng 600 sinh viên. Chúng tôi chưa chốt được ngân sách chính xác, nhờ bên bạn tư vấn các gói giá ưu đãi nhất và gửi proposal giúp.",
        "expected_issue": "Thiếu ngân sách (Missing budget) -> AI Agent tự động sinh câu hỏi gợi mở xác định ngân sách và đề xuất 2 phương án (Tier ngân sách tối thiểu vs tối ưu)."
    },
    {
        "inquiry_id": "INQ-202611-004",
        "received_at": "2026-11-16 14:40:00",
        "channel": "Form Website",
        "sender_name": "Thầy Vũ Đình Trọng",
        "sender_email": "trongvd@fpt.edu.vn",
        "organization": "Cao đẳng FPT Polytechnic",
        "raw_text": "Chúng tôi cần trang bị Campus All-in-One cho 1,500 sinh viên nhập học đợt tháng 12. Thời hạn cần bàn giao là 15 ngày. Vì số lượng rất lớn, trường đề xuất mức chiết khấu 30% trên tổng giá trị hợp đồng.",
        "expected_issue": "Quy mô lớn 1,500 tài khoản + Chiết khấu 30% (vượt quá 20% của Trưởng phòng, cần chuyển duyệt lên Ban Giám Đốc)."
    }
]

with open(os.path.join(DATA_DIR, "raw_inquiries.json"), "w", encoding="utf-8") as f:
    json.dump(raw_inquiries, f, ensure_ascii=False, indent=2)

print("[OK] Đã tạo thành công 5 bộ dữ liệu chuẩn trong thư mục 'data/'.")
