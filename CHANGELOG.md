# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.0.0] - 2024-01-01

### Added
- FastAPI gateway with API key authentication and rate limiting (10 req/min per key).
- `POST /users` endpoint for user registration and API key generation.
- `POST /quantum/crypto/keygen` — quantum-random key generation via Hadamard superposition.
- `POST /quantum/logistics/optimize` — multi-city route optimization via QAOA-inspired circuit.
- `POST /quantum/finance/portfolio` — portfolio optimization via VQE-inspired ansatz.
- `GET /health` — system health check endpoint.
- MySQL persistence via SQLAlchemy 2.0 ORM (Users, APIKeys, JobLogs).
- Auto table creation on server startup via `lifespan` context manager.
- Full job audit logging (input + result) for every quantum request.
- `AerSimulator` as the default quantum execution backend.
- `.env` based configuration with `python-dotenv`.
