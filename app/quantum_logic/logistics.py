# Original Author: Oluwatosin Olalere (GitHub: olo-lade)
# Repository: https://github.com/olo-lade/Quantum_software
# License: CC BY 4.0 — Credit required for any use or derivative work.

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import math


def optimize_route(distances: list[list[float]]) -> dict:
    """
    Approximate TSP route optimization using a QAOA-inspired ansatz.
    For n cities, encodes pairwise cost into a parameterized circuit.
    Returns the best measured route and its total distance.
    """
    n = len(distances)
    num_qubits = n * n  # one qubit per (city, position) pair

    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))

    # Cost layer: apply RZ rotations weighted by distance
    for i in range(n):
        for j in range(n):
            if i != j:
                qubit = i * n + j
                angle = distances[i][j] / (max(max(row) for row in distances) + 1e-9)
                qc.rz(math.pi * angle, qubit)

    # Mixer layer
    qc.rx(math.pi / 4, range(num_qubits))
    qc.measure(range(num_qubits), range(num_qubits))

    simulator = AerSimulator()
    job = simulator.run(qc, shots=512)
    counts = job.result().get_counts()

    best_bitstring = max(counts, key=counts.get)
    route = _decode_route(best_bitstring, n)
    total_distance = _calculate_distance(route, distances)

    return {"route": route, "total_distance": total_distance}


def _decode_route(bitstring: str, n: int) -> list[int]:
    """Decode a bitstring into a city visit order."""
    matrix = [[int(bitstring[i * n + j]) for j in range(n)] for i in range(n)]
    route = []
    used = set()
    for pos in range(n):
        col = [matrix[city][pos] for city in range(n)]
        city = next((i for i in range(n) if col[i] == 1 and i not in used), pos % n)
        route.append(city)
        used.add(city)
    return route


def _calculate_distance(route: list[int], distances: list[list[float]]) -> float:
    total = sum(distances[route[i]][route[(i + 1) % len(route)]] for i in range(len(route)))
    return round(total, 4)
