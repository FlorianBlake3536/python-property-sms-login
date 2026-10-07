from dataclasses import dataclass
from typing import Any

from .infrai_client import InfraiClient, InfraiError


@dataclass(frozen=True)
class TenantRecord:
    phone: str
    maintenance_requests: tuple[str, ...]
    documents: tuple[str, ...]
    inspection_reminders: tuple[str, ...]


def request_login_code(client: InfraiClient, tenant: TenantRecord) -> dict[str, Any]:
    if not tenant.phone.startswith("+"):
        raise ValueError("phone must use an international format")
    return client.send_otp(tenant.phone, f"login:{tenant.phone}")


def verify_login(client: InfraiClient, tenant: TenantRecord, code: str) -> dict[str, Any]:
    try:
        result = client.verify_otp(tenant.phone, code, f"verify:{tenant.phone}:{code}")
    except InfraiError as exc:
        if 400 <= exc.status < 500:
            return {"authenticated": False, "reason": exc.code}
        raise
    return {
        "authenticated": True,
        "tenant_phone": tenant.phone,
        "maintenance_requests": list(tenant.maintenance_requests),
        "documents": list(tenant.documents),
        "inspection_reminders": list(tenant.inspection_reminders),
        "verification": result,
    }
