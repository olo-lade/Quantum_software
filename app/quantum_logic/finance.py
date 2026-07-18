# Original Author: Joshua Tosin Pamilerin (GitHub: olo-lade)
# Repository: https://github.com/olo-lade/Quantum_software
# License: CC BY 4.0 — Credit required for any use or derivative work.

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import math


def optimize_portfolio(returns: list[float], risk_matrix: list[list[float]], risk_tolerance: float = 0.5) -> dict:
    """
    Quantum-assisted portfolio optimization using a VQE-inspired ansatz.
    Encodes asset returns and risk into rotation angles, measures optimal allocation.
    """
    n = len(returns)
    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    max_return = max(abs(r) for r in returns) or 1.0

    for i in range(n):
        return_angle = (returns[i] / max_return) * math.pi
        risk_angle = sum(risk_matrix[i]) / (n * max_return) * math.pi * risk_tolerance
        qc.ry(return_angle - risk_angle, i)

    # Entangle correlated assets
    for i in range(n - 1):
        qc.cx(i, i + 1)

    qc.measure(range(n), range(n))

    simulator = AerSimulator()
    job = simulator.run(qc, shots=1024)
    counts = job.result().get_counts()

    best = max(counts, key=counts.get)
    weights = _normalize_weights(best, n)
    return {"allocation": weights, "selected_assets": [f"asset_{i}" for i in range(n) if int(best[-(i+1)]) == 1]}


def _normalize_weights(bitstring: str, n: int) -> dict:
    bits = [int(bitstring[-(i + 1)]) for i in range(n)]
    total = sum(bits) or 1
    return {f"asset_{i}": round(bits[i] / total, 4) for i in range(n)}
