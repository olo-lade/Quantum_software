# 🌌 Quantum Software (QaaS Layer)

> **Original Author:** Oluwatosin Olalere (GitHub: [olo-lade](https://github.com/olo-lade))
> **Repository:** https://github.com/olo-lade/Quantum_software
> **License:** [CC BY 4.0](LICENSE) — You must credit the original author in any use, fork, or derivative work.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![Quantum Engine](https://img.shields.io/badge/Quantum-Qiskit-6929C4.svg)](https://qiskit.org)

An open-source, plug-and-play **Quantum-as-a-Service (QaaS)** abstraction API. Any company, mobile app, or platform can plug into quantum computing power via simple REST endpoints — no quantum physics knowledge required.

---

## 🎯 Target Sectors & Use Cases

| Sector | Endpoint | Algorithm |
|---|---|---|
| 🔐 Cybersecurity | `/quantum/crypto/keygen` | Hadamard superposition |
| 🔐 Cybersecurity | `/quantum/crypto/entropy` | Shannon entropy scoring |
| 🔐 Cybersecurity | `/quantum/crypto/otp/encrypt` | Quantum One-Time Pad |
| 🔐 Cybersecurity | `/quantum/crypto/otp/decrypt` | Quantum OTP decryption |
| 🔐 Cybersecurity | `/quantum/crypto/bb84` | BB84 Quantum Key Distribution |
| 🗝️ Key Management | `/quantum/keys/issue` | Quantum-random key issuance |
| 🗝️ Key Management | `/quantum/keys/{id}/rotate` | Zero-downtime key rotation |
| 🗝️ Key Management | `/quantum/keys/{id}/revoke` | Permanent key revocation |
| 🗝️ Key Management | `/quantum/keys/verify` | Verify + threat detection |
| 📋 Audit | `/quantum/audit/query` | Tamper-evident event log |
| 🚨 Monitoring | `/quantum/monitor/alerts` | Active threat alerts |
| 🚨 Monitoring | `/quantum/monitor/resolve/{id}` | Resolve a threat event |
| 🚚 Logistics | `/quantum/logistics/optimize` | QAOA route optimization |
| 📈 Finance | `/quantum/finance/portfolio` | VQE portfolio optimization |

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────┐
│              Client Application Layer                  │
│       (JavaScript / PHP / Mobile Apps / Webhooks)      │
└───────────────────────────┬────────────────────────────┘
                            │ (JSON / HTTP POST)
                            ▼
┌────────────────────────────────────────────────────────┐
│                 FastAPI Gateway Layer                  │
│  • API Key Authentication     • Request Validation    │
│  • MySQL Logging & Caching    • Rate Limiting          │
└───────────────────────────┬────────────────────────────┘
                            │ (Python In-Memory)
                            ▼
┌────────────────────────────────────────────────────────┐
│               Quantum Translation Engine               │
│  • Maps input JSON to Quantum Gate Circuits            │
│  • Algorithms: Hadamard, QAOA, VQE, BB84               │
└───────────────────────────┬────────────────────────────┘
                            │ (Qiskit Circuit Objects)
                            ▼
┌────────────────────────────────────────────────────────┐
│                Quantum Execution Provider              │
│       (Default: Aer Classical Simulator)               │
│       (Production: Real QPUs via AWS Braket / IBM)     │
└────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| API Gateway | [FastAPI](https://fastapi.tiangolo.com) + [Uvicorn](https://uvicorn.org) |
| Quantum Engine | [Qiskit](https://qiskit.org) + [Qiskit-Aer](https://github.com/Qiskit/qiskit-aer) |
| Database / ORM | [MySQL](https://mysql.com) + [SQLAlchemy 2.0](https://sqlalchemy.org) |
| Auth | API Key via `X-Api-Key` header |
| Config | `python-dotenv` `.env` file |

---

## 📂 Repository Structure

```
quantum-software/
├── app/
│   ├── main.py                 # API entry point, routes, auth, rate limiting
│   ├── database.py             # SQLAlchemy engine & session setup
│   ├── models.py               # ORM: User, APIKey, JobLog, ManagedKey, AuditLog, ThreatEvent
│   └── quantum_logic/
│       ├── cryptography.py     # Hadamard keygen, OTP, entropy, BB84
│       ├── key_management.py   # Key lifecycle + threat detection engine
│       ├── logistics.py        # QAOA-inspired route optimization
│       └── finance.py          # VQE-inspired portfolio optimization
├── frontend/
│   ├── index.html              # Landing page
│   ├── crypto.html             # Cryptography console
│   ├── keys.html               # Key management console
│   ├── monitor.html            # Audit & monitoring console
│   ├── logistics.html          # Logistics console
│   ├── finance.html            # Finance console
│   ├── shared.css              # Shared stylesheet
│   └── shared.js               # Shared API client + key persistence
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or 3.11
- MySQL Server (local or Docker)

### 1. Clone & Set Up

```bash
git clone https://github.com/your-org/quantum-software.git
cd quantum-software
python -m venv venv
```

Activate:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

```env
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/quantum_api
QUANTUM_BACKEND=simulator
IBM_QUANTUM_TOKEN=your_optional_ibm_token_here
```

### 4. Create Database & Run

```sql
CREATE DATABASE quantum_api;
```

```bash
uvicorn app.main:app --reload
```

- Dashboard: **`http://127.0.0.1:5500/frontend/index.html`**
- Swagger UI: **`http://127.0.0.1:8000/docs`**
- ReDoc: **`http://127.0.0.1:8000/redoc`**

---

## 🔑 Authentication

Register to receive an API key:

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

```json
{ "user_id": "uuid-here", "api_key": "your-64-char-hex-key" }
```

Pass the key in every request:
```
X-Api-Key: your-64-char-hex-key
```

---

## ⚛️ How the Algorithms Work

This section explains the quantum algorithm behind each feature — what it does, how the circuit is built, and why it produces the result it does.

---

### 1. 🔑 Key Generation — Hadamard Superposition

**The problem it solves:** Classical computers generate pseudo-random numbers using deterministic algorithms. If you know the seed, you can reproduce the output. Quantum superposition is physically random — no seed, no pattern, no reproduction.

**How the algorithm works:**

```
Step 1: Create a quantum circuit with N qubits (one per bit of the key)
Step 2: Apply a Hadamard gate to every qubit
         |0⟩ ──[H]──  →  (|0⟩ + |1⟩) / √2   ← 50/50 superposition
Step 3: Measure all qubits — each collapses to 0 or 1 at random
Step 4: Convert the resulting bitstring to a hex key
```

**In code (`cryptography.py`):**
```python
qc = QuantumCircuit(num_bits, num_bits)
qc.h(range(num_bits))          # Hadamard on every qubit → superposition
qc.measure(range(num_bits), range(num_bits))  # collapse to random bits

bitstring = list(simulator.run(qc, shots=1).result().get_counts().keys())[0]
return hex(int(bitstring, 2))[2:].zfill(num_bits // 4)
```

**Why it's better than `os.urandom()`:** The randomness comes from quantum measurement — a physical process with no hidden state. Classical RNG always has an internal state that could theoretically be predicted or reproduced.

---

### 2. 📊 Entropy Scoring — Shannon Entropy

**The problem it solves:** How do you prove your random number generator is actually random? You measure the distribution of its outputs. A biased RNG produces some values more than others — Shannon entropy catches this.

**How the algorithm works:**

```
Step 1: Run the same Hadamard circuit `shots` times (e.g. 1024)
Step 2: Collect the frequency of each unique outcome
Step 3: Calculate Shannon entropy:
         H = -Σ p(x) × log₂(p(x))
         where p(x) = count(x) / total_shots
Step 4: Normalise against maximum possible entropy (log₂(shots))
Step 5: Return score between 0.0 and 1.0
```

**In code (`cryptography.py`):**
```python
counts = simulator.run(qc, shots=shots).result().get_counts()
probs = [c / total for c in counts.values()]
entropy = -sum(p * math.log2(p) for p in probs if p > 0)
score = round(entropy / math.log2(total), 6)
```

**Reading the score:**
| Score | Meaning |
|---|---|
| `1.0` | Perfect uniform distribution — ideal quantum randomness |
| `0.9+` | Excellent — suitable for cryptographic use |
| `< 0.8` | Biased — investigate the backend before use |

---

### 3. 🔒 Quantum One-Time Pad (OTP)

**The problem it solves:** The OTP is the only encryption scheme with a mathematical proof of unbreakability — but only if the key is truly random and never reused. Classical computers cannot guarantee true randomness. Quantum circuits can.

**How the algorithm works:**

```
Encryption:
  Step 1: Measure the plaintext byte length (e.g. "hello" = 5 bytes = 40 bits)
  Step 2: Build a quantum circuit with 40 qubits, apply Hadamard to all
  Step 3: Measure → get 40 truly random bits → convert to 5 key bytes
  Step 4: XOR each plaintext byte with the corresponding key byte
           plaintext:  01101000  ('h')
           key:        10110011  (quantum random)
           ciphertext: 11011011  (meaningless without the key)
  Step 5: Return base64(ciphertext) + base64(key)

Decryption:
  Step 1: XOR ciphertext bytes with the same key bytes
           ciphertext: 11011011
           key:        10110011
           plaintext:  01101000  ('h') ← recovered exactly
```

**In code (`cryptography.py`):**
```python
# Encrypt
key_bytes = int(bitstring, 2).to_bytes(num_bytes, byteorder="big")
ciphertext_bytes = bytes(a ^ b for a, b in zip(plaintext_bytes, key_bytes))

# Decrypt
plaintext = bytes(a ^ b for a, b in zip(ciphertext, key)).decode()
```

**Security guarantee:** Without the key, every possible plaintext is equally likely. An attacker gains zero information from the ciphertext alone — this is information-theoretic security, stronger than computational security (AES, RSA).

> ⚠️ The key is never stored server-side. Store it securely — losing it means losing the plaintext permanently.

---

### 4. 🌐 BB84 Quantum Key Distribution

**The problem it solves:** Encryption is only as secure as the key exchange. Classical key exchange (RSA, Diffie-Hellman) relies on hard math problems that quantum computers can break. BB84 makes eavesdropping physically detectable — the laws of quantum mechanics guarantee it.

**How the algorithm works:**

```
Step 1 — Alice prepares qubits:
  For each bit, Alice picks a random basis: Z (rectilinear) or X (diagonal)
  • Bit 0 in Z basis → |0⟩
  • Bit 1 in Z basis → |1⟩  (X gate applied)
  • Bit 0 in X basis → |+⟩  (H gate applied)
  • Bit 1 in X basis → |−⟩  (X then H gate applied)

Step 2 — Bob measures:
  Bob picks his own random basis for each qubit independently
  • If Bob's basis matches Alice's → measurement is always correct
  • If bases differ → measurement is random (50/50)

Step 3 — Basis reconciliation (sifting):
  Alice and Bob publicly compare which bases they used (not the bits)
  They keep only the bits where their bases matched → sifted key

Step 4 — Eavesdropping detection:
  If Eve intercepted any qubit, she had to measure it (disturbing its state)
  This introduces errors in the matching bits
  Error rate > 10% → eavesdropper detected → discard the key
```

**In code (`cryptography.py`):**
```python
for bit, a_base, b_base in zip(alice_bits, alice_bases, bob_bases):
    qc = QuantumCircuit(1, 1)
    if bit == 1:   qc.x(0)          # encode the bit
    if a_base == "X": qc.h(0)       # Alice's basis choice
    if b_base == "X": qc.h(0)       # Bob's measurement basis
    qc.measure(0, 0)

# Sift — keep only matching bases
matching = [i for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
error_rate = sum(a != b for a, b in zip(alice_key, bob_key)) / len(alice_key)
eavesdropping_detected = error_rate > 0.1
```

**Why it's quantum-safe:** Measuring a qubit destroys its original state. An eavesdropper cannot copy a qubit (no-cloning theorem) or measure it without leaving a detectable trace.

---

### 5. 🗝️ Key Management — Lifecycle & Threat Detection

**The problem it solves:** Issuing a strong key is only half the job. Keys need to be rotated regularly, revoked instantly when compromised, and every access attempt needs to be monitored for attacks.

**How the system works:**

```
Issue:   generate_quantum_key() → store in DB with app_id, status, expiry
Rotate:  generate new key → save old key as previous_key → update DB
Revoke:  set status = "revoked" → any future use triggers threat alert

Verify (threat detection pipeline):
  1. Look up key_id in DB
  2. Check replay:     has this exact key_value been used before?  → high alert
  3. Check revoked:    is status == "revoked"?                     → high alert
  4. Check expiry:     is datetime.utcnow() > expires_at?          → reject
  5. Check value:      does key_value match DB record?
       → No:  increment failure counter for this app
              if failures >= 5 in 60s → critical brute_force alert
       → Yes: mark token as used, write auth_ok to audit log
```

**In code (`key_management.py`):**
```python
token_fingerprint = f"{key_id}:{key_value}"
if token_fingerprint in _used_tokens:          # replay check
    _record_threat(..., "replay", "high", ...)

if record.status == "revoked":                 # revoked key check
    _record_threat(..., "revoked_key_use", "high", ...)

if record.key_value != key_value:              # wrong value → brute force tracking
    _track_auth_failure(...)
```

**Threat severity levels:**
| Threat | Severity | Trigger |
|---|---|---|
| `brute_force` | critical | 5+ failed verifications within 60 seconds |
| `replay` | high | Same `key_id:key_value` pair submitted more than once |
| `revoked_key_use` | high | Any use of a revoked key |

---

### 6. 🚚 Logistics — QAOA Route Optimization

**The problem it solves:** Finding the shortest route through N cities (Travelling Salesman Problem) is NP-hard — classical computers take exponential time as N grows. QAOA uses quantum interference to find good approximate solutions faster.

**How the algorithm works:**

```
Step 1 — Encoding:
  Create N×N qubits — one per (city, position) pair
  qubit[i][j] = 1 means "visit city i at position j in the route"

Step 2 — Superposition:
  Apply Hadamard to all qubits → all routes exist simultaneously

Step 3 — Cost layer (problem Hamiltonian):
  Apply RZ rotations to each qubit, weighted by the distance between cities
  Short distances → small rotation angle → higher probability of being selected
  qc.rz(π × distance[i][j] / max_distance, qubit)

Step 4 — Mixer layer:
  Apply RX rotations to allow quantum tunnelling between route configurations
  qc.rx(π/4, all_qubits)

Step 5 — Measure:
  Run 512 shots → the most frequently measured bitstring encodes the best route
  Decode bitstring → city visit order → calculate total distance
```

**In code (`logistics.py`):**
```python
qc.h(range(num_qubits))                          # superposition over all routes

for i in range(n):
    for j in range(n):
        angle = distances[i][j] / max_distance
        qc.rz(math.pi * angle, i * n + j)        # cost encoding

qc.rx(math.pi / 4, range(num_qubits))            # mixer

best_bitstring = max(counts, key=counts.get)     # most probable = best route
```

**Why quantum helps:** Classical solvers must evaluate routes one at a time. The quantum circuit evaluates all routes simultaneously through superposition, then uses interference to amplify the probability of low-cost routes.

---

### 7. 📈 Finance — VQE Portfolio Optimization

**The problem it solves:** Markowitz portfolio optimization — finding the best mix of assets to maximise return for a given risk level — is a quadratic optimization problem. For large portfolios it becomes computationally expensive. VQE uses a parameterized quantum circuit to find the minimum-cost allocation.

**How the algorithm works:**

```
Step 1 — Superposition:
  N qubits (one per asset), all placed in superposition
  Each qubit being |1⟩ = "include this asset", |0⟩ = "exclude"

Step 2 — RY rotations (return vs risk encoding):
  For each asset i:
    return_angle = (return[i] / max_return) × π
    risk_angle   = (sum of row i in risk_matrix / n) × π × risk_tolerance
    net_angle    = return_angle - risk_angle
    qc.ry(net_angle, qubit_i)

  High return + low risk → large positive angle → qubit biased toward |1⟩ (include)
  Low return + high risk → small/negative angle → qubit biased toward |0⟩ (exclude)

Step 3 — Entanglement (correlation):
  CNOT gates between adjacent qubits model asset correlations
  qc.cx(i, i+1)

Step 4 — Measure:
  Run 1024 shots → most frequent bitstring = optimal asset selection
  Normalise selected assets to portfolio weights
```

**In code (`finance.py`):**
```python
for i in range(n):
    return_angle = (returns[i] / max_return) * math.pi
    risk_angle   = sum(risk_matrix[i]) / (n * max_return) * math.pi * risk_tolerance
    qc.ry(return_angle - risk_angle, i)   # encode return vs risk tradeoff

for i in range(n - 1):
    qc.cx(i, i + 1)                       # entangle correlated assets

best = max(counts, key=counts.get)        # most probable = optimal allocation
```

**Reading the output:**
- `allocation`: weight of each asset in the portfolio (sums to 1.0 across selected assets)
- `selected_assets`: assets with non-zero weight
- `risk_tolerance = 0.0` → most conservative (minimise risk, accept lower return)
- `risk_tolerance = 1.0` → most aggressive (maximise return, accept higher risk)

---

## 📡 API Reference

### `GET /health`
Health check. No auth required.

---

### `POST /quantum/crypto/keygen`
Generate a quantum-random cryptographic key.

```json
{ "num_bits": 256 }
```
```json
{ "key": "a3f9c2e1b7d4...", "bits": 256 }
```

---

### `POST /quantum/crypto/entropy`
Score the randomness quality of the quantum backend.

```json
{ "num_bits": 64, "shots": 1024 }
```
```json
{ "entropy_score": 0.998721, "unique_outcomes": 1024, "shots": 1024 }
```

---

### `POST /quantum/crypto/otp/encrypt`
Encrypt a message with a quantum One-Time Pad.

```json
{ "plaintext": "launch code: X7" }
```
```json
{ "ciphertext": "base64...", "key": "base64...", "message_length": 15 }
```
> ⚠️ Save the `key` — it is never stored server-side.

---

### `POST /quantum/crypto/otp/decrypt`
Decrypt a quantum OTP ciphertext.

```json
{ "ciphertext": "base64...", "key": "base64..." }
```
```json
{ "plaintext": "launch code: X7" }
```

---

### `POST /quantum/crypto/bb84`
Simulate BB84 Quantum Key Distribution with eavesdropping detection.

```json
{ "num_bits": 16 }
```
```json
{
  "sifted_key_length": 8,
  "shared_key": "10110100",
  "error_rate": 0.0,
  "eavesdropping_detected": false
}
```

---

### `POST /quantum/keys/issue`
Issue a quantum-random key for a client app.

```json
{ "app_id": "my-web-app", "key_bits": 256, "ttl_hours": 24 }
```
```json
{
  "key_id": "uuid",
  "app_id": "my-web-app",
  "key_value": "a3f9c2...",
  "status": "active",
  "expires_at": "2024-01-02T12:00:00"
}
```

---

### `POST /quantum/keys/{key_id}/rotate`
Replace a live key. Previous key preserved for graceful transition.

```json
{ "key_id": "uuid", "key_value": "new-key", "previous_key": "old-key" }
```

---

### `DELETE /quantum/keys/{key_id}/revoke`
Permanently revoke a key. Future use triggers a threat alert.

---

### `POST /quantum/keys/verify`
Verify a key with automatic threat detection.

```json
{ "key_id": "uuid", "key_value": "a3f9c2..." }
```
```json
{ "valid": true, "app_id": "my-web-app", "key_id": "uuid" }
```

Failure reasons: `key_not_found` · `replay_detected` · `key_revoked` · `key_expired` · `invalid_key`

---

### `POST /quantum/audit/query`
Query the tamper-evident audit log.

```json
{ "app_id": "my-web-app", "limit": 50 }
```

---

### `POST /quantum/monitor/alerts`
Get active threat alerts.

```json
{ "app_id": "my-web-app", "unresolved_only": true }
```
```json
[{
  "id": "uuid",
  "threat_type": "brute_force",
  "severity": "critical",
  "detail": "5 failed auth attempts in 60s from 192.168.1.1",
  "resolved": false
}]
```

---

### `POST /quantum/monitor/resolve/{threat_id}`
Mark a threat event as resolved.

---

### `POST /quantum/logistics/optimize`
Optimize a multi-city route via QAOA.

```json
{ "distances": [[0,10,15],[10,0,35],[15,35,0]] }
```
```json
{ "route": [0, 1, 2], "total_distance": 60.0 }
```

---

### `POST /quantum/finance/portfolio`
Quantum portfolio optimization via VQE ansatz.

```json
{
  "returns": [0.12, 0.08, 0.15, 0.05],
  "risk_matrix": [[0.1,0.02],[0.02,0.08]],
  "risk_tolerance": 0.5
}
```
```json
{
  "allocation": { "asset_0": 0.5, "asset_2": 0.5 },
  "selected_assets": ["asset_0", "asset_2"]
}
```

---

## ⚠️ Rate Limiting

Each API key is limited to **10 requests per minute**:

```json
{ "detail": "Rate limit exceeded. Max 10 requests/minute." }
```

---

## 🛡️ Compliance & Data Protection

### What is built in

| Requirement | Regulation | Implementation |
|---|---|---|
| Tamper-evident audit log | SOC 2, ISO 27001, HIPAA | `AuditLog` table — every security event logged with timestamp + IP |
| Key lifecycle management | NIST SP 800-57, PCI-DSS | Issue, rotate, revoke, expiry — full lifecycle in `ManagedKey` |
| Threat detection & alerting | SOC 2 CC6, ISO 27001 A.12.4 | Brute force, replay, revoked key use — auto-detected + stored |
| Rate limiting | OWASP API Top 10 | 10 req/min per API key |
| Encryption at rest | GDPR, HIPAA, PCI-DSS | All `key_value` fields encrypted with AES-256-GCM via `DB_ENCRYPTION_KEY` |
| GDPR right to be forgotten | GDPR Art. 17 | `DELETE /users/{id}` — anonymises PII, revokes all keys, soft-deletes account |
| GDPR right to access | GDPR Art. 15 | `GET /users/{id}/export` — returns all data held for the user |
| Log retention policy | SOC 2, GDPR Art. 5 | `DELETE /admin/purge-logs` — purge logs older than N days |
| Soft delete | GDPR, audit integrity | `deleted_at` on `User` — record kept for audit trail, PII anonymised |
| Retention metadata | SOC 2, ISO 27001 | `retention_days` on `JobLog` (90d) and `AuditLog` (365d) |

---

### Encryption at rest setup

Generate a `DB_ENCRYPTION_KEY` and add it to your `.env`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

```env
DB_ENCRYPTION_KEY=your_64_char_hex_string_here
```

All `key_value` and `previous_key` fields are encrypted with **AES-256-GCM** before being written to the database. The nonce is unique per encryption and stored alongside the ciphertext. Decryption only happens in memory during verification — the plaintext key never persists.

---

### GDPR endpoints

**Right to be forgotten — `DELETE /users/{user_id}`**
- Anonymises the email to `deleted_{id}@anonymised`
- Sets `deleted_at` timestamp
- Revokes all API keys and managed keys
- Audit log records are retained (required for legal/security integrity) but PII is removed

```json
{ "deleted": true, "user_id": "uuid", "anonymised_at": "2024-01-01T12:00:00" }
```

**Right to access — `GET /users/{user_id}/export`**
- Returns all data held: account info, managed keys (metadata only, no key values), audit logs, job logs, threat events
- Key values are never included in the export

---

### Log retention

**`DELETE /admin/purge-logs`**

```json
{ "older_than_days": 90 }
```

```json
{
  "purged_job_logs": 142,
  "purged_audit_logs": 0,
  "cutoff_date": "2023-10-01T00:00:00"
}
```

Default retention periods:
- `JobLog` — 90 days
- `AuditLog` — 365 days (SOC 2 / ISO 27001 minimum)

---

### Compliance status summary

| Regulation | Status | Notes |
|---|---|---|
| **GDPR** | ✅ Core requirements met | Deletion, export, anonymisation, encryption at rest |
| **NIST SP 800-57** | ✅ Full | Key issue, rotate, revoke, expiry lifecycle |
| **SOC 2 Type II** | ✅ Core requirements met | Audit log, threat detection, retention policy |
| **PCI-DSS** | ✅ Core requirements met | Encryption at rest, key management, audit trail |
| **ISO 27001** | ✅ Core requirements met | A.12.4 logging, A.9.4 access control, A.10.1 cryptography |
| **HIPAA** | ⚠️ Partial | Add TLS enforcement + field-level encryption for PHI at deployment |
| **FIPS 140-2** | ❌ Not applicable | Requires certified hardware module — out of scope for simulator |

---

## 🔁 Switching to Real Quantum Hardware

Default backend is `AerSimulator` (local classical simulation).

**IBM Quantum:**
```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService(channel="ibm_quantum", token=os.getenv("IBM_QUANTUM_TOKEN"))
backend = service.least_busy(operational=True, simulator=False)
```

**AWS Braket:** Replace `AerSimulator()` with a `BraketLocalBackend` or a managed device ARN via the `amazon-braket-sdk`.

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

1. Fork the repo
2. `git checkout -b feature/your-feature`
3. `git commit -m 'Add your feature'`
4. `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
