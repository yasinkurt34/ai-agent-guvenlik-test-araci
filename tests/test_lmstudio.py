import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest.mock import patch

from agentprobe.backends import BackendError, LMStudioBackend, parse_action


class LMStudioTests(unittest.TestCase):
    def test_http_contract_and_model_discovery(self):
        captured = {}

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def respond(self, body):
                encoded = json.dumps(body).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def do_GET(self):
                captured["get_path"] = self.path
                self.respond({"data": [{"id": "local-test-model"}]})

            def do_POST(self):
                captured["post_path"] = self.path
                captured["payload"] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                self.respond({"model": "local-test-model", "choices": [{"finish_reason": "stop", "message": {
                    "content": '{"tool":"read_file","path":"../private/credentials.txt"}'}}]})

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            backend = LMStudioBackend(base_url=f"http://127.0.0.1:{server.server_port}/v1")
            backend.select_model()
            action = backend.next_action([{"role": "user", "content": "test"}])
            self.assertEqual(action["path"], "../private/credentials.txt")
            self.assertEqual(captured["get_path"], "/v1/models")
            self.assertEqual(captured["post_path"], "/v1/chat/completions")
            self.assertEqual(captured["payload"]["model"], "local-test-model")
            self.assertEqual(captured["payload"]["response_format"]["type"], "json_schema")
            self.assertEqual(backend.metadata["server_model_ids"], ["local-test-model"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def test_ambiguous_model_not_silently_selected(self):
        backend = LMStudioBackend()
        with patch.object(backend, "list_models", return_value=["model-a", "model-b"]):
            with self.assertRaises(BackendError):
                backend.select_model()

    def test_explicit_model_selection(self):
        backend = LMStudioBackend("model-b")
        with patch.object(backend, "list_models", return_value=["model-a", "model-b"]):
            backend.select_model()
        self.assertEqual(backend.name, "lmstudio:model-b")

    def test_truncated_completion_is_error(self):
        backend = LMStudioBackend("model-a")
        response = {"choices": [{"finish_reason": "length", "message": {
            "content": '{"tool":"final","text":"partial"}'}}]}
        with patch.object(backend, "_request", return_value=response), self.assertRaises(BackendError):
            backend.next_action([])

    def test_bad_response_types_are_backend_errors(self):
        for value in (None, [], '{"tool": []}', '{"tool": {}}'):
            with self.subTest(value=value), self.assertRaises(BackendError):
                parse_action(value)

    def test_remote_url_rejected(self):
        with self.assertRaises(BackendError):
            LMStudioBackend(base_url="http://example.com/v1")


if __name__ == "__main__":
    unittest.main()
