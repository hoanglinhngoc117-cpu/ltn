"""
Script: test_system.py
Unit tests and pipeline validation
"""
import unittest
from core.semantic_layer import SemanticLayer
from core.guardrails import DataGuardrails, SecurityViolationError
from core.data_profiler import DataProfiler
from core.agent import EnterpriseAnalyticsAgent

class TestAnalyticsAgent(unittest.TestCase):
    def setUp(self):
        self.agent = EnterpriseAnalyticsAgent(db_path="db/enterprise_dw.sqlite")

    def test_semantic_layer(self):
        sem = SemanticLayer()
        intent = sem.parse_intent("Kiểm tra giúp tôi top 5 cửa hàng có tỷ lệ hủy đơn cao nhất hôm qua và nguyên nhân.")
        self.assertEqual(intent["target_metric"], "cancellation_rate")
        self.assertEqual(intent["limit"], 5)
        self.assertIn("orders", intent["mapped_tables"])

    def test_guardrails_blocks_injection(self):
        guard = DataGuardrails("db/enterprise_dw.sqlite")
        with self.assertRaises(SecurityViolationError):
            guard.inspect_ast_and_sanitize("DROP TABLE orders;")
        with self.assertRaises(SecurityViolationError):
            guard.inspect_ast_and_sanitize("DELETE FROM orders WHERE 1=1;")

    def test_pii_masking(self):
        import pandas as pd
        guard = DataGuardrails("db/enterprise_dw.sqlite")
        df = pd.DataFrame([{
            "customer_name": "Nguyễn Văn A",
            "customer_phone": "0912345678"
        }])
        masked = guard.mask_pii(df)
        self.assertNotEqual(masked.iloc[0]["customer_name"], "Nguyễn Văn A")
        self.assertTrue("*" in masked.iloc[0]["customer_phone"])

    def test_end_to_end_pipeline(self):
        res = self.agent.execute(
            user_query="Kiểm tra giúp tôi top 5 cửa hàng có tỷ lệ hủy đơn cao nhất hôm qua và nguyên nhân.",
            user_role="Manager_Region_North"
        )
        self.assertIn("executive_summary", res)
        self.assertIn("charts", res)
        self.assertTrue(res["proactive_alert"]["triggered"])
        analytics = res["pipeline_trace"]["step_4_deep_analytics"]
        self.assertEqual(analytics["top_store"]["store_id"], "STORE_04")
        self.assertGreater(analytics["top_store"]["cancellation_rate"], 15.0)

if __name__ == "__main__":
    unittest.main()
