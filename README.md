# Quantum Software Infrastructure (PRIVATE)

This repository is **private** and contains production-only resources.

## Contents

| Folder | Description |
|---|---|
| `deployment/` | AWS CDK / Terraform cloud deployment scripts |
| `payments/` | Stripe payment gateway integration |
| `secrets/` | Production environment configs (never commit `.env`) |
| `database/` | Production DB migration scripts |

## ⚠️ Security Rules

- NEVER push `.env` files with real credentials
- NEVER make this repository public
- All secrets must use AWS Secrets Manager or environment variables

## Linked Public Repo

Core API code lives at: https://github.com/olo-lade/Quantum_software
