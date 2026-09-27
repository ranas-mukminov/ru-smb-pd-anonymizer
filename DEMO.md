# Phase-0 public demo (stub) — AEGIS Lite / 152Guard

> **Stub only.** Not a full product implementation. Tracks a public demo path for epic
> [152fz-compliance-as-code#1](https://github.com/ranas-mukminov/152fz-compliance-as-code/issues/1).
> Fake PD below is synthetic — never use real personal data in demos.

## 1) Compose one-liner (planned)

When the Lite API image exists:

```bash
docker compose -f deploy/demo/compose.yaml up --build
# → http://127.0.0.1:8080/health
```

Until then, local CLI dry-run on synthetic CSV:

```bash
pip install -e .
ru-pd-anon profile-dataset examples/data/synthetic_crm.csv
```

## 2) One API call (planned shape)

```bash
curl -sS -X POST http://127.0.0.1:8080/v1/anonymize \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer demo-key' \
  -d '{
    "policy": "analytics",
    "records": [
      {"fio": "Иванов Иван Иванович", "phone": "+7 999 123-45-67", "inn": "7701234567"}
    ]
  }'
# expected (illustrative): masked FIO/phone/INN + audit event id
```

## 3) Fake PD sample (synthetic CRM row)

From [`examples/data/synthetic_crm.csv`](examples/data/synthetic_crm.csv):

| Field | Fake value |
|-------|------------|
| fio | Иванов Иван Иванович |
| passport | 1234 567890 |
| inn | 7701234567 |
| snils | 123-456-789 12 |
| phone | +7 999 123-45-67 |
| email | ivanov@example.com |

**Checklist for backlog (Phase-0 demo path)**

- [ ] Publish `deploy/demo/compose.yaml` + health endpoint
- [ ] Expose `/v1/anonymize` with demo key (rate-limited)
- [ ] Return masked sample + evidence/audit id
- [ ] Link this DEMO.md from product landing (152guard.space)

---

*AEGIS Lite / Run_as_daemon · tracking only — no force-push / no product code in this stub.*
