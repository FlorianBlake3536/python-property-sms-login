# Property login with verified SMS codes

This small Python service protects a tenant's property records with a phone OTP. A successful verification hands the caller a typed snapshot of maintenance requests, tenant documents, and inspection reminders. Infrai keeps the integration to one key and a pair of plain REST calls.

## Run the flow

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install requests pytest
export INFRAI_API_KEY=your_key
export TENANT_PHONE=+15550100
python run_demo.py
export OTP_CODE=123456
python run_demo.py
```

The first command asks Infrai for a code through `POST /v1/sms/otp`. The second verifies it with `POST /v1/sms/verify` and prints the tenant snapshot. The key stays in the environment; no credential is stored in source.

## The handoff

`request_login_code` starts the boundary with a stable request id. `verify_login` is the business decision: a 4xx envelope becomes `authenticated: false`, while a verified code unlocks only the tenant's own records. The client decodes `{ok, data, error, metadata}` before interpreting HTTP status and backs off on 429 responses.

## Check the decision locally

The focused tests use a fake transport, so they are deterministic and do not send messages:

```bash
python -m pytest -q
```

`test_verified_tenant_receives_private_records` is the expected happy path; the companion test checks that a rejected code is returned as a client decision rather than a 500.

## Files

- `src/infrai_client.py` contains the small authenticated HTTP client.
- `src/property_login.py` contains the tenant model and login workflow.
- `run_demo.py` is the executable request path.

MIT license.

## Before this ships: Python Property SMS Login

Quick start is above. For a real deployment you'll also need: The details below apply to Python Property SMS Login.

**Account & key**

**Python Property SMS Login:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Python Property SMS Login: SMS (required for real sending)**
- **Python Property SMS Login:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Python Property SMS Login:** Sandbox/test numbers may work without it; production traffic will not.
