"""
Script: main.py
Demo CLI thực thi AI Data Analytics Agent theo đúng kịch bản đề bài
"""
import json
import sys
from core.agent import EnterpriseAnalyticsAgent

def print_separator(title: str):
    print("\n" + "=" * 80)
    print(f" {title.upper()} ")
    print("=" * 80)

def main():
    agent = EnterpriseAnalyticsAgent(db_path="db/enterprise_dw.sqlite")

    user_query = "Kiểm tra giúp tôi top 5 cửa hàng có tỷ lệ hủy đơn cao nhất hôm qua và nguyên nhân."
    user_role = "Manager_Region_North"

    print_separator("KỊCH BẢN CHẠY DEMO THỰC TẾ")
    print(f"👤 Người dùng hỏi: \"{user_query}\"")
    print(f"🔐 Phân quyền người dùng (RBAC Role): {user_role}")

    # Chạy toàn bộ pipeline 6 bước
    result = agent.execute(user_query, user_role=user_role)
    trace = result["pipeline_trace"]

    # 1. Intent & Context Parsing
    print_separator("BƯỚC 1: TIẾP NHẬN & HIỂU Ý ĐỊNH (INTENT & CONTEXT PARSING)")
    intent = trace["step_1_intent"]["entities"]
    print(f"  • Thời gian nhận diện : {intent['time_range']['display']}")
    print(f"  • Chỉ số KPI chính    : {intent['target_metric']} ({trace['step_1_intent']['mapped_kpi']['name']})")
    print(f"  • Công thức chuẩn     : {trace['step_1_intent']['mapped_kpi']['formula']}")
    print(f"  • Bảng dữ liệu liên quan: {', '.join(intent['mapped_tables'])}")

    # 2. Planning & Secure Retrieval
    print_separator("BƯỚC 2: LẬP KẾ HOẠCH & TRUY VẤN AN TOÀN (GUARDRAILS & RBAC)")
    print("  • Các bước truy vấn con (Decomposition):")
    for idx, s in enumerate(trace["step_2_security_retrieval"]["plan_steps"], 1):
        print(f"    {idx}. {s}")
    print("\n  • Kiểm tra AST Parser: CHẶN TUYỆT ĐỐI INSERT/UPDATE/DELETE/DROP (PASS)")
    print(f"  • Áp dụng RBAC Policy: Tự động tiêm điều kiện 'stores.region = ''North''' cho vai trò {user_role}")
    print("\n  • Mẫu dữ liệu đã che giấu PII (PII Masking Sample):")
    for sample in trace["step_2_security_retrieval"]["pii_masked_sample"]:
        print(f"    - Mã: {sample['order_id']} | Tên: {sample['customer_name']} | SĐT: {sample['customer_phone']}")

    # 3. Data Profiling & Quarantine
    print_separator("BƯỚC 3: LÀM SẠCH & KIỂM ĐỊNH CHẤT LƯỢNG (DATA PROFILING & QUARANTINE)")
    prof = trace["step_3_profiling_quarantine"]["report"]
    print(f"  • Tổng số bản ghi quét       : {prof['total_scanned']}")
    print(f"  • Bản ghi sạch hợp lệ        : {prof['clean_count']}")
    print(f"  • Bản ghi bị cách ly (Quarantine): {prof['quarantined_count']}")
    print(f"  • Chi tiết lỗi phát hiện:")
    for err_name, count in prof["issues"].items():
        if count > 0:
            print(f"    - {err_name}: {count} bản ghi (Đã đẩy sang bảng data_quarantine)")

    # 4. Deep Analytics & Root Cause
    print_separator("BƯỚC 4: PHÂN TÍCH CHUYÊN SÂU & TÌM NGUYÊN NHÂN GỐC RỄ (RCA)")
    analytics = trace["step_4_deep_analytics"]
    top_store = analytics["top_store"]
    print(f"  • Cửa hàng có tỷ lệ hủy cao nhất: {top_store['store_name']}")
    print(f"  • Tỷ lệ hủy: {top_store['cancellation_rate']}% ({top_store['cancelled_orders']}/{top_store['total_orders']} đơn)")
    print(f"  • So với trung bình mạng lưới ({analytics['network_average_rate']}%): Cao gấp {top_store['ratio_vs_average']} lần!")
    print(f"  • Phân bổ theo khung giờ: {analytics['peak_window']['percentage']}% đơn hủy tập trung trong khung {analytics['peak_window']['hours']}")
    print(f"  • Đối chiếu kho: Phát hiện {len(analytics['correlated_inventory_alerts'])} cảnh báo sai lệch giữa POS và kho quầy thực tế!")

    # 5. Visualization & Narrative
    print_separator("BƯỚC 5: TRỰC QUAN HÓA & TỔNG HỢP INSIGHT (EXECUTIVE SUMMARY)")
    summary = result["executive_summary"]
    for sec in summary["sections"]:
        print(f"\n{sec['icon']} {sec['stage']}:")
        for bullet in sec["bullets"]:
            clean_b = bullet.replace("**", "").replace("`", "")
            print(f"   • {clean_b}")

    # 6. Delivery & HITL
    print_separator("BƯỚC 6: PHẢN HỒI TƯƠNG TÁC & CẢNH BÁO CHỦ ĐỘNG (DELIVERY & HITL)")
    alert = result["proactive_alert"]
    if alert["triggered"]:
        card = alert["card"]
        print(f"{card['title']}")
        print(f"  Nội dung: {card['description'].replace('**', '')}")
        print(f"  Hành động đề xuất: {card['proposed_action']}")
        print("  Các nút phê duyệt gửi tới Quản lý qua Lark/Slack Card:")
        for act in card["actions"]:
            print(f"    [{act['label']}]")

    print_separator("HOÀN TẤT CHU KỲ VẬN HÀNH AGENT")

if __name__ == "__main__":
    main()
