from src.infrai_client import InfraiClient, InfraiError
from src.property_login import TenantRecord, verify_login


class FakeClient(InfraiClient):
    def __init__(self, error=None):
        self.error = error

    def verify_otp(self, to, code, request_id):
        if self.error:
            raise self.error
        return {"verified": True}


def test_verified_tenant_receives_private_records():
    tenant = TenantRecord("+15550100", ("Boiler check",), ("lease.pdf",), ("2026-10-15",))
    result = verify_login(FakeClient(), tenant, "123456")
    assert result["authenticated"] is True
    assert result["documents"] == ["lease.pdf"]


def test_business_rejection_does_not_become_server_error():
    tenant = TenantRecord("+15550100", (), (), ())
    result = verify_login(FakeClient(InfraiError("CODE_INVALID", {}, 400)), tenant, "000000")
    assert result == {"authenticated": False, "reason": "CODE_INVALID"}
