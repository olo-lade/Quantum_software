# 🌌 Quantum Software (QaaS Layer)

> **Original Author:** Joshua Tosin Pamilerin (GitHub: [olo-lade](https://github.com/olo-lade))
> **Repository:** https://github.com/olo-lade/Quantum_software
> **License:** [CC BY 4.0](LICENSE) — You must credit the original author in any use, fork, or derivative work.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![Quantum Engine](https://img.shields.io/badge/Quantum-Qiskit-6929C4.svg)](https://qiskit.org)

An open-source, plug-and-play **Quantum-as-a-Service (QaaS)** abstraction API. This platform allows companies, mobile apps, and enterprise systems to leverage quantum computing power via simple REST endpoints — without writing a single line of quantum circuit physics.

---

## 🎯 Target Sectors & Use Cases

| Sector | Endpoint | Algorithm |
|---|---|---|
| 🔐 Cybersecurity | `/quantum/crypto/keygen` | Hadamard superposition (true quantum randomness) |
| 🚚 Logistics | `/quantum/logistics/optimize` | QAOA (Quantum Approximate Optimization Algorithm) |
| 📈 Finance | `/quantum/finance/portfolio` | VQE-inspired ansatz (Variational Quantum Eigensolver) |

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
│  • Algorithms: Hadamard, QAOA, VQE                     │
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
│   ├── __init__.py
│   ├── main.py                 # API entry point, routes, auth, rate limiting
│   ├── database.py             # SQLAlchemy engine & session setup
│   ├── models.py               # ORM schemas: User, APIKey, JobLog
│   └── quantum_logic/
│       ├── __init__.py
│       ├── cryptography.py     # Quantum key generation (Hadamard)
│       ├── logistics.py        # Route optimization (QAOA-inspired)
│       └── finance.py          # Portfolio optimization (VQE-inspired)
├── frontend/
│   └── index.html              # Single-page dashboard UI
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
├── CONTRIBUTING.md             # Contribution guidelines
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT License
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or 3.11
- MySQL Server (local or Docker)

### 1. Clone & Set Up Virtual Environment

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

Edit `.env` with your database credentials:

```env
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/quantum_api
QUANTUM_BACKEND=simulator
IBM_QUANTUM_TOKEN=your_optional_ibm_token_here
```

### 4. Create the Database

```sql
CREATE DATABASE quantum_api;
```

Tables are auto-created on first startup via SQLAlchemy.

### 5. Run the Server

```bash
uvicorn app.main:app --reload
```

Swagger UI: **`http://127.0.0.1:8000/docs`**
ReDoc: **`http://127.0.0.1:8000/redoc`**

---

## 🔑 Authentication

All quantum endpoints require an `X-Api-Key` header. Register a user first to receive a key:

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

Response:
```json
{
  "user_id": "uuid-here",
  "api_key": "your-64-char-hex-key"
}
```

Use the key in all subsequent requests:
```
X-Api-Key: your-64-char-hex-key
```

---

## 📡 API Endpoints

### `GET /health`
Health check. No auth required.

```bash
curl http://127.0.0.1:8000/health
```

---

### `POST /quantum/crypto/keygen`
Generate a quantum-random cryptographic key using Hadamard superposition.

**Request:**
```json
{
  "num_bits": 256
}
```

**Response:**
```json
{
  "key": "a3f9c2e1b7d4...",
  "bits": 256
}
```

| Field | Type | Default | Range |
|---|---|---|---|
| `num_bits` | integer | `256` | `8 – 512` |

---

### `POST /quantum/logistics/optimize`
Optimize a multi-city route using a QAOA-inspired quantum circuit.

**Request:**
```json
{
  "distances": [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
  ]
}
```

**Response:**
```json
{
  "route": [0, 1, 3, 2],
  "total_distance": 80.0
}
```

| Field | Type | Description |
|---|---|---|
| `distances` | `float[][]` | Square NxN matrix of city-to-city distances |

---

### `POST /quantum/finance/portfolio`
Quantum-assisted portfolio optimization using a VQE-inspired ansatz.

**Request:**
```json
{
  "returns": [0.12, 0.08, 0.15, 0.05],
  "risk_matrix": [
    [0.1, 0.02, 0.04, 0.01],
    [0.02, 0.08, 0.03, 0.02],
    [0.04, 0.03, 0.12, 0.01],
    [0.01, 0.02, 0.01, 0.05]
  ],
  "risk_tolerance": 0.5
}
```

**Response:**
```json
{
  "allocation": {
    "asset_0": 0.5,
    "asset_1": 0.0,
    "asset_2": 0.5,
    "asset_3": 0.0
  },
  "selected_assets": ["asset_0", "asset_2"]
}
```

| Field | Type | Default | Description |
|---|---|---|---|
| `returns` | `float[]` | — | Expected return per asset |
| `risk_matrix` | `float[][]` | — | NxN covariance matrix |
| `risk_tolerance` | `float` | `0.5` | `0.0` (low risk) to `1.0` (high risk) |

---

## ⚠️ Rate Limiting

Each API key is limited to **10 requests per minute**. Exceeding this returns:

```json
{
  "detail": "Rate limit exceeded. Max 10 requests/minute."
}
```

---

## 🔁 Switching to Real Quantum Hardware

By default the API runs on the `AerSimulator` (local classical simulation). To target real QPUs:

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

Quick steps:
1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
