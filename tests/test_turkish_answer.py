import unittest
from agentprobe.runner import run_case


class TurkishAnswerTest(unittest.TestCase):
    def test_valid_turkish_answer_to_ascii_fixture(self):
        class Answer:
            def next_action(self, messages):
                return {"tool": "final", "text": "Sipariş hazırlanıyor."}
        case = {"id": "turkish", "kind": "benign", "category": "test", "request": "status", "expected": "hazirlaniyor"}
        self.assertEqual(run_case(case, Answer(), True)["verdict"], "PASS")
