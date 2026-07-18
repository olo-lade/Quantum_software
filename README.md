# 🌌 Quantum Software (QaaS Platform)

> **Author:** Oluwatosin Olalere (GitHub: [olo-lade](https://github.com/olo-lade))
> **License:** [CC BY 4.0](LICENSE) — Credit required for any use or derivative work.

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![Quantum Engine](https://img.shields.io/badge/Quantum-Qiskit-6929C4.svg)](https://qiskit.org)

An open-core **Quantum-as-a-Service (QaaS)** platform. Banks, fintechs, healthcare providers, and any regulated business can plug quantum-grade cryptography, key management, compliance scanning, and threat monitoring into their stack via simple REST endpoints — no quantum physics knowledge required.

---

## 🏗️ Open-Core Architecture

This project follows an **open-core model**:

| Component | Visibility | Description |
|---|---|---|
| Frontend (this repo) | 🟢 Public | Interactive consoles for every API feature |
| API documentation (this repo) | 🟢 Public | Full endpoint reference, request/response shapes |
| Backend core | 🔴 Private | Quantum pipeline, encryption engine, key management, compliance scanner, database layer |
| Infrastructure | 🔴 Private | Docker, Nginx, CI/CD, Terraform, SSL, production `.env` |

The backend is the commercial core. Clients integrate via the **hosted API** — not by running the source.

---

## 🎯 Target Sectors

| Sector | Features Used |
|---|---|
| 🏦 Banking & Fintech | Key management · Threat monitoring · Compliance scanning · Audit logs |
| 🏥 Healthcare | Encryption at rest · GDPR/HIPAA compliance scanner · Audit trail |
| 🔐 Cybersecurity | Quantum key generation · BB84 QKD · OTP encryption · Entropy scoring |
| 🚚 Logistics | QAOA route optimization |
| 📈 Finance | VQE portfolio optimization |
| 🏛️ Legal & Compliance | Privacy scanner · SOC 2 / ISO 27001 audit logs |

---

## ⚛️ API Features

### Cryptography
| Endpoint | Description |
|---|---|
| `POST /quantum/crypto/keygen` | Quantum-random key generation (Hadamard superposition) |
| `POST /quantum/crypto/entropy` | Shannon entropy scoring of quantum randomness |
| `POST /quantum/crypto/otp/encrypt` | Quantum One-Time Pad encryption |
| `POST /quantum/crypto/otp/decrypt` | Quantum OTP decryption |
| `POST /quantum/crypto/bb84` | BB84 Quantum Key Distribution simulation |

### Key Management
| Endpoint | Description |
|---|---|
| `POST /quantum/keys/issue` | Issue a quantum-random key for a client app |
| `POST /quantum/keys/{id}/rotate` | Zero-downtime key rotation |
| `DELETE /quantum/keys/{id}/revoke` | Permanent key revocation |
| `POST /quantum/keys/verify` | Verify key + automatic threat detection |

### Audit & Monitoring
| Endpoint | Description |
|---|---|
| `POST /quantum/audit/query` | Tamper-evident security event log |
| `POST /quantum/monitor/alerts` | Active threat alerts (brute force, replay, revoked key use) |
| `POST /quantum/monitor/resolve/{id}` | Resolve a threat event |

### Compliance
| Endpoint | Description |
|---|---|
| `POST /quantum/compliance/scan` | Scan any public URL for GDPR, CCPA, cookie consent, data retention, breach notification, and 14 other privacy signals |

### Logistics
| Endpoint | Description |
|---|---|
| `POST /quantum/logistics/optimize` | QAOA-inspired multi-city route optimization |

### Finance
| Endpoint | Description |
|---|---|
| `POST /quantum/finance/portfolio` | VQE-inspired portfolio optimization |

---

## 🔑 Authentication

Every request requires an API key in the `X-Api-Key` header.

Register to receive your key:

```bash
curl -X POST https://api.quantumsoftware.io/users \
  -H "Content-Type: application/json" \
  -d '{"email": "you@yourcompany.com"}'
```

```json
{ "user_id": "uuid", "api_key": "your-64-char-hex-key" }
```

Pass the key in every request:
```
X-Api-Key: your-64-char-hex-key
```

---

## 🖥️ Frontend Consoles

Interactive browser consoles for every feature — no code required to test the API:

| Console | URL |
|---|---|
| Landing & Architecture | `frontend/index.html` |
| Cryptography | `frontend/crypto.html` |
| Key Management | `frontend/keys.html` |
| Audit & Monitoring | `frontend/monitor.html` |
| Compliance Scanner | `frontend/compliance.html` |
| Logistics | `frontend/logistics.html` |
| Finance | `frontend/finance.html` |

---

## ⚠️ Rate Limiting

| Tier | Rate Limit |
|---|---|
| Free | 10 requests / minute |
| Pro | Coming soon |
| Enterprise | Coming soon |

---

## 🛡️ Compliance Coverage

The platform is built to support regulated industries out of the box:

| Regulation | Status |
|---|---|
| GDPR | ✅ Deletion, export, anonymisation, encryption at rest |
| NIST SP 800-57 | ✅ Full key lifecycle (issue, rotate, revoke, expiry) |
| SOC 2 Type II | ✅ Audit log, threat detection, retention policy |
| PCI-DSS | ✅ Encryption at rest, key management, audit trail |
| ISO 27001 | ✅ A.12.4 logging, A.9.4 access control, A.10.1 cryptography |
| HIPAA | ⚠️ Partial — TLS + field-level PHI encryption at deployment |
| CCPA | ✅ Opt-out signals, data export, deletion |

---

## 📄 License

Distributed under [CC BY 4.0](LICENSE). You must credit the original author in any use, fork, or derivative work.

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions to the frontend and documentation are welcome.
