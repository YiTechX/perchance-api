import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from api.index import app


class TestPerchanceApi(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("status"), "online")
        self.assertIn("/v1/images/generations", data.get("endpoints", []))

    def test_health_endpoint(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("status"), "ok")

    def test_list_models(self):
        resp = self.client.get("/v1/models")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("data", data)
        model_ids = [m["id"] for m in data["data"]]
        self.assertIn("perchance", model_ids)
        self.assertIn("perchance-cinematic", model_ids)

    def test_generate_validation_error(self):
        resp = self.client.post("/v1/images/generations", json={"prompt": ""})
        self.assertEqual(resp.status_code, 400)

    @patch("api.index.generator_client.generate")
    def test_generate_success(self, mock_generate):
        mock_generate.return_value = ["iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="]

        resp = self.client.post("/v1/images/generations", json={
            "prompt": "a test cute dog",
            "model": "perchance-cinematic",
            "size": "1024x1024",
            "response_format": "b64_json"
        })

        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("data", data)
        self.assertEqual(len(data["data"]), 1)
        self.assertIn("b64_json", data["data"][0])


if __name__ == "__main__":
    unittest.main()
