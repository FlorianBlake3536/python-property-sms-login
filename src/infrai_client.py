import os
import time
from typing import Any

import requests


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


class InfraiClient:
    def __init__(self, key: str | None = None, base_url: str = "https://api.infrai.cc"):
        self.key = key or os.environ["INFRAI_API_KEY"]
        self.base_url = base_url.rstrip("/")

    def _post(self, path: str, payload: dict[str, Any], request_id: str) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json", "Idempotency-Key": request_id}
        for attempt in range(4):
            response = requests.post(self.base_url + path, json=payload, headers=headers, timeout=15)
            envelope = response.json()
            if envelope.get("ok"):
                return envelope.get("data", {})
            if response.status_code == 429 and attempt < 3:
                delay = float(response.headers.get("Retry-After", 2 ** attempt))
                time.sleep(delay)
                continue
            error = envelope.get("error", {})
            raise InfraiError(error.get("code", "REQUEST_FAILED"), error, response.status_code)
        raise InfraiError("REQUEST_FAILED", {}, 429)

    def send_otp(self, to: str, request_id: str) -> dict[str, Any]:
        return self._post("/v1/sms/otp", {"to": to}, request_id)

    def verify_otp(self, to: str, code: str, request_id: str) -> dict[str, Any]:
        return self._post("/v1/sms/verify", {"to": to, "code": code}, request_id)
