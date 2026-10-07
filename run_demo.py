import os

from src.infrai_client import InfraiClient
from src.property_login import TenantRecord, request_login_code, verify_login


tenant = TenantRecord(
    phone=os.environ.get("TENANT_PHONE", "+15550100"),
    maintenance_requests=("Leaking kitchen tap",),
    documents=("lease-2026.pdf", "insurance.pdf"),
    inspection_reminders=("Annual safety inspection: 2026-10-15",),
)
client = InfraiClient()
request_login_code(client, tenant)
print("OTP requested. Set OTP_CODE to the received value to verify.")
if os.environ.get("OTP_CODE"):
    print(verify_login(client, tenant, os.environ["OTP_CODE"]))
